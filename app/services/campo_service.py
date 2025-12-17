import base64
from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.repositories import campo_repository


def _normalize_kmz_to_bytes(value):
    if value is None:
        return None

    if isinstance(value, (bytes, bytearray)):
        return bytes(value)

    if isinstance(value, memoryview):
        return value.tobytes()

    if isinstance(value, str):
        s = value.strip()

        # Postgres bytea -> "\x..."
        if s.startswith("\\x"):
            return bytes.fromhex(s[2:])

        # posible base64
        try:
            return base64.b64decode(s, validate=True)
        except Exception:
            pass

        return s.encode("utf-8")

    return bytes(value)


# =========================
# CRUD
# =========================

def create_campo(db: Session, data: dict):
    return campo_repository.create(db, data)


def get_campos(db: Session):
    return campo_repository.list_with_kmz_flag(db)


def get_campo(db: Session, campoid: int):
    campo = campo_repository.get_one_with_kmz_flag(db, campoid)
    if not campo:
        raise HTTPException(status_code=404, detail="Campo no encontrado")
    return campo


def update_campo_put(db: Session, campoid: int, data: dict):
    return campo_repository.update_put(db, campoid, data)


def update_campo_patch(db: Session, campoid: int, data: dict):
    return campo_repository.update_patch(db, campoid, data)


def delete_campo(db: Session, campo: dict):
    campo_repository.delete_one(db, campo["campoid"])


# =========================
# KMZ
# =========================

def upload_kmz(db: Session, campoid: int, file: UploadFile):
    if not campo_repository.exists(db, campoid):
        raise HTTPException(status_code=404, detail="Campo no encontrado")

    kmz_bytes = file.file.read()
    campo_repository.set_kmz(db, campoid, kmz_bytes)


def get_kmz(db: Session, campoid: int) -> bytes:
    if not campo_repository.exists(db, campoid):
        raise HTTPException(status_code=404, detail="Campo no encontrado")

    raw = campo_repository.get_raw_kmz(db, campoid)
    kmz_bytes = _normalize_kmz_to_bytes(raw)

    if not kmz_bytes:
        raise HTTPException(status_code=404, detail="KMZ no encontrado")

    return kmz_bytes


def delete_kmz(db: Session, campoid: int):
    if not campo_repository.exists(db, campoid):
        raise HTTPException(status_code=404, detail="Campo no encontrado")

    campo_repository.set_kmz(db, campoid, None)
