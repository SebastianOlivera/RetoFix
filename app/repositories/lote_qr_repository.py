from typing import Iterable, Optional
from datetime import date

from sqlalchemy.orm import Session

from app.models import CodigoQR, Lote


def create_lote(
    db: Session,
    fechasiembra: Optional[date] = None,
    fechacosecha: Optional[date] = None,
    fechaprocesamiento: Optional[date] = None,
    fechavencimiento: Optional[date] = None,
) -> Lote:
    lote = Lote(
        fechasiembra=fechasiembra,
        fechacosecha=fechacosecha,
        fechaprocesamiento=fechaprocesamiento,
        fechavencimiento=fechavencimiento,
    )
    db.add(lote)
    db.flush()
    return lote


def add_qrs_to_db(qrs: Iterable[CodigoQR], db: Session) -> None:
    db.add_all(list(qrs))
    db.commit()


def add_qr(qr: CodigoQR, db: Session) -> None:
    db.add(qr)


def refresh_lote(lote: Lote, db: Session) -> None:
    db.refresh(lote)


def list_lote_qrs(lote_id: int, db: Session) -> list[CodigoQR]:
    return db.query(CodigoQR).filter(CodigoQR.lote_id == lote_id).all()


def get_qr_by_id(qr_id: str, db: Session) -> CodigoQR | None:
    return db.query(CodigoQR).filter(CodigoQR.qr_id == qr_id).first()


def get_lote(lote_id: int, db: Session) -> Lote | None:
    return db.query(Lote).filter(Lote.loteid == lote_id).first()
