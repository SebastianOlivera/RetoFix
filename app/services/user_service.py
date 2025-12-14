import bcrypt
from sqlalchemy.orm import Session
from app.repositories.user_repository import create_user, list_users
from app.schemas.schemas import UserCreate


def crear_usuario(payload: UserCreate, db: Session):
    hashed_password = bcrypt.hashpw(payload.password.encode("utf-8"), bcrypt.gensalt()).decode(
        "utf-8"
    )
    return create_user(nombre=payload.nombre, hashed_password=hashed_password, db=db)


def listar_usuarios(db: Session):
    return list_users(db)
