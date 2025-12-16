from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models.control_calidad import ControlDeCalidad


def get_control(control_id: int, db: Session) -> Optional[ControlDeCalidad]:
    return (
        db.query(ControlDeCalidad)
        .filter(ControlDeCalidad.controlcalidadid == control_id)
        .first()
    )


def listar_controles(db: Session) -> list[ControlDeCalidad]:
    return db.query(ControlDeCalidad).all()


def get_control_por_lote(lote_id: int, db: Session) -> Optional[ControlDeCalidad]:
    return (
        db.query(ControlDeCalidad)
        .filter(ControlDeCalidad.loteid == lote_id)
        .first()
    )


def crear_control_calidad(
    loteid: int,
    pdfurl: Optional[str],
    resumenresultados: Optional[str],
    responsable: Optional[str],
    creado_en: datetime,
    db: Session,
) -> ControlDeCalidad:
    control = ControlDeCalidad(
        loteid=loteid,
        pdfurl=pdfurl,
        resumenresultados=resumenresultados,
        responsable=responsable,
    )
    db.add(control)
    db.commit()
    db.refresh(control)
    return control


def actualizar_control_calidad(
    control: ControlDeCalidad,
    loteid: Optional[int],
    pdfurl: Optional[str],
    resumenresultados: Optional[str],
    responsable: Optional[str],
    actualizado_en: datetime,
    db: Session,
) -> ControlDeCalidad:
    if loteid is not None:
        control.loteid = loteid
    if pdfurl is not None:
        control.pdfurl = pdfurl
    if resumenresultados is not None:
        control.resumenresultados = resumenresultados
    if responsable is not None:
        control.responsable = responsable

    db.commit()
    db.refresh(control)
    return control


def eliminar_control_calidad_repo(control: ControlDeCalidad, db: Session) -> None:
    db.delete(control)
    db.commit()
