from datetime import timedelta
from dotenv import load_dotenv
import uuid
import boto3
import os 

from config.settings import (
    AWS_S3_ENDPOINT_URL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME,
)

s3 = boto3.client(
    's3',
    endpoint_url=AWS_S3_ENDPOINT_URL,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

def generate_file_key(filename: str, user_id: int) -> str:
    ext = filename.split('.')[-1]
    unique_id = uuid.uuid4().hex
    return f"uploads/{user_id}/{unique_id}.{ext}"


def presigned_upload_url(file_key: str, content_type: str) -> str:
    return s3.generate_presigned_url(
        ClientMethod='put_object',
        Params={
            'Bucket': AWS_STORAGE_BUCKET_NAME,
            'Key': file_key,
            'ContentType': content_type,
        },
        ExpiresIn=3600  # 1 hour
    )

def presigned_download_url(file_key: str) -> str:
    return s3.get_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': AWS_STORAGE_BUCKET_NAME,
            'Key': file_key,
        },
        ExpiresIn=3600  # 1 hour
    )