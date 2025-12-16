from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.controlDeCalidad import (
    ControlCalidadCreate,
    ControlCalidadResponse,
    ControlCalidadUpdate,
)
from app.services import control_calidad_service

router = APIRouter(prefix="/controles-calidad", tags=["controles-calidad"])


@router.post("", response_model=ControlCalidadResponse, summary="Crear control de calidad")
def crear_control_de_calidad(
    payload: ControlCalidadCreate, db: Session = Depends(get_db)
):
    return control_calidad_service.crear_control_calidad(payload, db)


@router.get("", response_model=List[ControlCalidadResponse], summary="Listar controles de calidad")
def listar_controles_de_calidad(db: Session = Depends(get_db)):
    return control_calidad_service.listar_controles_calidad(db)


@router.get(
    "/{control_id}",
    response_model=ControlCalidadResponse,
    summary="Obtener control de calidad por id",
)
def obtener_control_de_calidad(control_id: int, db: Session = Depends(get_db)):
    control = control_calidad_service.obtener_control_calidad(control_id, db)
    if not control:
        raise HTTPException(status_code=404, detail="Control de calidad no encontrado")
    return control


@router.put(
    "/{control_id}",
    response_model=ControlCalidadResponse,
    summary="Actualizar control de calidad",
)
def actualizar_control_de_calidad(
    control_id: int, payload: ControlCalidadUpdate, db: Session = Depends(get_db)
):
    control = control_calidad_service.obtener_control_calidad(control_id, db)
    if not control:
        raise HTTPException(status_code=404, detail="Control de calidad no encontrado")

    return control_calidad_service.actualizar_control_calidad_service(
        control_id, payload, db
    )


@router.patch(
    "/{control_id}",
    response_model=ControlCalidadResponse,
    summary="Actualizar parcialmente el control de calidad",
)
def parchar_control_de_calidad(
    control_id: int, payload: ControlCalidadUpdate, db: Session = Depends(get_db)
):
    control = control_calidad_service.obtener_control_calidad(control_id, db)
    if not control:
        raise HTTPException(status_code=404, detail="Control de calidad no encontrado")

    return control_calidad_service.actualizar_control_calidad_parcial(
        control_id, payload, db
    )


@router.delete(
    "/{control_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar control de calidad",
)
def eliminar_control_de_calidad(control_id: int, db: Session = Depends(get_db)):
    control = control_calidad_service.obtener_control_calidad(control_id, db)
    if not control:
        raise HTTPException(status_code=404, detail="Control de calidad no encontrado")

    control_calidad_service.eliminar_control_calidad(control_id, db)
