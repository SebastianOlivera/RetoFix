from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.models.control_calidad import ControlDeCalidad
from app.repositories import control_calidad_repository
from app.schemas.controlDeCalidad import (
    ControlCalidadCreate,
    ControlCalidadUpdate,
)


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def crear_control_calidad(payload: ControlCalidadCreate, db: Session) -> ControlDeCalidad:
    existente = control_calidad_repository.get_control_por_lote(payload.loteid, db)
    if existente:
        return existente

    return control_calidad_repository.crear_control_calidad(
        loteid=payload.loteid,
        pdfurl=payload.pdfurl,
        resumenresultados=payload.resumenresultados,
        responsable=payload.responsable,
        creado_en=_now_utc(),
        db=db,
    )


def actualizar_control_calidad_service(
    control_id: int, payload: ControlCalidadUpdate, db: Session
) -> Optional[ControlDeCalidad]:
    control = control_calidad_repository.get_control(control_id, db)
    if not control:
        return None

    return control_calidad_repository.actualizar_control_calidad(
        control,
        loteid=payload.loteid,
        pdfurl=payload.pdfurl,
        resumenresultados=payload.resumenresultados,
        responsable=payload.responsable,
        actualizado_en=_now_utc(),
        db=db,
    )


def actualizar_control_calidad_parcial(
    control_id: int, payload: ControlCalidadUpdate, db: Session
) -> Optional[ControlDeCalidad]:
    return actualizar_control_calidad_service(control_id, payload, db)


def eliminar_control_calidad(control_id: int, db: Session) -> None:
    control = control_calidad_repository.get_control(control_id, db)
    if not control:
        return
    control_calidad_repository.eliminar_control_calidad_repo(control, db)
