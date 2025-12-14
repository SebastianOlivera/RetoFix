from sqlalchemy.orm import Session

from app.models.info_nutricional import InfoNutricional
from app.repositories import info_nutricional_repository
from app.schemas.info_nutricional import InfoNutricionalCreate, InfoNutricionalUpdate


def create_info_nutricional(db: Session, data: InfoNutricionalCreate):
    return info_nutricional_repository.create(db, data.model_dump())


def get_info_nutricional(db: Session):
    return info_nutricional_repository.list_all(db)


def get_info_nutricional_by_id(db: Session, info_id: int):
    return info_nutricional_repository.get_by_id(db, info_id)


def update_info_nutricional(db: Session, info: InfoNutricional, data: InfoNutricionalUpdate):
    return info_nutricional_repository.update(db, info, data.model_dump(exclude_unset=True))


def delete_info_nutricional(db: Session, info: InfoNutricional):
    info_nutricional_repository.delete(db, info)
