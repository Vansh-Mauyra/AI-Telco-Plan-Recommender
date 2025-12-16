from app.bedrock_client import call_bedrock_claude
from ..prompts import GENERIC_SYSTEM_PROMPT


def handle_generic(message: str) -> dict:
    """
    Handles non-recommendation intents like:
    - FAQs
    - General questions
    - Explanations
    - Small talk

    Claude does ALL reasoning here.
    """

    answer = call_bedrock_claude(
        system_prompt=GENERIC_SYSTEM_PROMPT,
        user_prompt=message,
        max_tokens=500
    )

    return {
        "type": "GENERIC",
        "answer": answer,
        "plans": []
    }
