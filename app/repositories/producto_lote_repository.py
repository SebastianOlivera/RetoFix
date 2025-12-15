from collections.abc import Sequence
from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models import (
    ControlDeCalidad,
    InfoNutricional,
    Lote,
    Producto,
    ProductoLotePertenece,
)


# ===== Validaciones básicas =====


def producto_existe(db: Session, producto_id: int) -> bool:
    return db.get(Producto, producto_id) is not None


def lote_existe(db: Session, lote_id: int) -> bool:
    return db.get(Lote, lote_id) is not None


def existe_asociacion(db: Session, producto_id: int, lote_id: int) -> bool:
    stmt = select(ProductoLotePertenece).where(
        ProductoLotePertenece.productoid == producto_id,
        ProductoLotePertenece.loteid == lote_id,
    )
    return db.execute(stmt).scalar_one_or_none() is not None


# ===== CRUD de asociaciones =====


def crear_asociacion(db: Session, producto_id: int, lote_id: int) -> ProductoLotePertenece:
    enlace = ProductoLotePertenece(productoid=producto_id, loteid=lote_id)
    db.add(enlace)
    db.commit()
    db.refresh(enlace)
    return enlace


def eliminar_asociacion(db: Session, producto_id: int, lote_id: int) -> bool:
    stmt = (
        delete(ProductoLotePertenece)
        .where(
            ProductoLotePertenece.productoid == producto_id,
            ProductoLotePertenece.loteid == lote_id,
        )
        .execution_options(synchronize_session="fetch")
    )
    result = db.execute(stmt)
    db.commit()
    return (result.rowcount or 0) > 0


def obtener_asociacion(
    db: Session, producto_id: int, lote_id: int
) -> Optional[ProductoLotePertenece]:
    stmt = select(ProductoLotePertenece).where(
        ProductoLotePertenece.productoid == producto_id,
        ProductoLotePertenece.loteid == lote_id,
    )
    return db.execute(stmt).scalar_one_or_none()


def listar_asociaciones(db: Session, limit: int = 100, offset: int = 0) -> Sequence[ProductoLotePertenece]:
    stmt = (
        select(ProductoLotePertenece)
        .order_by(ProductoLotePertenece.productoid, ProductoLotePertenece.loteid)
        .limit(limit)
        .offset(offset)
    )
    return db.execute(stmt).scalars().all()


def listar_lotes_por_producto(db: Session, producto_id: int) -> Sequence[Lote]:
    stmt = (
        select(Lote)
        .join(ProductoLotePertenece, ProductoLotePertenece.loteid == Lote.loteid)
        .where(ProductoLotePertenece.productoid == producto_id)
        .order_by(Lote.loteid)
    )
    return db.execute(stmt).scalars().all()


def listar_productos_por_lote(db: Session, lote_id: int) -> Sequence[Producto]:
    stmt = (
        select(Producto)
        .join(ProductoLotePertenece, ProductoLotePertenece.productoid == Producto.productoid)
        .where(ProductoLotePertenece.loteid == lote_id)
        .order_by(Producto.productoid)
    )
    return db.execute(stmt).scalars().all()


def actualizar_asociacion(
    db: Session, producto_id: int, lote_id: int, nuevo_producto_id: int, nuevo_lote_id: int
) -> None:
    # implementación sencilla: borrar y volver a crear
    stmt = delete(ProductoLotePertenece).where(
        ProductoLotePertenece.productoid == producto_id,
        ProductoLotePertenece.loteid == lote_id,
    )
    db.execute(stmt)
    db.add(ProductoLotePertenece(productoid=nuevo_producto_id, loteid=nuevo_lote_id))
    db.commit()


# ===== Payload QR =====


def obtener_payload_qr(db: Session, producto_id: int, lote_id: int) -> Optional[dict]:
    stmt = (
        select(Producto, Lote, InfoNutricional, ControlDeCalidad)
        .join(ProductoLotePertenece, ProductoLotePertenece.productoid == Producto.productoid)
        .join(Lote, ProductoLotePertenece.loteid == Lote.loteid)
        .outerjoin(InfoNutricional, InfoNutricional.productoid == Producto.productoid)
        .outerjoin(ControlDeCalidad, ControlDeCalidad.loteid == Lote.loteid)
        .where(
            ProductoLotePertenece.productoid == producto_id,
            ProductoLotePertenece.loteid == lote_id,
        )
        .limit(1)
    )

    result = db.execute(stmt).first()
    if not result:
        return None

    producto, lote, info, qc = result

    payload = {
        "producto": {
            "productoid": producto.productoid,
            "nombrecomercial": producto.nombrecomercial,
            "descripcion": producto.descripcion,
            "imagenurl": producto.imagenurl,
            "categoria": producto.categoria,
            "porciones": producto.porciones,
            "mododeuso": producto.mododeuso,
            "pdfurl": producto.pdfurl,
            "claim": producto.claim,
        },
        "lote": {
            "loteid": lote.loteid,
            "fechasiembra": lote.fechasiembra,
            "fechacosecha": lote.fechacosecha,
            "fechaprocesamiento": lote.fechaprocesamiento,
            "fechavencimiento": lote.fechavencimiento,
        },
    }

    if info:
        payload["info_nutricional"] = {
            "infonutricionalid": info.infonutricionalid,
            "calorias": info.calorias,
            "proteinas": info.proteinas,
            "grasas": info.grasas,
            "carbohidratos": info.carbohidratos,
            "vitaminas": info.vitaminas,
            "minerales": info.minerales,
            "beneficios": info.beneficios,
        }

    if qc:
        payload["control_de_calidad"] = {
            "controlcalidadid": qc.controlcalidadid,
            "pdfurl": qc.pdfurl,
            "resumenresultados": qc.resumenresultados,
            "responsable": qc.responsable,
        }

    return payload
