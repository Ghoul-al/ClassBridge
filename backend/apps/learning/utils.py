import boto3
from django.conf import settings
from botocore.exceptions import ClientError
import uuid
from .models import FileUpload

def get_minio_client():
    return boto3.client(
        's3',
        endpoint_url=f"http{'s' if settings.MINIO_SECURE else ''}://{settings.MINIO_ENDPOINT}",
        aws_access_key_id=settings.MINIO_ACCESS_KEY,
        aws_secret_access_key=settings.MINIO_SECRET_KEY,
        region_name='us-east-1',  # MinIO doesn't use regions, but boto3 requires it
    )

def upload_file_to_minio(file_obj, file_name, school_id, user):
    client = get_minio_client()
    bucket_name = settings.MINIO_BUCKET_NAME

    # Ensure bucket exists
    try:
        client.head_bucket(Bucket=bucket_name)
    except ClientError:
        client.create_bucket(Bucket=bucket_name)

    # Generate unique key
    file_extension = file_name.split('.')[-1] if '.' in file_name else ''
    minio_key = f"{school_id}/{uuid.uuid4()}.{file_extension}"

    # Upload file
    client.upload_fileobj(file_obj, bucket_name, minio_key)

    # Generate public URL (assuming MinIO is accessible)
    file_url = f"http{'s' if settings.MINIO_SECURE else ''}://{settings.MINIO_ENDPOINT}/{bucket_name}/{minio_key}"

    # Save metadata
    file_upload = FileUpload.objects.create(
        school_id=school_id,
        uploaded_by=user,
        file_name=file_name,
        file_size=file_obj.size,
        mime_type=file_obj.content_type,
        minio_key=minio_key,
        file_url=file_url,
    )

    return file_upload

def delete_file_from_minio(minio_key):
    client = get_minio_client()
    bucket_name = settings.MINIO_BUCKET_NAME
    client.delete_object(Bucket=bucket_name, Key=minio_key)