import json
from typing import List
from app.db.database import fetch_all 
from ..bedrock_client import call_bedrock_claude
from ..prompts import COMPARISON_SYSTEM, COMPARISON_USER_TEMPLATE

def get_plans_for_compare(plan_ids: List[int]) -> List[dict]:
    sql = """
    SELECT plan_id, plan_name, monthly_fee, data_gb, daily_data_gb,
           voice_minutes, sms_count, roaming_included,
           international_roaming, network_type
    FROM telco_plan
    WHERE plan_id = ANY(%s)
    """
    return fetch_all(sql, (plan_ids,))

def build_comparison_answer(message: str, plans: List[dict]) -> str:
    user_prompt = COMPARISON_USER_TEMPLATE.format(
        user_message=message,
        plans_json=json.dumps(plans, indent=2),
    )
    return call_bedrock_claude(COMPARISON_SYSTEM, user_prompt)

def handle_comparison(message: str, plan_ids: List[int]) -> dict:
    plans = get_plans_for_compare(plan_ids)
    answer = build_comparison_answer(message, plans)
    return {
        "type": "COMPARISON",
        "answer": answer,
        "plans": plans,
    }