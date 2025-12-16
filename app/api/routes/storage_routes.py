from fastapi import APIRouter, HTTPException

from app.schemas.storage import PresignedPutRequest, PresignedUrlResponse
from app.services import minio_service


router = APIRouter(tags=["Archivos"])


@router.post("/generarPutURL", response_model=PresignedUrlResponse)
def generar_put_url(payload: PresignedPutRequest):
    try:
        url = minio_service.get_presigned_put_url(payload.file)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    return PresignedUrlResponse(url=url)
