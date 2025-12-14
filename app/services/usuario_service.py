from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.usuario import Usuario
from app.schemas.schemas import UsuarioCreate, UsuarioPatch, UsuarioUpdatePut

# -------------------------------------------------
# Password hashing
# - Evitamos bcrypt (límite 72 bytes y problemas de backend en Windows)
# - pbkdf2_sha256 es estable y soporta passwords largas
# -------------------------------------------------
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


# -------------------------
# helpers
# -------------------------
def _hash_password(password: str) -> str:
    if password is None or len(password) == 0:
        raise ValueError("Password requerido")
    return pwd_context.hash(password)


def _verify_password(plain: str, hashed: str) -> bool:
    if not plain or not hashed:
        return False
    return pwd_context.verify(plain, hashed)


# -------------------------
# queries
# -------------------------
def list_all(db: Session):
    return db.query(Usuario).all()


def get_by_id(db: Session, usuarioid: int):
    return db.query(Usuario).filter(Usuario.usuarioid == usuarioid).first()


def get_by_mail(db: Session, mail: str):
    return db.query(Usuario).filter(Usuario.mail == mail).first()


# -------------------------
# commands
# -------------------------
def create(db: Session, payload: UsuarioCreate):
    # evitar mails duplicados
    if get_by_mail(db, payload.mail):
        raise ValueError("El mail ya existe")

    usuario = Usuario(
        mail=payload.mail,
        rol=payload.rol,
        passwordhash=_hash_password(payload.password),
    )

    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


def update(db: Session, usuarioid: int, payload: UsuarioPatch):
    usuario = get_by_id(db, usuarioid)
    if not usuario:
        return None

    if payload.mail is not None:
        # si cambia el mail, validar duplicados
        existente = get_by_mail(db, payload.mail)
        if existente and existente.usuarioid != usuarioid:
            raise ValueError("El mail ya existe")
        usuario.mail = payload.mail

    if payload.rol is not None:
        usuario.rol = payload.rol

    if payload.password is not None:
        usuario.passwordhash = _hash_password(payload.password)

    db.commit()
    db.refresh(usuario)
    return usuario


def delete(db: Session, usuarioid: int):
    usuario = get_by_id(db, usuarioid)
    if not usuario:
        return False

    db.delete(usuario)
    db.commit()
    return True


# opcional (por si después hacés login)
def authenticate(db: Session, mail: str, password: str):
    u = get_by_mail(db, mail)
    if not u:
        return None
    if not _verify_password(password, u.passwordhash):
        return None
    return u

def update_put(db: Session, usuarioid: int, payload: UsuarioUpdatePut):
    """
    PUT = reemplazo completo.
    En tu schema UsuarioUpdatePut hereda de UsuarioCreate, así que trae:
    mail (required), rol (required), password (required)
    """
    usuario = get_by_id(db, usuarioid)
    if not usuario:
        return None

    # validar duplicados si cambia el mail
    existente = get_by_mail(db, payload.mail)
    if existente and existente.usuarioid != usuarioid:
        raise ValueError("El mail ya existe")

    usuario.mail = payload.mail
    usuario.rol = payload.rol
    usuario.passwordhash = _hash_password(payload.password)

    db.commit()
    db.refresh(usuario)
    return usuario