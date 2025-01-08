import boto3
import os

endpoint = os.environ.get('S3ENDPOINT')
s3user = os.environ.get('S3USER')
s3pass = os.environ.get('S3PASSWORD')

s3_client = boto3.client(
    "s3",
    endpoint_url=endpoint,
    aws_access_key_id=s3user,
    aws_secret_access_key=s3pass
)