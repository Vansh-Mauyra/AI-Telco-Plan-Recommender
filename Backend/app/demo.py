import os
import boto3
print("AWS_ACCESS_KEY_ID:", os.getenv("AWS_ACCESS_KEY_ID"))
print("AWS_SECRET_ACCESS_KEY:", os.getenv("AWS_SECRET_ACCESS_KEY"))
print("AWS_DEFAULT_REGION:", os.getenv("AWS_DEFAULT_REGION"))
print(boto3.client("sts").get_caller_identity())
