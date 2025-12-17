from fastapi import APIRouter, Depends, UploadFile, File, Form, Response, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.services import campo_service

router = APIRouter(prefix="/campos", tags=["Campos"])


@router.get("")
def listar_campos(db: Session = Depends(get_db)):
    return campo_service.get_campos(db)


@router.get("/{campoid}")
def obtener_campo(campoid: int, db: Session = Depends(get_db)):
    return campo_service.get_campo(db, campoid)


@router.post("", status_code=status.HTTP_201_CREATED)
def crear_campo(
    nombre: str = Form(...),
    departamento: str = Form(...),
    tipomanejo: str = Form(...),
    coordenadas: str | None = Form(None),
    db: Session = Depends(get_db),
):
    data = {
        "nombre": nombre,
        "departamento": departamento,
        "tipomanejo": tipomanejo,
        "coordenadas": coordenadas,
    }
    return campo_service.create_campo(db, data)


@router.post("/{campoid}/kmz", status_code=status.HTTP_204_NO_CONTENT)
def subir_kmz(
    campoid: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    campo_service.upload_kmz(db, campoid, file)


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


@router.delete("/{campoid}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_campo(campoid: int, db: Session = Depends(get_db)):
    campo = campo_service.get_campo(db, campoid)
    campo_service.delete_campo(db, campo)


@router.delete("/{campoid}/kmz", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_kmz(campoid: int, db: Session = Depends(get_db)):
    campo_service.delete_kmz(db, campoid)


@router.get("/{campoid}/kmz")
def descargar_kmz(campoid: int, db: Session = Depends(get_db)):
    kmz_bytes = campo_service.get_kmz(db, campoid)
    return Response(
        content=kmz_bytes,
        media_type="application/vnd.google-earth.kmz",
        headers={
            "Content-Disposition": f'attachment; filename="campo_{campoid}.kmz"'
        },
    )
