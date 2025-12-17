from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.cultivo import Cultivo
from app.schemas.cultivo import CultivoCreate, CultivoUpdate


def crear_cultivo(db: Session, cultivo_data: CultivoCreate) -> Cultivo:
    """Crear un nuevo cultivo"""
    cultivo = Cultivo(
        variedad=cultivo_data.variedad,
        practicasagronomicas=cultivo_data.practicasagronomicas,
        usofertilizante=cultivo_data.usofertilizante,
        condicionesclimaticas=cultivo_data.condicionesclimaticas,
    )
    db.add(cultivo)
    db.commit()
    db.refresh(cultivo)
    return cultivo


def obtener_todos_cultivos(db: Session) -> List[Cultivo]:
    """Obtener todos los cultivos"""
    return db.query(Cultivo).all()


def obtener_cultivo(db: Session, cultivo_id: int) -> Optional[Cultivo]:
    """Obtener un cultivo por ID"""
    cultivo = db.query(Cultivo).filter(Cultivo.cultivoid == cultivo_id).first()
    if not cultivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cultivo no encontrado"
        )
    return cultivo


def actualizar_cultivo_completo(
    db: Session, cultivo_id: int, cultivo_data: CultivoUpdate
) -> Cultivo:
    """Actualizar todos los campos de un cultivo (PUT)"""
    cultivo = db.query(Cultivo).filter(Cultivo.cultivoid == cultivo_id).first()
    if not cultivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cultivo no encontrado"
        )

    cultivo.variedad = cultivo_data.variedad
    cultivo.practicasagronomicas = cultivo_data.practicasagronomicas
    cultivo.usofertilizante = cultivo_data.usofertilizante
    cultivo.condicionesclimaticas = cultivo_data.condicionesclimaticas

    db.commit()
    db.refresh(cultivo)
    return cultivo


def actualizar_cultivo_parcial(
    db: Session, cultivo_id: int, cultivo_data: CultivoUpdate
) -> Cultivo:
    """Actualizar solo los campos proporcionados (PATCH)"""
    cultivo = db.query(Cultivo).filter(Cultivo.cultivoid == cultivo_id).first()
    if not cultivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cultivo no encontrado"
        )

    # Solo actualizar campos que no sean None
    if cultivo_data.variedad is not None:
        cultivo.variedad = cultivo_data.variedad
    if cultivo_data.practicasagronomicas is not None:
        cultivo.practicasagronomicas = cultivo_data.practicasagronomicas
    if cultivo_data.usofertilizante is not None:
        cultivo.usofertilizante = cultivo_data.usofertilizante
    if cultivo_data.condicionesclimaticas is not None:
        cultivo.condicionesclimaticas = cultivo_data.condicionesclimaticas

    db.commit()
    db.refresh(cultivo)
    return cultivo


def eliminar_cultivo(db: Session, cultivo_id: int) -> dict:
    """Eliminar un cultivo"""
    cultivo = db.query(Cultivo).filter(Cultivo.cultivoid == cultivo_id).first()
    if not cultivo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cultivo no encontrado"
        )

    db.delete(cultivo)
    db.commit()
    return {"message": f"Cultivo {cultivo_id} eliminado exitosamente"}
