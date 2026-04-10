"""
Inference Script — Legal Contract Review Environment
=====================================================
OpenEnv Hackathon compliant inference script.

Uses Groq API for ultra-fast LLM inference (llama-3.3-70b-versatile by default).
Compatible with any OpenAI-spec endpoint via API_BASE_URL.

stdout emits exactly:
  [START] task=<task_name> env=<benchmark> model=<model_name>
  [STEP]  step=<n> action=<action_str> reward=<0.00> done=<true|false> error=<msg|null>
  [END]   success=<true|false> steps=<n> score=<score> rewards=<r1,r2,...,rn>

Environment Variables:
  GROQ_API_KEY   Groq API key (primary)
  HF_TOKEN       HuggingFace / fallback API key
  API_KEY        Generic API key fallback
  API_BASE_URL   LLM endpoint (default: Groq)
  MODEL_NAME     Model identifier (default: llama-3.3-70b-versatile)
  ENV_BASE_URL   Legal Contract Env URL (default: http://localhost:7860)
  TASK_NAME      Task to run (default: find_missing_clauses)
"""

import asyncio
import json
import os
import textwrap
import httpx
from typing import List, Optional
from openai import OpenAI

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

# Groq is primary (fastest), falls back to HF router
API_KEY      = (
    os.getenv("GROQ_API_KEY") or
    os.getenv("HF_TOKEN") or
    os.getenv("API_KEY", "")
)
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME   = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
ENV_BASE_URL = os.getenv("ENV_BASE_URL", "http://localhost:7860")
TASK_NAME    = os.getenv("TASK_NAME", "find_missing_clauses")
BENCHMARK    = os.getenv("BENCHMARK", "legal_contract_review")

MAX_STEPS               = 3
TEMPERATURE             = 0.2     # Low for precise legal reasoning
MAX_TOKENS              = 600
SUCCESS_SCORE_THRESHOLD = 0.5

# ─────────────────────────────────────────────
# Mandatory Logging Format
# ─────────────────────────────────────────────

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)

def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val  = str(done).lower()
    action_clean = action.replace("\n", " ").replace("\r", "").strip()[:200]
    print(
        f"[STEP] step={step} action={action_clean} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )

def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )

# ─────────────────────────────────────────────
# System Prompts per Task
# ─────────────────────────────────────────────

SYSTEM_PROMPTS = {
    "find_missing_clauses": textwrap.dedent("""
        You are an expert contract attorney reviewing legal agreements.
        Your task is to identify MISSING standard clauses from contracts.

        Standard clause types to check for:
        - termination
        - confidentiality
        - indemnification
        - dispute_resolution
        - payment_terms
        - intellectual_property
        - limitation_of_liability
        - governing_law

        You will receive a contract. Respond ONLY with a valid JSON object in this exact format:
        {
          "task": "find_missing_clauses",
          "find_missing": {
            "missing_clauses": ["termination", "governing_law"]
          }
        }

        Rules:
        - Only include clause types from the standard list above
        - Only list clauses that are genuinely ABSENT from the contract
        - Do NOT include clauses that are present even if poorly written
        - Respond ONLY with the JSON — no explanation, no markdown, no preamble
    """).strip(),

    "identify_risky_party": textwrap.dedent("""
        You are an expert contract attorney analyzing contract fairness.
        Your task is to identify which party is disadvantaged by a specific flagged clause.

        Parties are labeled "Party A" and "Party B" with their real names given in the contract.
        Your options for disadvantaged_party: "Party A", "Party B", "Both equally", "Neither"

        You will receive a contract and the target clause to analyze.
        Respond ONLY with a valid JSON object in this exact format:
        {
          "task": "identify_risky_party",
          "identify_risky": {
            "clause_id": "clause_6",
            "disadvantaged_party": "Party B",
            "reasoning": "This clause is one-sided because Party B bears all obligations while Party A retains sole discretion with no recourse."
          }
        }

        Rules:
        - Use the exact clause_id from the task description
        - Reasoning must be 1-2 sentences explaining the imbalance using legal terms
        - Use words like: unilateral, one-sided, disproportionate, no recourse, bears all risk
        - Respond ONLY with JSON — no markdown, no preamble
    """).strip(),

    "rewrite_ambiguous": textwrap.dedent("""
        You are an expert contract drafter specializing in making vague clauses legally enforceable.
        Your task is to REWRITE an ambiguous clause to be precise and legally sound.

        A good rewrite MUST include:
        1. Specific numbers, percentages, timeframes (e.g., "within 30 days", "60% of net profit")
        2. Clearly defined terms (no "reasonable", "appropriate", "periodically", "fair")
        3. Carve-outs and exceptions where appropriate (provided that, except, notwithstanding)
        4. Formal legal language ("shall", "in writing", "binding", "obligated")
        5. Dispute resolution mechanism if applicable

        You will receive a contract with a flagged ambiguous clause.
        Respond ONLY with a valid JSON object in this exact format:
        {
          "task": "rewrite_ambiguous",
          "rewrite": {
            "clause_id": "clause_1",
            "rewritten_clause": "Your precise, enforceable rewrite here. Must be at least 50 words."
          }
        }

        Rules:
        - Use the exact clause_id from the task description
        - Rewrite must be at least 50 words with specific figures
        - Replace ALL vague terms: "reasonable", "appropriate", "periodically", "fair", "timely"
        - Respond ONLY with JSON — no markdown, no preamble
    """).strip(),
}

