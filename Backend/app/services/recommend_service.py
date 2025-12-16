import json
from typing import List, Optional

from app.db.database import fetch_all
from app.db.queries import (
    get_customer_profile,
    fetch_usage_summary,
    fetch_candidate_plans,
)
from app.services.scoring import score_plan
from app.bedrock_client import call_bedrock_claude
from ..prompts import (
    CONSTRAINT_EXTRACTOR_SYSTEM,
    CONSTRAINT_EXTRACTOR_USER_TEMPLATE,
    RECOMMENDATION_SYSTEM,
    RECOMMENDATION_USER_TEMPLATE,
)


# -------------------------------------------------
# 1. Extract constraints from user message (Claude)
# -------------------------------------------------
def extract_constraints(message: str) -> dict:
    user_prompt = CONSTRAINT_EXTRACTOR_USER_TEMPLATE.format(message=message)

    raw = call_bedrock_claude(
        CONSTRAINT_EXTRACTOR_SYSTEM,
        user_prompt,
        max_tokens=200
    )

    try:
        return json.loads(raw)
    except Exception:
        return {
            "budget": None,
            "min_data_gb_per_month": None,
            "min_data_gb_per_day": None,
            "min_voice_minutes": None,
            "needs_roaming": False,
            "needs_international_roaming": False,
            "priority": None,
            "network_type": None,
            "validity_days": None,
            "validity_preference": None
        }


# -------------------------------------------------
# 2. DB filtering using constraints
# -------------------------------------------------
def query_plans_by_constraints(constraints: dict, limit: int = 20) -> List[dict]:
    return fetch_candidate_plans(
        budget=constraints.get("budget") or 999999,
        min_data=constraints.get("min_data_gb_per_month") or 0,
        min_voice=constraints.get("min_voice_minutes") or 0,
        needs_roaming=constraints.get("needs_roaming", False),
        needs_int_roaming=constraints.get("needs_international_roaming", False),
        network_type=constraints.get("network_type"),
        validity_days=constraints.get("validity_days"),
        limit=limit
    )


# -------------------------------------------------
# 3. Claude explanation
# -------------------------------------------------
def build_recommendation_answer(
    user_message: str,
    constraints: dict,
    plans: List[dict]
) -> str:

    user_prompt = RECOMMENDATION_USER_TEMPLATE.format(
        user_message=user_message,
        constraints_json=json.dumps(constraints, indent=2),
        plans_json=json.dumps(plans, indent=2),
    )

    return call_bedrock_claude(
        RECOMMENDATION_SYSTEM,
        user_prompt
    )


# -------------------------------------------------
# 4. MAIN ENTRY POINT
# -------------------------------------------------
def handle_recommendation(
    message: str,
    user_id: Optional[str] = None,
    max_results: int = 5
) -> dict:
    """
    Hybrid AI + Rules-based recommendation flow

    Flow:
    1. Extract constraints (Claude)
    2. Filter plans from DB
    3. If user_id → usage-based scoring
    4. Claude explains final results
    """

    # Step 1: Extract constraints
    constraints = extract_constraints(message)
    VALIDITY_MAP = {
    "short": 28,
    "medium": 56,
    "long": 84,
    "annual": 365
    }

    DATA_PREFERENCE_MAP = {
    "high": 120,
    "medium": 90,        
    "low": 30
    }

    if constraints.get("validity_days") is None:
        pref = constraints.get("validity_preference")
        if pref in VALIDITY_MAP:
            constraints["validity_days"] = VALIDITY_MAP[pref]
    
    if constraints.get("min_data_gb_per_month") is None:
        data_pref = constraints.get("data_preference")
        if data_pref in DATA_PREFERENCE_MAP:
            constraints["min_data_gb_per_month"] = DATA_PREFERENCE_MAP[data_pref]


    # Step 2: Fetch candidate plans
    plans = query_plans_by_constraints(
        constraints,
        limit=max_results * 3
    )

    if not plans:
        return {
            "type": "RECOMMENDATION",
            "answer": "Sorry, I couldn’t find any plans matching your needs.",
            "plans": []
        }

    # Step 3: Personalization (usage_history aware)
    if user_id:
        user = get_customer_profile(user_id)
        usage = fetch_usage_summary(user_id)

        if user and usage:
            user_context = {
                **user,
                **usage
            }

            for plan in plans:
                plan["score"] = score_plan(plan, user_context)

            plans.sort(key=lambda x: x["score"], reverse=True)

    # Final shortlist
    final_plans = plans[:max_results]

    # Step 4: Claude explanation (NO decision making)
    answer = build_recommendation_answer(
        message,
        constraints,
        final_plans
    )

    return {
        "type": "RECOMMENDATION",
        "answer": answer,
        "plans": final_plans
    }
