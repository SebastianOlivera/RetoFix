from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.connection import get_db
from app.services import campo_service
from app.db.connection import SessionLocal


router = APIRouter(prefix="/campos", tags=["Campos"])


@router.get("/campos")
def listar_campos(db: Session = Depends(get_db)):
    return campo_service.get_campos(db)


@router.get("/{campoid}", status_code=status.HTTP_200_OK)
def obtener_campo(campoid: int, db: Session = Depends(get_db)):
    return campo_service.get_campo(db, campoid)


@router.post("/", status_code=status.HTTP_201_CREATED)
def crear_campo(
    nombre: str,
    departamento: str,
    tipomanejo: str,
    coordenadas: str | None = None,
    db: Session = Depends(get_db)
):
    data = {
        "nombre": nombre,
        "departamento": departamento,
        "tipomanejo": tipomanejo,
        "coordenadas": coordenadas
    }
    return campo_service.create_campo(db, data)


@router.delete("/{campoid}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_campo(campoid: int, db: Session = Depends(get_db)):
    campo = campo_service.get_campo(db, campoid)
    campo_service.delete_campo(db, campo)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# PUT → reemplazo total
@router.put("/{campoid}")
def actualizar_campo_put(
    campoid: int,
    nombre: str,
    departamento: str,
    tipomanejo: str,
    coordenadas: str | None = None,
    archivokmz: str | None = None,
    db: Session = Depends(get_db),
):
    data = {
        "nombre": nombre,
        "departamento": departamento,
        "tipomanejo": tipomanejo,
        "coordenadas": coordenadas,
        "archivokmz": archivokmz,
    }
    return campo_service.update_campo_put(db, campoid, data)


# PATCH → actualización parcial
@router.patch("/{campoid}")
def actualizar_campo_patch(
    campoid: int,
    nombre: str | None = None,
    departamento: str | None = None,
    tipomanejo: str | None = None,
    coordenadas: str | None = None,
    archivokmz: str | None = None,
    db: Session = Depends(get_db),
):
    data = {
        k: v
        for k, v in {
            "nombre": nombre,
            "departamento": departamento,
            "tipomanejo": tipomanejo,
            "coordenadas": coordenadas,
            "archivokmz": archivokmz,
        }.items()
        if v is not None
    }

    return campo_service.update_campo_patch(db, campoid, data)