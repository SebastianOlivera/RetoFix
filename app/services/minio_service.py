import os
from datetime import timedelta
from typing import Optional

from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error

load_dotenv()


def _get_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Falta la variable de entorno requerida: {name}")
    return value


def _client() -> Minio:
    return Minio(
        _get_env("MINIO_ENDPOINT"),
        access_key=_get_env("MINIO_ACCESS_KEY"),
        secret_key=_get_env("MINIO_SECRET_KEY"),
        secure=True,
    )


def _bucket_name() -> str:
    return _get_env("MINIO_BUCKET")


def get_presigned_put_url(
    object_name: str, expires_minutes: int = 30, bucket: Optional[str] = None
) -> str:
    if not object_name:
        raise ValueError("El nombre del archivo es requerido para generar la URL de carga")

    target_bucket = bucket or _bucket_name()

    try:
        return _client().presigned_put_object(
            target_bucket,
            object_name,
            expires=timedelta(minutes=expires_minutes),
        )
    except S3Error as exc:
        raise RuntimeError(f"Error generando presigned URL: {exc}") from exc


def get_presigned_get_url(
    object_name: str, expires_minutes: int = 5, bucket: Optional[str] = None
) -> str:
    if not object_name:
        raise ValueError("El nombre del archivo es requerido para generar la URL firmada")

    target_bucket = bucket or _bucket_name()

    try:
        return _client().presigned_get_object(
            target_bucket,
            object_name,
            expires=timedelta(minutes=expires_minutes),
        )
    except S3Error as exc:
        raise RuntimeError(f"No se pudo generar la URL firmada: {exc}") from exc
