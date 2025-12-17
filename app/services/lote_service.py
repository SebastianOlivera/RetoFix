from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.lote import Lote
from app.repositories import campo_repository, lote_repository
from app.schemas.lote import LoteCreate, LoteUpdate


def create_Lote(db: Session, data: LoteCreate) -> Lote:
    if not campo_repository.exists(db, data.campoid):
        raise HTTPException(status_code=404, detail="Campo no encontrado")
    return lote_repository.create(db, data.model_dump())


def get_lotes(db: Session) -> list[Lote]:
    return lote_repository.list_all(db)


def get_lote_by_id(db: Session, lote_id: int) -> Lote | None:
    return lote_repository.get_by_id(db, lote_id)


def update_lote(db: Session, lote: Lote, data: LoteUpdate) -> Lote:
    if data.campoid is not None and not campo_repository.exists(db, data.campoid):
        raise HTTPException(status_code=404, detail="Campo no encontrado")
    return lote_repository.update(db, lote, data.model_dump(exclude_unset=True))


def delete_lote(db: Session, lote: Lote) -> None:
    lote_repository.delete(db, lote)
