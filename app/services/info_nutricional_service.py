from sqlalchemy.orm import Session

from app.models.info_nutricional import InfoNutricional
from app.schemas.info_nutricional import InfoNutricionalCreate, InfoNutricionalUpdate


def create_info_nutricional(db: Session, data: InfoNutricionalCreate):
    info = InfoNutricional(**data.model_dump())
    db.add(info)
    db.commit()
    db.refresh(info)
    return info


def get_info_nutricional(db: Session):
    return db.query(InfoNutricional).all()


def get_info_nutricional_by_id(db: Session, info_id: int):
    return db.query(InfoNutricional).filter(InfoNutricional.infoid == info_id).first()


def update_info_nutricional(db: Session, info: InfoNutricional, data: InfoNutricionalUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(info, field, value)

    db.commit()
    db.refresh(info)
    return info


def delete_info_nutricional(db: Session, info: InfoNutricional):
    db.delete(info)
    db.commit()
