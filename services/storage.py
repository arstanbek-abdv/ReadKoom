from datetime import timedelta
from dotenv import load_dotenv
from botocore.config import Config
import uuid
import boto3
import os 

from config.settings import (
    AWS_S3_REGION_NAME,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_STORAGE_BUCKET_NAME,
    DOWNLOAD_EXPIRES,
    UPLOAD_EXPIRES,
    MAX_UPLOAD_BYTES
)

s3_client = boto3.client(
    's3',
    aws_s3_region_name = AWS_S3_REGION_NAME,
    aws_access_key_id = AWS_ACCESS_KEY_ID,
    aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    config = Config(signature_version = 's3v4')
)

def generate_file_key(user_id: int) -> str:
    file_key = uuid.uuid4().hex
    return f"publications/{user_id}/{file_key}"


def upload_url(file_key: str) -> str:
    return s3_client.generate_presigned_post(
        Bucket = AWS_STORAGE_BUCKET_NAME,
        Key = file_key,
        Conditions = [
            ["content-length-range", 1, MAX_UPLOAD_BYTES],
            ["starts-with", "$Content-Type", ""]
        ],
        ExpiresIn = UPLOAD_EXPIRES
    )

def download_url(file_key: str, mime_type: str, file_name: str) -> str:
    return s3_client.generate_presigned_url(
        ClientMethod = 'get_object',
        Params = {
            'Bucket': AWS_STORAGE_BUCKET_NAME,
            'Key': file_key,
            'ResponseContentType': mime_type,
            'ResponseContentDisposition': f'attachment; filename = {file_name}'
        },
        ExpiresIn = DOWNLOAD_EXPIRES
    )