"""
Graders for all 3 tasks.
Each grader returns a float score in [0.0, 1.0] with partial credit.

- Task 1: find_missing_clauses   → score = correct_found / total_missing (penalty for false positives)
- Task 2: identify_risky_party   → binary (1.0) + reasoning quality bonus (0.0–0.2, capped at 1.0)
- Task 3: rewrite_ambiguous      → multi-criteria: length, specificity, legal vocab, carve-outs, enforceability
"""

import re
from typing import List, Dict, Any, Tuple

from models import (
    ContractAction, FindMissingClausesAction, IdentifyRiskyPartyAction,
    RewriteAmbiguousAction, ClauseType, Party, TaskName
)


# ─────────────────────────────────────────────
# Task 1 Grader: Find Missing Clauses
# ─────────────────────────────────────────────

def grade_find_missing_clauses(
    action: FindMissingClausesAction,
    contract_data: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Score = (correctly identified missing clauses) / (total missing clauses)
    Penalty: -0.1 per false positive (clause agent says is missing but is present), min 0.0
    """
    expected_missing: List[str] = contract_data["missing_clauses"]
    submitted: List[str] = [c.value for c in action.missing_clauses]

    submitted_set = set(submitted)
    expected_set  = set(expected_missing)

    true_positives  = submitted_set & expected_set
    false_positives = submitted_set - expected_set
    false_negatives = expected_set - submitted_set

    if not expected_set:
        return 1.0, "✅ Contract has no missing clauses. Perfect score."

    base_score = len(true_positives) / len(expected_set)
    penalty    = len(false_positives) * 0.1
    score      = max(0.0, min(1.0, base_score - penalty))

    feedback_parts = []
    if true_positives:
        feedback_parts.append(f"✅ Correctly identified: {', '.join(sorted(true_positives))}")
    if false_negatives:
        feedback_parts.append(f"❌ Missed: {', '.join(sorted(false_negatives))}")
    if false_positives:
        feedback_parts.append(f"⚠️ False positives (present in contract): {', '.join(sorted(false_positives))}")

    feedback = " | ".join(feedback_parts) if feedback_parts else "No clauses submitted."
    return round(score, 3), feedback


# ─────────────────────────────────────────────
# Task 2 Grader: Identify Risky Party
# ─────────────────────────────────────────────

def grade_identify_risky_party(
    action: IdentifyRiskyPartyAction,
    contract_data: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Base score: 1.0 if correct party identified, 0.0 if wrong.
    Reasoning bonus: up to +0.2 if reasoning mentions key legal terms (capped at 1.0).
    """
    target_clause_id = contract_data["target_clause_id"]
    target_answer    = contract_data["target_answer"]

    if action.clause_id != target_clause_id:
        return 0.0, f"❌ Wrong clause analyzed. Expected: {target_clause_id}, got: {action.clause_id}."

    party_correct = (action.disadvantaged_party.value == target_answer)
    base_score    = 1.0 if party_correct else 0.0

    reasoning_lower = action.reasoning.lower()
    quality_keywords = [
        "unilateral", "one-sided", "disproportionate", "unfair", "no recourse",
        "imbalance", "leverage", "disadvantage", "rights", "obligation",
        "sole discretion", "arbitrary", "without cause", "without notice",
        "bears all", "all risk", "no right", "no remedy",
    ]
    keyword_hits    = sum(1 for kw in quality_keywords if kw in reasoning_lower)
    reasoning_bonus = min(0.2, keyword_hits * 0.05)

    score = min(1.0, base_score + reasoning_bonus)

    if party_correct:
        feedback = (
            f"✅ Correct! {target_answer} is disadvantaged. "
            f"Reasoning quality bonus: +{reasoning_bonus:.2f} "
            f"({keyword_hits} legal keywords found)"
        )
    else:
        feedback = (
            f"❌ Incorrect. You said '{action.disadvantaged_party.value}' "
            f"but the answer is '{target_answer}'. "
            f"Hint: Look at who bears all the risk/cost in clause {target_clause_id}."
        )

    return round(score, 3), feedback


# ─────────────────────────────────────────────
# Task 3 Grader: Rewrite Ambiguous Clause
# ─────────────────────────────────────────────

def grade_rewrite_ambiguous(
    action: RewriteAmbiguousAction,
    contract_data: Dict[str, Any]
) -> Tuple[float, str]:
    """
    Score based on weighted presence of required legal elements:
    1. Length check (min_word_count)             → 0.10
    2. Specificity (numbers, dates, durations)   → 0.30
    3. Defined terms / legal vocabulary          → 0.30
    4. Carve-outs / exceptions present           → 0.20
    5. Enforceability markers                    → 0.10
    """
    target_clause_id = contract_data["target_clause_id"]
    eval_keywords    = contract_data["evaluation_keywords"]
    min_words        = contract_data["min_word_count"]

    if action.clause_id != target_clause_id:
        return 0.0, f"❌ Wrong clause. Expected {target_clause_id}, got {action.clause_id}."

    rewrite    = action.rewritten_clause.lower()
    word_count = len(action.rewritten_clause.split())
    score_components = {}
    feedback_parts   = []

    # 1. Length check
    if word_count >= min_words:
        score_components["length"] = 0.10
        feedback_parts.append(f"✅ Good length ({word_count} words)")
    else:
        score_components["length"] = round(word_count / min_words * 0.10, 3)
        feedback_parts.append(f"⚠️ Too brief ({word_count}/{min_words} words needed)")

    # 2. Specificity: numbers, percentages, durations
    specificity_patterns = [
        r'\d+\s*%',
        r'\d+\s*(year|month|day|week)',
        r'\$\s*\d+',
        r'\d{1,2}/\d{1,2}/\d{2,4}',
        r'(january|february|march|april|may|june|july|august|september|october|november|december)',
        r'net\s*\d+',
        r'\d+\s*days',
    ]
    specificity_hits = sum(1 for pat in specificity_patterns if re.search(pat, rewrite))
    specificity_score = min(0.30, specificity_hits * 0.10)
    score_components["specificity"] = specificity_score
    if specificity_hits >= 2:
        feedback_parts.append(f"✅ Good specificity ({specificity_hits} numeric/date patterns found)")
    elif specificity_hits == 1:
        feedback_parts.append(f"⚠️ Some specificity — add more percentages, durations, or amounts")
    else:
        feedback_parts.append(f"❌ No specific figures — add percentages, durations, dollar amounts")

    # 3. Legal vocabulary from eval_keywords
    keyword_hits = [kw for kw in eval_keywords if kw.lower() in rewrite]
    vocab_score  = min(0.30, len(keyword_hits) * 0.05)
    score_components["legal_vocab"] = vocab_score
    if keyword_hits:
        feedback_parts.append(f"✅ Legal terms found: {', '.join(keyword_hits[:5])}")
    else:
        feedback_parts.append(f"❌ Missing legal terminology — use domain-specific language")

    # 4. Carve-outs / exceptions
    carveout_terms = [
        "except", "excluding", "provided that", "notwithstanding",
        "unless", "shall not include", "does not include",
        "publicly available", "public domain", "prior to",
        "required by law", "court order", "except as required",
    ]
    carveout_hits = sum(1 for t in carveout_terms if t in rewrite)
    carveout_score = min(0.20, carveout_hits * 0.07)
    score_components["carveouts"] = carveout_score
    if carveout_hits >= 2:
        feedback_parts.append(f"✅ Carve-outs/exceptions present ({carveout_hits} found)")
    elif carveout_hits == 1:
        feedback_parts.append(f"⚠️ Limited carve-outs — add more exceptions")
    else:
        feedback_parts.append(f"⚠️ No carve-outs — consider adding exceptions (public domain, court orders)")

    # 5. Enforceability markers
    enforce_terms = [
        "in writing", "written notice", "shall", "must", "obligated",
        "binding", "enforceable", "agrees to", "warrants", "hereby",
    ]
    enforce_hits  = sum(1 for t in enforce_terms if t in rewrite)
    enforce_score = min(0.10, enforce_hits * 0.03)
    score_components["enforceability"] = enforce_score
    if enforce_hits >= 2:
        feedback_parts.append(f"✅ Enforceability markers present")
    else:
        feedback_parts.append(f"⚠️ Add formal enforceability language ('shall', 'in writing', 'binding')")

    total_score = sum(score_components.values())
    total_score = min(1.0, max(0.0, total_score))

    feedback = " | ".join(feedback_parts)
    return round(total_score, 3), feedback


# ─────────────────────────────────────────────
# Unified Grade Entry Point
# ─────────────────────────────────────────────

def grade_action(
    action: ContractAction,
    contract_data: Dict[str, Any],
    task: TaskName
) -> Tuple[float, str]:
    """Route to the correct grader based on task."""

    if task == TaskName.FIND_MISSING_CLAUSES:
        if action.find_missing is None:
            return 0.0, "❌ No find_missing action provided for this task."
        return grade_find_missing_clauses(action.find_missing, contract_data)

    elif task == TaskName.IDENTIFY_RISKY_PARTY:
        if action.identify_risky is None:
            return 0.0, "❌ No identify_risky action provided for this task."
        return grade_identify_risky_party(action.identify_risky, contract_data)

    elif task == TaskName.REWRITE_AMBIGUOUS:
        if action.rewrite is None:
            return 0.0, "❌ No rewrite action provided for this task."
        return grade_rewrite_ambiguous(action.rewrite, contract_data)

    else:
        return 0.0, f"❌ Unknown task: {task}"
