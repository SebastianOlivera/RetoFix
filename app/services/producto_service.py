from typing import Optional, List
from sqlalchemy.orm import Session

from app.repositories.producto_repository import (
    create_producto,
    delete_producto,
    get_producto,
    list_productos,
    update_producto,
)
from app.schemas.producto import (
    ProductoCreate,
    ProductoUpdate,
    ProductoUpdatePut,
    ProductoResponse,
)


# ========= CRUD =========

def create(db: Session, payload: ProductoCreate):
    return create_producto(
        db=db,
        nombrecomercial=payload.nombrecomercial,
        descripcion=payload.descripcion,
        imagenurl=payload.imagenurl,
        categoria=payload.categoria,
        porciones=payload.porciones,
        mododeuso=payload.mododeuso,
        pdfurl=payload.pdfurl,
        claim=payload.claim,
    )


def list_all(db: Session, categoria: Optional[str] = None):
    productos = list_productos(db)
    if categoria:
        productos = [p for p in productos if p.categoria == categoria]
    return productos


def get_by_id(db: Session, productoid: int):
    return get_producto(db, productoid)


def update_put(db: Session, productoid: int, payload: ProductoUpdatePut):
    producto = get_producto(db, productoid)
    if not producto:
        return None

    return update_producto(db, producto, **payload.model_dump())


def update(db: Session, productoid: int, payload: ProductoUpdate):
    producto = get_producto(db, productoid)
    if not producto:
        return None

    return update_producto(db, producto, **payload.model_dump(exclude_unset=True))


def delete(db: Session, productoid: int) -> bool:
    producto = get_producto(db, productoid)
    if not producto:
        return False

    delete_producto(db, producto)
    return True


# ========= HELPERS =========

def split_claims(claim: str | None) -> List[str]:
    if not claim:
        return []
    return [c.strip() for c in claim.split(";") if c.strip()]


def serialize_producto(p) -> ProductoResponse:
    return ProductoResponse(
        productoid=p.productoid,
        nombrecomercial=p.nombrecomercial,
        descripcion=p.descripcion,
        imagenurl=p.imagenurl,
        categoria=p.categoria,
        porciones=p.porciones,
        mododeuso=p.mododeuso,
        pdfurl=p.pdfurl,
        claim=p.claim,
        claims=split_claims(p.claim),
    )
