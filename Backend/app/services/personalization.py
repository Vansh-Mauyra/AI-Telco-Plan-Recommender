# app/services/personalization.py

from app.db.queries import (
    get_customer_profile,
    fetch_candidate_plans,
    fetch_usage_summary
)
from app.services.scoring import score_plan


def personalize_plans(user_id: int, limit: int = 5):
    """
    Returns top N personalized plans based on:
    - customer profile
    - usage history
    - scoring logic
    """

    user = get_customer_profile(user_id)
    if not user:
        return []

    # 🔹 NEW: pull aggregated usage
    usage = fetch_usage_summary(user_id)

    avg_data = usage.get("avg_data_gb") or user.get("avg_monthly_data_gb", 0)
    avg_voice = usage.get("avg_voice_minutes") or user.get("avg_voice_minutes", 0)

    needs_roaming = usage.get("uses_roaming", False)
    needs_int_roaming = usage.get("uses_international", False)

    # 🔹 Fetch candidate plans using better filters
    plans = fetch_candidate_plans(
        budget=user["budget"],
        min_data=avg_data * 1.2,     # safety margin
        min_voice=avg_voice * 1.2,
        needs_roaming=needs_roaming,
        needs_int_roaming=needs_int_roaming
    )

    # 🔹 Score plans
    for p in plans:
        p["score"] = score_plan(
            plan=p,
            user=user,
            usage=usage
        )

    plans.sort(key=lambda x: x["score"], reverse=True)
    return plans[:limit]
