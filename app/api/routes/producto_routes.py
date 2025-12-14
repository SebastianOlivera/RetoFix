# routers/producto_routes.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.dependencies import get_db
from app.schemas import ProductoCreate, ProductoUpdate, ProductoResponse
from app.services import producto_service as svc

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("", response_model=ProductoResponse)
def crear_producto(payload: ProductoCreate, db: Session = Depends(get_db)):
    p = svc.create(db, payload)
    return svc.serialize_producto(p)

@router.get("", response_model=List[ProductoResponse])
def listar_productos(
    categoria: Optional[str] = Query(default=None),
    db: Session = Depends(get_db)
):
    items = svc.list_all(db, categoria=categoria)
    return [svc.serialize_producto(p) for p in items]

@router.get("/{productoid}", response_model=ProductoResponse)
def obtener_producto(productoid: int, db: Session = Depends(get_db)):
    p = svc.get_by_id(db, productoid)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return svc.serialize_producto(p)

@router.patch("/{productoid}", response_model=ProductoResponse)
def actualizar_producto(productoid: int, payload: ProductoUpdate, db: Session = Depends(get_db)):
    p = svc.update(db, productoid, payload)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return svc.serialize_producto(p)

@router.delete("/{productoid}")
def eliminar_producto(productoid: int, db: Session = Depends(get_db)):
    ok = svc.delete(db, productoid)
    if not ok:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"ok": True}

@router.get("/{productoid}/claims")
def claims_de_producto(productoid: int, db: Session = Depends(get_db)):
    p = svc.get_by_id(db, productoid)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"productoid": productoid, "claims": svc.split_claims(p.claim)}
