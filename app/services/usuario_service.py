from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.models.usuario import Usuario
from app.schemas import UsuarioCreate, UsuarioUpdatePut, UsuarioPatch


def _ensure_unique_mail(db: Session, mail: str, usuario_id: int | None = None) -> None:
    query = db.query(Usuario).filter(Usuario.mail == mail)
    if usuario_id:
        query = query.filter(Usuario.usuarioid != usuario_id)
    if query.first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El mail ya esta registrado",
        )


def _apply_password_if_needed(user: Usuario, password: str | None) -> None:
    if password:
        user.passwordhash = get_password_hash(password)


def create(db: Session, payload: UsuarioCreate) -> Usuario:
    _ensure_unique_mail(db, payload.mail)
    user = Usuario(mail=payload.mail, rol=payload.rol, nombre=payload.nombre)
    _apply_password_if_needed(user, payload.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def list_all(db: Session) -> list[Usuario]:
    return db.query(Usuario).order_by(Usuario.usuarioid).all()


def get_by_id(db: Session, usuario_id: int) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.usuarioid == usuario_id).first()


def get_by_mail(db: Session, mail: str) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.mail == mail).first()


def update_put(db: Session, usuario_id: int, payload: UsuarioUpdatePut) -> Usuario:
    user = get_by_id(db, usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    _ensure_unique_mail(db, payload.mail, usuario_id=usuario_id)
    user.mail = payload.mail
    user.rol = payload.rol
    _apply_password_if_needed(user, payload.password)
    db.commit()
    db.refresh(user)
    return user


def patch(db: Session, usuario_id: int, payload: UsuarioPatch) -> Usuario:
    user = get_by_id(db, usuario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    if payload.mail is not None and payload.mail != user.mail:
        _ensure_unique_mail(db, payload.mail, usuario_id=usuario_id)
        user.mail = payload.mail

    if payload.rol is not None:
        user.rol = payload.rol

    _apply_password_if_needed(user, payload.password)

    db.commit()
    db.refresh(user)
    return user

def authenticate(db: Session, mail: str, password: str) -> Usuario:
    user = db.query(Usuario).filter(Usuario.mail == mail).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales invalidas",
        )

    if verify_password(password, user.passwordhash):
        return user

    if user.passwordhash == password:
        user.passwordhash = get_password_hash(password)
        db.commit()
        db.refresh(user)
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales invalidas",
    )
