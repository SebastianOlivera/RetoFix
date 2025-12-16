from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services import minio_service

router = APIRouter(tags=["MinIO"])


class PresignedPutRequest(BaseModel):
    file: str


class PresignedPutResponse(BaseModel):
    url: str


@router.post("/generarPutURL", response_model=PresignedPutResponse)
def generar_put_url(payload: PresignedPutRequest):
    try:
        url = minio_service.get_presigned_put_url(payload.file)
    except Exception as exc:  # pragma: no cover - defensive
        raise HTTPException(status_code=500, detail="No se pudo generar la URL") from exc
    return PresignedPutResponse(url=url)
