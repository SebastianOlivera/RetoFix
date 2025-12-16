from sqlalchemy.orm import Session
from app.models.campo import Campo


def get_all(db: Session):
    return db.query(Campo).all()


def get_by_id(db: Session, campoid: int):
    return db.query(Campo).filter(Campo.campoid == campoid).first()


def create(db: Session, data: dict):
    campo = Campo(**data)
    db.add(campo)
    db.commit()
    db.refresh(campo)
    return campo


def update(db: Session, campo: Campo, data: dict):
    for key, value in data.items():
        setattr(campo, key, value)

    db.commit()
    db.refresh(campo)
    return campo


def delete(db: Session, campo: Campo):
    db.delete(campo)
    db.commit()
