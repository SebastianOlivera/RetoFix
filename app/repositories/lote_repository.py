from sqlalchemy.orm import Session

from app.models.lote import Lote
from sqlalchemy.orm import Session

from app.models.lote import Lote


def create(db: Session, data: dict) -> Lote:
    lote = Lote(**data)
    db.add(lote)
    db.commit()
    db.refresh(lote)
    return lote


def list_all(db: Session) -> list[Lote]:
    return db.query(Lote).all()


def get_by_id(db: Session, lote_id: int) -> Lote | None:
    return db.query(Lote).filter(Lote.loteid == lote_id).first()


def update(db: Session, lote: Lote, data: dict) -> Lote:
    for field, value in data.items():
        setattr(lote, field, value)
    db.commit()
    db.refresh(lote)
    return lote


def delete(db: Session, lote: Lote) -> None:
    db.delete(lote)
    db.commit()
