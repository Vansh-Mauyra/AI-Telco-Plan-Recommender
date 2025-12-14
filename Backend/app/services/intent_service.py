from ..bedrock_client import call_bedrock_claude
from ..prompts import INTENT_CLASSIFIER_SYSTEM, INTENT_CLASSIFIER_USER_TEMPLATE

def classify_intent(message: str) -> str:
    user_prompt = INTENT_CLASSIFIER_USER_TEMPLATE.format(message=message)
    result = call_bedrock_claude(INTENT_CLASSIFIER_SYSTEM, user_prompt, max_tokens=10)
    label = result.strip().upper()
    if label not in ("FAQ", "RECOMMENDATION", "COMPARISON"):
        return "FAQ"
    return label