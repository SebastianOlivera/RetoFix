from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.lote import LoteCreate, LoteUpdate, LoteResponse
from app.services import lote_service

router = APIRouter(prefix="/lotes", tags=["Lotes"])


@router.post("/", response_model=LoteResponse, status_code=status.HTTP_201_CREATED)
def crear_lote(payload: LoteCreate, db: Session = Depends(get_db)):
    return lote_service.create_Lote(db, payload)


@router.get("/", response_model=List[LoteResponse])
def listar_lotes(db: Session = Depends(get_db)):
    return lote_service.get_lotes(db)



@router.get("/{loteid}", response_model=LoteResponse)
def obtener_lote(loteid: int, db: Session = Depends(get_db)):
    lote = lote_service.get_lote_by_id(db, loteid)
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return lote

@router.put("/{loteid}", response_model=LoteResponse, summary="Actualizar lote completo (PUT)")
def actualizar_lote_put(loteid: int, payload: LoteCreate, db: Session = Depends(get_db)):
    lote = lote_service.get_lote_by_id(db, loteid)
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")

    # PUT = reemplazo total (lo que no mandes, queda None)
    lote.campoid = payload.campoid
    lote.fechasiembra = payload.fechasiembra
    lote.fechacosecha = payload.fechacosecha
    lote.fechaprocesamiento = payload.fechaprocesamiento
    lote.fechavencimiento = payload.fechavencimiento

    db.commit()
    db.refresh(lote)
    return lote


@router.patch("/{loteid}", response_model=LoteResponse)
def actualizar_lote_patch(loteid: int, payload: LoteUpdate, db: Session = Depends(get_db)):
    lote = lote_service.get_lote_by_id(db, loteid)
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return lote_service.update_lote(db, lote, payload)


@router.delete("/{loteid}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_lote(loteid: int, db: Session = Depends(get_db)):
    lote = lote_service.get_lote_by_id(db, loteid)
    if not lote:
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    lote_service.delete_lote(db, lote)
    return
