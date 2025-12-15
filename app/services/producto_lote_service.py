from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import producto_lote_repository as repo


def _validar_producto_y_lote(db: Session, producto_id: int, lote_id: int) -> None:
    if not repo.producto_existe(db, producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    if not repo.lote_existe(db, lote_id):
        raise HTTPException(status_code=404, detail="Lote no encontrado")


def crear(db: Session, producto_id: int, lote_id: int):
    _validar_producto_y_lote(db, producto_id, lote_id)
    if repo.existe_asociacion(db, producto_id, lote_id):
        raise HTTPException(status_code=409, detail="El producto ya está asociado a ese lote")
    return repo.crear_asociacion(db, producto_id, lote_id)


def eliminar(db: Session, producto_id: int, lote_id: int):
    if not repo.eliminar_asociacion(db, producto_id, lote_id):
        raise HTTPException(status_code=404, detail="Asociación producto-lote no encontrada")
    return {"ok": True}


def obtener(db: Session, producto_id: int, lote_id: int):
    enlace = repo.obtener_asociacion(db, producto_id, lote_id)
    if not enlace:
        raise HTTPException(status_code=404, detail="Asociación producto-lote no encontrada")
    return enlace


def listar(db: Session, limit: int = 100, offset: int = 0):
    return repo.listar_asociaciones(db, limit=limit, offset=offset)


def lotes_de_producto(db: Session, producto_id: int):
    if not repo.producto_existe(db, producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return repo.listar_lotes_por_producto(db, producto_id)


def productos_de_lote(db: Session, lote_id: int):
    if not repo.lote_existe(db, lote_id):
        raise HTTPException(status_code=404, detail="Lote no encontrado")
    return repo.listar_productos_por_lote(db, lote_id)


def actualizar(
    db: Session, producto_id: int, lote_id: int, nuevo_producto_id: int, nuevo_lote_id: int
):
    if not repo.existe_asociacion(db, producto_id, lote_id):
        raise HTTPException(status_code=404, detail="Asociación producto-lote no encontrada")

    _validar_producto_y_lote(db, nuevo_producto_id, nuevo_lote_id)

    if repo.existe_asociacion(db, nuevo_producto_id, nuevo_lote_id):
        raise HTTPException(status_code=409, detail="La nueva asociación ya existe")

    repo.actualizar_asociacion(db, producto_id, lote_id, nuevo_producto_id, nuevo_lote_id)
    return {
        "ok": True,
        "old": {"productoid": producto_id, "loteid": lote_id},
        "new": {"productoid": nuevo_producto_id, "loteid": nuevo_lote_id},
    }


def payload_qr(db: Session, producto_id: int, lote_id: int):
    payload = repo.obtener_payload_qr(db, producto_id, lote_id)
    if not payload:
        raise HTTPException(status_code=404, detail="Ese producto no pertenece a ese lote")
    return payload
