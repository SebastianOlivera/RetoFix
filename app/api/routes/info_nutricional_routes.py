from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.info_nutricional import (
    InfoNutricionalCreate,
    InfoNutricionalUpdate,
    InfoNutricionalResponse,
)
from app.services import info_nutricional_service

router = APIRouter(prefix="/info-nutricional", tags=["Info Nutricional"])


@router.post("", response_model=InfoNutricionalResponse, status_code=status.HTTP_201_CREATED)
def crear_info_nutricional(payload: InfoNutricionalCreate, db: Session = Depends(get_db)):
    return info_nutricional_service.create_info_nutricional(db, payload)


@router.get("", response_model=List[InfoNutricionalResponse])
def listar_info_nutricional(db: Session = Depends(get_db)):
    return info_nutricional_service.get_info_nutricional(db)


@router.get("/{info_id}", response_model=InfoNutricionalResponse)
def obtener_info_nutricional(info_id: int, db: Session = Depends(get_db)):
    info = info_nutricional_service.get_info_nutricional_by_id(db, info_id)
    if not info:
        raise HTTPException(status_code=404, detail="Informacion nutricional no encontrada")
    return info


@router.put("/{info_id}", response_model=InfoNutricionalResponse)
def actualizar_info_nutricional(info_id: int, payload: InfoNutricionalUpdate, db: Session = Depends(get_db)):
    info = info_nutricional_service.get_info_nutricional_by_id(db, info_id)
    if not info:
        raise HTTPException(status_code=404, detail="Informacion nutricional no encontrada")
    return info_nutricional_service.update_info_nutricional(db, info, payload)


@router.patch("/{info_id}", response_model=InfoNutricionalResponse)
def actualizar_info_nutricional_parcial(info_id: int, payload: InfoNutricionalUpdate, db: Session = Depends(get_db)):
    info = info_nutricional_service.get_info_nutricional_by_id(db, info_id)
    if not info:
        raise HTTPException(status_code=404, detail="Informacion nutricional no encontrada")
    return info_nutricional_service.update_info_nutricional(db, info, payload)


@router.delete("/{info_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_info_nutricional(info_id: int, db: Session = Depends(get_db)):
    info = info_nutricional_service.get_info_nutricional_by_id(db, info_id)
    if not info:
        raise HTTPException(status_code=404, detail="Informacion nutricional no encontrada")
    info_nutricional_service.delete_info_nutricional(db, info)
