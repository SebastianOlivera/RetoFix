import shutil
from datetime import datetime
from pathlib import Path
from typing import Iterable

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models import CodigoQR, Lote


def create_lote(
    numero_lote: str,
    producto_id: int,
    cantidad: int,
    campo_nombre: str | None,
    fecha_produccion: datetime,
    db: Session,
) -> Lote:
    lote = Lote(
        numero_lote=numero_lote,
        producto_id=producto_id,
        cantidad=cantidad,
        campo_nombre=campo_nombre,
        fecha_produccion=fecha_produccion,
    )
    db.add(lote)
    db.flush()
    return lote


def add_qrs_to_db(qrs: Iterable[CodigoQR], db: Session) -> None:
    db.add_all(list(qrs))
    db.commit()


def add_qr(qr: CodigoQR, db: Session) -> None:
    db.add(qr)


def refresh_lote(lote: Lote, db: Session) -> None:
    db.refresh(lote)


def list_lote_qrs(lote_id: int, db: Session) -> list[CodigoQR]:
    return db.query(CodigoQR).filter(CodigoQR.lote_id == lote_id).all()


def get_qr_by_id(qr_id: str, db: Session) -> CodigoQR | None:
    return db.query(CodigoQR).filter(CodigoQR.qr_id == qr_id).first()


def get_lote(lote_id: int, db: Session) -> Lote | None:
    return db.query(Lote).filter(Lote.id == lote_id).first()


def save_kmz(lote: Lote, file: UploadFile, db: Session) -> Path:
    kmz_dir = Path("kmz_files")
    kmz_dir.mkdir(exist_ok=True)

    file_path = kmz_dir / f"lote_{lote.id}_{file.filename}"
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    lote.kmz_path = str(file_path)
    db.commit()
    return file_path
