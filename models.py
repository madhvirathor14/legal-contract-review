"""
Typed Pydantic models for Legal Contract Review Environment.
OpenEnv spec compliance: typed models for /reset, /step, /state endpoints.
"""

from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ─────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────

class TaskName(str, Enum):
    FIND_MISSING_CLAUSES = "find_missing_clauses"   # Easy
    IDENTIFY_RISKY_PARTY = "identify_risky_party"   # Medium
    REWRITE_AMBIGUOUS    = "rewrite_ambiguous"       # Hard


class ClauseType(str, Enum):
    TERMINATION             = "termination"
    CONFIDENTIALITY         = "confidentiality"
    INDEMNIFICATION         = "indemnification"
    DISPUTE_RESOLUTION      = "dispute_resolution"
    PAYMENT_TERMS           = "payment_terms"
    INTELLECTUAL_PROPERTY   = "intellectual_property"
    LIMITATION_OF_LIABILITY = "limitation_of_liability"
    GOVERNING_LAW           = "governing_law"


class Party(str, Enum):
    PARTY_A = "Party A"
    PARTY_B = "Party B"
    BOTH    = "Both equally"
    NEUTRAL = "Neither"


# ─────────────────────────────────────────────
# Action Models (what the agent sends)
# ─────────────────────────────────────────────

class FindMissingClausesAction(BaseModel):
    """Agent submits a list of clause types it believes are missing."""
    missing_clauses: List[ClauseType] = Field(
        ...,
        description="List of clause types the agent thinks are missing from the contract"
    )


class IdentifyRiskyPartyAction(BaseModel):
    """Agent identifies which party is disadvantaged by a specific clause."""
    clause_id: str = Field(
        ...,
        description="ID of the clause being analyzed (e.g., 'clause_3')"
    )
    disadvantaged_party: Party = Field(
        ...,
        description="Which party is disadvantaged by this clause"
    )
    reasoning: str = Field(
        ...,
        description="Brief explanation of why this party is disadvantaged"
    )


class RewriteAmbiguousAction(BaseModel):
    """Agent rewrites an ambiguous clause to be legally sound."""
    clause_id: str = Field(
        ...,
        description="ID of the ambiguous clause to rewrite"
    )
    rewritten_clause: str = Field(
        ...,
        description="The rewritten, legally sound version of the clause"
    )


class ContractAction(BaseModel):
    """Top-level action wrapper — agent sends ONE of the task-specific actions."""
    task: TaskName
    find_missing: Optional[FindMissingClausesAction] = None
    identify_risky: Optional[IdentifyRiskyPartyAction] = None
    rewrite: Optional[RewriteAmbiguousAction] = None


# ─────────────────────────────────────────────
# Observation Models (what the agent receives)
# ─────────────────────────────────────────────

class ContractClause(BaseModel):
    """A single clause in a contract."""
    clause_id: str
    clause_type: Optional[ClauseType] = None
    title: str
    text: str
    is_ambiguous: bool = False
    flagged_for_analysis: bool = False


class ContractObservation(BaseModel):
    """Full observation returned to the agent after reset/step."""
    contract_id: str
    contract_title: str
    contract_text: str
    clauses: List[ContractClause]
    task: TaskName
    task_description: str
    step_number: int
    max_steps: int
    last_action_feedback: Optional[str] = None
    last_action_error: Optional[str] = None
    score_so_far: float = 0.0


# ─────────────────────────────────────────────
# Step Result
# ─────────────────────────────────────────────

class StepResult(BaseModel):
    observation: ContractObservation
    reward: float = Field(ge=0.0, le=1.0)
    done: bool
    info: Dict[str, Any] = {}


# ─────────────────────────────────────────────
# Reset / State
# ─────────────────────────────────────────────

class ResetRequest(BaseModel):
    task: Optional[TaskName] = None
    seed: Optional[int] = None


class StateResponse(BaseModel):
    current_observation: ContractObservation
    total_reward: float
    steps_taken: int
    done: bool
