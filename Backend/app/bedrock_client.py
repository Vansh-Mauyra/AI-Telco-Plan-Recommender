import json
import boto3
from app.config import settings
import botocore.config

config = botocore.config.Config(
    read_timeout=30,
    connect_timeout=10,
    retries={"max_attempts": 2}
)

def get_bedrock_client():
    """
    Lazily create Bedrock client.
    This MUST NOT run at import time.
    """
    return boto3.client(
        "bedrock-runtime",
        region_name=settings.AWS_REGION,
        verify=False,
        config=config
    )

def call_bedrock_claude(system_prompt: str, user_prompt: str, max_tokens: int = 800):
    bedrock = get_bedrock_client()

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": 0.2,
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt
                    }
                ]
            }
        ]
    }

    response = bedrock.invoke_model(
        modelId=settings.BEDROCK_MODEL_ID,
        body=json.dumps(body)
    )

    response_body = json.loads(response["body"].read())

    for block in response_body.get("content", []):
        if block.get("type") == "text":
            return block.get("text", "")

    return ""
