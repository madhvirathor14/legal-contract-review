import re
from typing import List, Dict, Any
from models import (
    ContractAction,
    FindMissingClausesAction,
    IdentifyRiskyPartyAction,
    RewriteAmbiguousAction,
    TaskName
)

# ─────────────────────────────────────────────
# Task 1: Find Missing Clauses
# ─────────────────────────────────────────────

def grade_find_missing_clauses(
    action: FindMissingClausesAction,
    contract_data: Dict[str, Any]
) -> float:

    expected_missing = contract_data.get("missing_clauses", [])
    submitted = [c.value for c in action.missing_clauses]

    submitted_set = set(submitted)
    expected_set = set(expected_missing)

    if not expected_set:
        return 1.0

    true_positives = submitted_set & expected_set
    false_positives = submitted_set - expected_set

    base_score = len(true_positives) / len(expected_set)
    penalty = len(false_positives) * 0.1

    score = max(0.0, min(1.0, base_score - penalty))
    return round(score, 3)


# ─────────────────────────────────────────────
# Task 2: Identify Risky Party
# ─────────────────────────────────────────────

def grade_identify_risky_party(
    action: IdentifyRiskyPartyAction,
    contract_data: Dict[str, Any]
) -> float:

    target_clause_id = contract_data.get("target_clause_id")
    target_answer = contract_data.get("target_answer")

    if action.clause_id != target_clause_id:
        return 0.0

    party_correct = (action.disadvantaged_party.value == target_answer)
    base_score = 1.0 if party_correct else 0.0

    reasoning = (action.reasoning or "").lower()

    keywords = [
        "unilateral", "one-sided", "unfair", "risk", "obligation",
        "liability", "no recourse", "disadvantage", "imbalance"
    ]

    keyword_hits = sum(1 for k in keywords if k in reasoning)
    bonus = min(0.2, keyword_hits * 0.05)

    return round(min(1.0, base_score + bonus), 3)


# ─────────────────────────────────────────────
# Task 3: Rewrite Ambiguous Clause
# ─────────────────────────────────────────────

def grade_rewrite_ambiguous(
    action: RewriteAmbiguousAction,
    contract_data: Dict[str, Any]
) -> float:

    rewrite = (action.rewritten_clause or "").lower()
    word_count = len(rewrite.split())

    score = 0.0

    # Length
    if word_count >= contract_data.get("min_word_count", 20):
        score += 0.2

    # Specificity (numbers, %, $, durations)
    if re.search(r"\d", rewrite):
        score += 0.2

    if any(x in rewrite for x in ["%", "$", "days", "months", "years"]):
        score += 0.1

    # Legal vocabulary
    if any(x in rewrite for x in ["shall", "must", "binding", "agrees"]):
        score += 0.2

    # Exceptions / carve-outs
    if any(x in rewrite for x in ["except", "unless", "provided that"]):
        score += 0.2

    # Enforceability tone
    if any(x in rewrite for x in ["in writing", "notice", "liable"]):
        score += 0.1

    return round(min(1.0, score), 3)


# ─────────────────────────────────────────────
# Unified Entry Point
# ─────────────────────────────────────────────

def grade_action(
    action: ContractAction,
    contract_data: Dict[str, Any],
    task: TaskName
) -> float:

    try:
        if task == TaskName.FIND_MISSING_CLAUSES:
            if action.find_missing is None:
                return 0.0
            return grade_find_missing_clauses(action.find_missing, contract_data)

        elif task == TaskName.IDENTIFY_RISKY_PARTY:
            if action.identify_risky is None:
                return 0.0
            return grade_identify_risky_party(action.identify_risky, contract_data)

        elif task == TaskName.REWRITE_AMBIGUOUS:
            if action.rewrite is None:
                return 0.0
            return grade_rewrite_ambiguous(action.rewrite, contract_data)

        return 0.0

    except Exception as e:
        print("GRADER ERROR:", str(e))  # debug safety
        return 0.0
