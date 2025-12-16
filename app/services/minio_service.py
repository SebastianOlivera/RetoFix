import os
from datetime import timedelta
from typing import Optional

from minio import Minio

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio.reto-ucu.net")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "golanduser")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", 'g0l4ndu$er!"#')
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "goland-bucket")
MINIO_SECURE = os.getenv("MINIO_SECURE", "true").lower() == "true"

_client: Optional[Minio] = None


def _get_client() -> Minio:
    global _client
    if _client is None:
        _client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE,
        )
    return _client


def get_presigned_put_url(object_name: str, expires_minutes: int = 30) -> str:
    client = _get_client()
    return client.presigned_put_object(
        MINIO_BUCKET,
        object_name,
        expires=timedelta(minutes=expires_minutes),
    )


def get_presigned_get_url(object_name: str, expires_minutes: int = 5) -> str:
    client = _get_client()
    return client.presigned_get_object(
        MINIO_BUCKET,
        object_name,
        expires=timedelta(minutes=expires_minutes),
    )