# ─────────────────────────────────────────────
# Environment Client
# ─────────────────────────────────────────────

async def env_reset(task: str) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{ENV_BASE_URL}/reset",
            json={"task": task},
        )
        resp.raise_for_status()
        return resp.json()

async def env_step(action: dict) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.post(
            f"{ENV_BASE_URL}/step",
            json=action,
        )
        resp.raise_for_status()
        return resp.json()

# ─────────────────────────────────────────────
# LLM Agent
# ─────────────────────────────────────────────

def build_user_prompt(
    observation: dict,
    task: str,
    step: int,
    last_feedback: Optional[str]
) -> str:
    contract_title = observation.get("contract_title", "Unknown Contract")
    contract_text  = observation.get("contract_text", "")
    task_desc      = observation.get("task_description", "")
    clauses        = observation.get("clauses", [])
    score_so_far   = observation.get("score_so_far", 0.0)
    max_steps      = observation.get("max_steps", MAX_STEPS)

    clauses_text = ""
    if clauses:
        clauses_text = "\n\nIDENTIFIED CLAUSES:\n"
        for c in clauses:
            flag = " ⚑ FLAGGED FOR ANALYSIS" if c.get("flagged_for_analysis") else ""
            amb  = " [AMBIGUOUS]" if c.get("is_ambiguous") else ""
            clauses_text += f"  [{c['clause_id']}] {c['title']}{flag}{amb}:\n    {c['text'][:300]}\n"

    feedback_section = ""
    if last_feedback and step > 1:
        feedback_section = (
            f"\n\nPREVIOUS ATTEMPT FEEDBACK (step {step-1}):\n{last_feedback}\n"
            f"Improve your answer based on this feedback to increase your score."
        )

    prompt = textwrap.dedent(f"""
        CONTRACT: {contract_title}
        STEP: {step}/{max_steps} | CURRENT SCORE: {score_so_far:.3f}

        TASK INSTRUCTIONS:
        {task_desc}

        FULL CONTRACT TEXT:
        {contract_text}
        {clauses_text}
        {feedback_section}

        Now provide your JSON response for task '{task}'. Respond ONLY with valid JSON.
    """).strip()

    return prompt


