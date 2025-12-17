from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services import lote_service

router = APIRouter(tags=["publico"])


@router.get("/producto/{qr_id}")
def ver_producto_por_qr(qr_id: str, db: Session = Depends(get_db)):
    return lote_service.ver_producto_por_qr(qr_id, db)


@router.get("/qr-image/{qr_id}")
def obtener_imagen_qr(qr_id: str, db: Session = Depends(get_db)):
    qr_path = lote_service.obtener_imagen_qr(qr_id, db)
    return FileResponse(qr_path, media_type="image/png")
