from sqlalchemy.orm import Session

from app.models.info_nutricional import InfoNutricional


def create(db: Session, data: dict) -> InfoNutricional:
    info = InfoNutricional(**data)
    db.add(info)
    db.commit()
    db.refresh(info)
    return info


def list_all(db: Session) -> list[InfoNutricional]:
    return db.query(InfoNutricional).all()


def get_by_id(db: Session, info_id: int) -> InfoNutricional | None:
    return db.query(InfoNutricional).filter(InfoNutricional.infoid == info_id).first()


def update(db: Session, info: InfoNutricional, data: dict) -> InfoNutricional:
    for field, value in data.items():
        setattr(info, field, value)
    db.commit()
    db.refresh(info)
    return info


def delete(db: Session, info: InfoNutricional) -> None:
    db.delete(info)
    db.commit()
