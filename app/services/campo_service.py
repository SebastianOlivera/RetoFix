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
    return campo_repository.create(db, payload)



def delete_campo(db: Session, campo: Campo):
    if hasattr(campo, "lotes") and campo.lotes:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el campo porque tiene lotes asociados"
        )

    campo_repository.delete(db, campo)

    

def update_campo_put(db: Session, campoid: int, data: dict):
    campo = campo_repository.get_by_id(db, campoid)

    if not campo:
        raise HTTPException(status_code=404, detail="Campo no encontrado")

    # PUT → reemplazo completo
    return campo_repository.update(db, campo, data)


def update_campo_patch(db: Session, campoid: int, data: dict):
    campo = campo_repository.get_by_id(db, campoid)

    if not campo:
        raise HTTPException(status_code=404, detail="Campo no encontrado")

    # PATCH → solo lo que venga
    return campo_repository.update(db, campo, data)