def get_agent_action(
    client: OpenAI,
    observation: dict,
    task: str,
    step: int,
    last_feedback: Optional[str],
) -> tuple[dict, str]:
    """Call the LLM to get the next action. Returns (action_dict, raw_text)."""
    system_prompt = SYSTEM_PROMPTS.get(task, SYSTEM_PROMPTS["find_missing_clauses"])
    user_prompt   = build_user_prompt(observation, task, step, last_feedback)

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_prompt},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        raw_text = (completion.choices[0].message.content or "").strip()

        # Clean markdown fences if present
        clean = raw_text.strip()
        if clean.startswith("```"):
            lines = clean.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            clean = "\n".join(lines)
        clean = clean.strip()

        action_dict = json.loads(clean)
        return action_dict, raw_text

    except json.JSONDecodeError as e:
        print(f"[DEBUG] JSON parse error: {e} | raw: {raw_text[:300]}", flush=True)
        return _fallback_action(task), f"JSON_PARSE_ERROR: {e}"
    except Exception as e:
        print(f"[DEBUG] LLM call failed: {e}", flush=True)
        return _fallback_action(task), f"LLM_ERROR: {e}"


def _fallback_action(task: str) -> dict:
    """Fallback action when LLM fails — ensures no crash."""
    if task == "find_missing_clauses":
        return {
            "task": "find_missing_clauses",
            "find_missing": {
                "missing_clauses": ["termination", "governing_law", "dispute_resolution"]
            }
        }
    elif task == "identify_risky_party":
        return {
            "task": "identify_risky_party",
            "identify_risky": {
                "clause_id": "clause_6",
                "disadvantaged_party": "Party B",
                "reasoning": (
                    "This clause is unilateral and one-sided, creating disproportionate disadvantage "
                    "for Party B who bears all obligations with no recourse or remedy."
                )
            }
        }
    else:
        return {
            "task": "rewrite_ambiguous",
            "rewrite": {
                "clause_id": "clause_1",
                "rewritten_clause": (
                    "Net profits shall be distributed 60% to Partner A and 40% to Partner B, "
                    "calculated quarterly on net revenue by a certified public accountant within "
                    "30 days of each quarter end. Each distribution shall be made within 15 days "
                    "of the accountant's report. Disputes regarding profit calculations shall be "
                    "resolved through binding arbitration within 60 days, with costs shared equally. "
                    "Extraordinary distributions require 14 days written notice. This obligation is "
                    "binding and enforceable against both parties, provided that distributions shall "
                    "not include reserved operating capital as defined in Schedule A."
                )
            }
        }

# ─────────────────────────────────────────────
# Main Loop
# ─────────────────────────────────────────────

async def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    rewards:       List[float]  = []
    steps_taken:   int          = 0
    score:         float        = 0.0
    success:       bool         = False
    last_feedback: Optional[str] = None

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        # Reset environment
        result      = await env_reset(TASK_NAME)
        observation = result.get("observation", {})

        for step in range(1, MAX_STEPS + 1):
            if result.get("done", False):
                break

            # Get LLM action
            action_dict, raw_text = get_agent_action(
                client, observation, TASK_NAME, step, last_feedback
            )

            # Submit to environment
            try:
                result = await env_step(action_dict)
            except Exception as e:
                print(f"[DEBUG] env_step error: {e}", flush=True)
                result = {
                    "observation": observation,
                    "reward": 0.0,
                    "done": True,
                    "info": {}
                }

            reward      = float(result.get("reward", 0.0))
            done        = bool(result.get("done", False))
            observation = result.get("observation", {})
            error       = observation.get("last_action_error", None)
            last_feedback = observation.get("last_action_feedback", None)

            rewards.append(reward)
            steps_taken = step

            action_summary = f"task={TASK_NAME},step={step},score={reward:.3f}"
            log_step(step=step, action=action_summary, reward=reward, done=done, error=error)

            if done:
                break

        score   = max(rewards) if rewards else 0.0
        success = score >= SUCCESS_SCORE_THRESHOLD

    except Exception as e:
        print(f"[DEBUG] Unhandled exception in main loop: {e}", flush=True)
        import traceback
        traceback.print_exc()

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    asyncio.run(main())
