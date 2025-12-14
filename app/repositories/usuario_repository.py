from sqlalchemy.orm import Session

from app.models.usuario import Usuario


def list_all(db: Session) -> list[Usuario]:
    return db.query(Usuario).all()


def get_by_id(db: Session, usuarioid: int) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.usuarioid == usuarioid).first()


def get_by_mail(db: Session, mail: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.mail == mail).first()


def create(db: Session, usuario: Usuario) -> Usuario:
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def update(db: Session, usuario: Usuario) -> Usuario:
    db.commit()
    db.refresh(usuario)
    return usuario


def delete(db: Session, usuario: Usuario) -> None:
    db.delete(usuario)
    db.commit()
