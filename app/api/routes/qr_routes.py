from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services import producto_lote_service as svc

router = APIRouter(prefix="/qr", tags=["QR"])


@router.get("/productos/{producto_id}/lotes/{lote_id}")
def obtener_payload_qr(producto_id: int, lote_id: int, db: Session = Depends(get_db)):
    return svc.payload_qr(db, producto_id, lote_id)
