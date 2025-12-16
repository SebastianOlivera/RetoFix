from typing import List

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.producto_lote import ProductoLoteCambio, ProductoLoteRespuesta
from app.services import producto_lote_service as svc

router = APIRouter(tags=["Producto-Lote"])


@router.post(
    "/productos/{producto_id}/lotes/{lote_id}",
    status_code=201,
    response_model=ProductoLoteRespuesta,
)
def asociar_producto_lote(producto_id: int, lote_id: int, db: Session = Depends(get_db)):
    enlace = svc.crear(db, producto_id, lote_id)
    return ProductoLoteRespuesta(productoid=enlace.productoid, loteid=enlace.loteid)


@router.delete("/productos/{producto_id}/lotes/{lote_id}", status_code=204)
def desasociar_producto_lote(producto_id: int, lote_id: int, db: Session = Depends(get_db)):
    svc.eliminar(db, producto_id, lote_id)
    return None


@router.get("/productos-lotes", response_model=List[ProductoLoteRespuesta])
def listar_asociaciones(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    enlaces = svc.listar(db, limit=limit, offset=offset)
    return [ProductoLoteRespuesta(productoid=e.productoid, loteid=e.loteid) for e in enlaces]


@router.get(
    "/productos/{producto_id}/lotes/{lote_id}", response_model=ProductoLoteRespuesta
)
def obtener_asociacion(producto_id: int, lote_id: int, db: Session = Depends(get_db)):
    enlace = svc.obtener(db, producto_id, lote_id)
    return ProductoLoteRespuesta(productoid=enlace.productoid, loteid=enlace.loteid)


@router.get("/productos/{producto_id}/lotes")
def obtener_lotes_de_producto(producto_id: int, db: Session = Depends(get_db)):
    return svc.lotes_de_producto(db, producto_id)


@router.get("/lotes/{lote_id}/productos")
def obtener_productos_de_lote(lote_id: int, db: Session = Depends(get_db)):
    return svc.productos_de_lote(db, lote_id)


@router.patch(
    "/productos/{producto_id}/lotes/{lote_id}", response_model=ProductoLoteRespuesta
)
def actualizar_asociacion(
    producto_id: int,
    lote_id: int,
    payload: ProductoLoteCambio = Body(...),
    db: Session = Depends(get_db),
):
    cambio = svc.actualizar(db, producto_id, lote_id, payload.nuevo_productoid, payload.nuevo_loteid)
    return ProductoLoteRespuesta(
        productoid=cambio["new"]["productoid"],
        loteid=cambio["new"]["loteid"],
    )
