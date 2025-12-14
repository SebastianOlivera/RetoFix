from sqlalchemy.orm import Session

from app.models.usuario import Usuario


def create_user(nombre: str, hashed_password: str, db: Session) -> Usuario:
    user = Usuario(mail=nombre, passwordhash=hashed_password, rol="usuario")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session) -> list[Usuario]:
    return db.query(Usuario).all()
