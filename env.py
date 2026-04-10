"""
Core environment logic for Legal Contract Review Environment.
Manages episode state, task selection, and step execution.
"""

import random
from typing import Optional, Dict, Any, List

from models import (
    TaskName, ContractAction, ContractObservation, ContractClause,
    StepResult, ResetRequest
)
from contracts import FIND_MISSING_CONTRACTS, IDENTIFY_RISKY_CONTRACTS, REWRITE_CONTRACTS
from graders import grade_action


MAX_STEPS_PER_TASK = {
    TaskName.FIND_MISSING_CLAUSES: 3,   # Easy — 3 attempts
    TaskName.IDENTIFY_RISKY_PARTY: 2,   # Medium — 2 attempts
    TaskName.REWRITE_AMBIGUOUS:    1,   # Hard — 1 attempt (like real legal review)
}

TASK_DESCRIPTIONS = {
    TaskName.FIND_MISSING_CLAUSES: (
        "EASY TASK: Review this contract and identify ALL missing standard clause types. "
        "Submit a list of clause type names that should be in this contract but aren't. "
        "Standard clauses include: termination, confidentiality, indemnification, "
        "dispute_resolution, payment_terms, intellectual_property, limitation_of_liability, governing_law."
    ),
    TaskName.IDENTIFY_RISKY_PARTY: (
        "MEDIUM TASK: A specific clause in this contract has been flagged as one-sided. "
        "Identify which party (Party A or Party B) is disadvantaged by the target clause, "
        "and provide your legal reasoning."
    ),
    TaskName.REWRITE_AMBIGUOUS: (
        "HARD TASK: The flagged clause is legally ambiguous and potentially unenforceable. "
        "Rewrite it to be legally precise, specific, and enforceable. "
        "Your rewrite must define all vague terms, include specific timeframes/amounts, "
        "add appropriate carve-outs, and use proper legal language."
    ),
}


class LegalContractEnv:
    """
    Stateful Legal Contract Review Environment.
    One episode = one contract + one task.
    """

    def __init__(self):
        self._reset_state()

    def _reset_state(self):
        self.current_task: Optional[TaskName]  = None
        self.current_contract: Optional[Dict]  = None
        self.step_count: int                   = 0
        self.total_reward: float               = 0.0
        self.done: bool                        = False
        self.best_score: float                 = 0.0
        self.history: List[Dict]               = []

    def reset(self, request: Optional[ResetRequest] = None) -> StepResult:
        """Start a new episode. Picks a task and contract."""
        self._reset_state()

        # Pick task
        if request and request.task:
            self.current_task = request.task
        else:
            self.current_task = random.choice(list(TaskName))

        # Pick contract for that task
        seed = request.seed if request else None
        rng  = random.Random(seed)

        if self.current_task == TaskName.FIND_MISSING_CLAUSES:
            pool = FIND_MISSING_CONTRACTS
        elif self.current_task == TaskName.IDENTIFY_RISKY_PARTY:
            pool = IDENTIFY_RISKY_CONTRACTS
        else:
            pool = REWRITE_CONTRACTS

        self.current_contract = rng.choice(pool)

        obs = self._build_observation(feedback=None, error=None)
        return StepResult(observation=obs, reward=0.0, done=False, info={"reset": True})

    def step(self, action: ContractAction) -> StepResult:
        """Process one agent action and return reward + new observation."""
        if self.done:
            obs = self._build_observation(
                feedback="Episode already finished. Call reset() to start a new episode.",
                error="Episode is done"
            )
            return StepResult(observation=obs, reward=0.0, done=True)

        if self.current_task is None or self.current_contract is None:
            obs = self._build_observation(
                feedback="Environment not initialized. Call reset() first.",
                error="Not initialized"
            )
            return StepResult(observation=obs, reward=0.0, done=True)

        # Validate task matches
        if action.task != self.current_task:
            obs = self._build_observation(
                feedback=f"Task mismatch. Current task is '{self.current_task.value}' but action is for '{action.task.value}'.",
                error="Task mismatch"
            )
            return StepResult(observation=obs, reward=0.0, done=False)

        self.step_count += 1
        max_steps = MAX_STEPS_PER_TASK[self.current_task]

        # Grade the action
        score, feedback = grade_action(action, self.current_contract, self.current_task)

        improvement     = max(0.0, score - self.best_score)
        self.best_score = max(self.best_score, score)
        reward          = score

        self.total_reward += reward
        self.history.append({
            "step": self.step_count,
            "score": score,
            "feedback": feedback,
        })

        done = (score >= 0.95) or (self.step_count >= max_steps)
        self.done = done

        obs = self._build_observation(feedback=feedback, error=None, score=score)
        return StepResult(
            observation=obs,
            reward=round(reward, 3),
            done=done,
            info={"score": score, "step": self.step_count, "improvement": round(improvement, 3)}
        )

    def get_state(self) -> StepResult:
        """Return current state without advancing."""
        if self.current_contract is None:
            obs = ContractObservation(
                contract_id="none",
                contract_title="Not initialized",
                contract_text="Call POST /reset to begin.",
                clauses=[],
                task=TaskName.FIND_MISSING_CLAUSES,
                task_description="Call reset first.",
                step_number=0,
                max_steps=0,
            )
            return StepResult(observation=obs, reward=0.0, done=False)

        obs = self._build_observation(feedback="State snapshot.", error=None)
        return StepResult(observation=obs, reward=self.total_reward, done=self.done)

    def _build_observation(
        self,
        feedback: Optional[str],
        error: Optional[str],
        score: float = 0.0
    ) -> ContractObservation:
        if self.current_contract is None:
            return ContractObservation(
                contract_id="none",
                contract_title="Not initialized",
                contract_text="",
                clauses=[],
                task=TaskName.FIND_MISSING_CLAUSES,
                task_description="",
                step_number=0,
                max_steps=0,
            )

        contract  = self.current_contract
        max_steps = MAX_STEPS_PER_TASK[self.current_task]
        task_desc = contract.get("task_description", TASK_DESCRIPTIONS[self.current_task])

        raw_clauses = contract.get("clauses", [])
        if self.current_task == TaskName.REWRITE_AMBIGUOUS:
            raw_clauses = contract.get("ambiguous_clauses", raw_clauses)
            target_id   = contract.get("target_clause_id")
            if target_id:
                raw_clauses = [c for c in raw_clauses if c.get("clause_id") == target_id] or raw_clauses

        clauses = [
            ContractClause(
                clause_id=c["clause_id"],
                title=c["title"],
                text=c["text"],
                clause_type=c.get("clause_type"),
                is_ambiguous=c.get("is_ambiguous", False),
                flagged_for_analysis=c.get("flagged_for_analysis", False),
            )
            for c in raw_clauses
        ]

        return ContractObservation(
            contract_id=contract["contract_id"],
            contract_title=contract["contract_title"],
            contract_text=contract["contract_text"],
            clauses=clauses,
            task=self.current_task,
            task_description=task_desc,
            step_number=self.step_count,
            max_steps=max_steps,
            last_action_feedback=feedback,
            last_action_error=error,
            score_so_far=round(self.best_score, 3),
        )
