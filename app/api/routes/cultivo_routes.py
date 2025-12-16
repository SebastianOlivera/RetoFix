from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.cultivo import CultivoCreate, CultivoResponse, CultivoUpdate
from app.services import cultivo_service

router = APIRouter(prefix="/cultivos", tags=["cultivos"])


@router.post("", response_model=CultivoResponse, summary="Crear cultivo")
def crear_cultivo(payload: CultivoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo cultivo"""
    return cultivo_service.crear_cultivo(db, payload)


@router.get("", response_model=List[CultivoResponse], summary="Listar todos los cultivos")
def listar_cultivos(db: Session = Depends(get_db)):
    """Obtener lista de todos los cultivos"""
    return cultivo_service.obtener_todos_cultivos(db)


@router.get(
    "/{cultivo_id}", response_model=CultivoResponse, summary="Obtener un cultivo"
)
def obtener_cultivo(cultivo_id: int, db: Session = Depends(get_db)):
    """Obtener un cultivo específico por ID"""
    return cultivo_service.obtener_cultivo(db, cultivo_id)


@router.put(
    "/{cultivo_id}",
    response_model=CultivoResponse,
    summary="Actualizar cultivo completo",
)
def actualizar_cultivo(
    cultivo_id: int, payload: CultivoUpdate, db: Session = Depends(get_db)
):
    """Actualizar todos los campos de un cultivo (PUT)"""
    return cultivo_service.actualizar_cultivo_completo(db, cultivo_id, payload)


@router.patch(
    "/{cultivo_id}",
    response_model=CultivoResponse,
    summary="Actualizar cultivo parcial",
)
def actualizar_parcial_cultivo(
    cultivo_id: int, payload: CultivoUpdate, db: Session = Depends(get_db)
):
    """Actualizar solo los campos proporcionados de un cultivo (PATCH)"""
    return cultivo_service.actualizar_cultivo_parcial(db, cultivo_id, payload)


@router.delete("/{cultivo_id}", summary="Eliminar cultivo")
def eliminar_cultivo(cultivo_id: int, db: Session = Depends(get_db)):
    """Eliminar un cultivo por ID"""
    return cultivo_service.eliminar_cultivo(db, cultivo_id)
