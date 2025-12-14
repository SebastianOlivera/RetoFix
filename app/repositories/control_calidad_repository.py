from datetime import datetime

from sqlalchemy.orm import Session

from app.models import ControlDeCalidad


def get_control(control_id: int, db: Session) -> ControlDeCalidad | None:
    return db.query(ControlDeCalidad).filter(ControlDeCalidad.id == control_id).first()


def get_control_por_lote(lote_id: int, db: Session) -> ControlDeCalidad | None:
    return db.query(ControlDeCalidad).filter(ControlDeCalidad.lote_id == lote_id).first()


def crear_control_calidad(
    lote_id: int,
    estado: str,
    observaciones: str | None,
    inspector: str | None,
    fecha_inspeccion: datetime,
    db: Session,
) -> ControlDeCalidad:
    control = ControlDeCalidad(
        lote_id=lote_id,
        estado=estado,
        observaciones=observaciones,
        inspector=inspector,
        fecha_inspeccion=fecha_inspeccion,
    )
    db.add(control)
    db.flush()
    return control


def actualizar_control_calidad(
    control: ControlDeCalidad,
    estado: str | None,
    observaciones: str | None,
    inspector: str | None,
    fecha_inspeccion: datetime | None,
    db: Session,
) -> ControlDeCalidad:
    if estado is not None:
        control.estado = estado
    if observaciones is not None:
        control.observaciones = observaciones
    if inspector is not None:
        control.inspector = inspector
    if fecha_inspeccion is not None:
        control.fecha_inspeccion = fecha_inspeccion

    db.flush()
    return control


def eliminar_control_calidad_repo(control: ControlDeCalidad, db: Session) -> None:
    db.delete(control)
    db.flush()
