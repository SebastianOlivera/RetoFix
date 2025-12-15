from sqlalchemy.orm import Session

from app.models.lote import Lote
from app.repositories import lote_repository
from app.schemas.lote import LoteCreate, LoteUpdate


def create_Lote(db: Session, data: LoteCreate) -> Lote:
    return lote_repository.create(db, data.model_dump())


def get_lotes(db: Session) -> list[Lote]:
    return lote_repository.list_all(db)


def get_lote_by_id(db: Session, lote_id: int) -> Lote | None:
    return lote_repository.get_by_id(db, lote_id)


def update_lote(db: Session, lote: Lote, data: LoteUpdate) -> Lote:
    return lote_repository.update(db, lote, data.model_dump(exclude_unset=True))


def delete_lote(db: Session, lote: Lote) -> None:
    lote_repository.delete(db, lote)
