import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Telco AI Recommender"
    DB_DSN: str = os.getenv(
        "DB_DSN",
        "dbname=telco_ai user=postgres password=9879368530V@n host=localhost port=5432"
    )

    AWS_REGION: str = os.getenv("AWS_REGION", "ap-southeast-1")
    BEDROCK_MODEL_ID: str = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")

settings = Settings()