from sqlalchemy.orm import Session

from app.models import User


def create_user(nombre: str, hashed_password: str, db: Session) -> User:
    user = User(nombre=nombre, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_users(db: Session) -> list[User]:
    return db.query(User).all()
