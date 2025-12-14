from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.campo import Campo
from app.repositories import campo_repository


def get_campos(db: Session):
    return campo_repository.get_all(db)


def get_campo(db: Session, campoid: int):
    campo = campo_repository.get_by_id(db, campoid)
    if not campo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Campo no encontrado"
        )
    return campo


def create_campo(db: Session, payload: dict):
    campo = Campo(**payload)
    db.add(campo)
    db.commit()
    db.refresh(campo)
    return campo



def delete_campo(db: Session, campo: Campo):
    """
    Placeholder de regla de negocio:
    si en el futuro el campo tiene lotes, acá se valida.
    """
    # PLACEHOLDER LOTE
    if hasattr(campo, "lotes") and campo.lotes:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el campo porque tiene lotes asociados"
        )

    campo_repository.delete(db, campo)

    

def update_campo_put(db: Session, campoid: int, data: dict):
    campo = db.query(Campo).filter(Campo.campoid == campoid).first()

    if not campo:
        raise HTTPException(status_code=404, detail="Campo no encontrado")

    # PUT → reemplazo completo
    campo.nombre = data["nombre"]
    campo.departamento = data["departamento"]
    campo.tipomanejo = data["tipomanejo"]
    campo.coordenadas = data.get("coordenadas")
    campo.archivokmz = data.get("archivokmz")

    db.commit()
    db.refresh(campo)
    return campo


def update_campo_patch(db: Session, campoid: int, data: dict):
    campo = db.query(Campo).filter(Campo.campoid == campoid).first()

    if not campo:
        raise HTTPException(status_code=404, detail="Campo no encontrado")

    # PATCH → solo lo que venga
    for key, value in data.items():
        setattr(campo, key, value)

    db.commit()
    db.refresh(campo)
    return campo
