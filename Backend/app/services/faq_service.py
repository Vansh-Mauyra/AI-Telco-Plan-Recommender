import json
from app.db.database import fetch_all
from ..bedrock_client import call_bedrock_claude
from ..prompts import FAQ_SYSTEM, FAQ_USER_TEMPLATE

def get_faq_context(message: str) -> dict:
    # naive: search plan_name by ILIKE
    sql = """
    SELECT plan_id, plan_name, monthly_fee, data_gb, daily_data_gb,
           voice_minutes, sms_count, roaming_included,
           international_roaming, network_type
    FROM telco_plan
    WHERE plan_name ILIKE '%' || %s || '%'
       OR plan_code ILIKE '%' || %s || '%'
    LIMIT 10
    """
    plans = fetch_all(sql, (message, message))
    return {"plans": plans}

def build_faq_answer(message: str, context: dict) -> str:
    user_prompt = FAQ_USER_TEMPLATE.format(
        user_message=message,
        context_json=json.dumps(context, indent=2),
    )
    return call_bedrock_claude(FAQ_SYSTEM, user_prompt)

def handle_faq(message: str) -> dict:
    context = get_faq_context(message)
    answer = build_faq_answer(message, context)
    return {
        "type": "FAQ",
        "answer": answer,
        "plans": context.get("plans", []),
    }
