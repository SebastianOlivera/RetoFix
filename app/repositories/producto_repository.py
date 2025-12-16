from sqlalchemy.orm import Session

from app.models import Producto


def create_producto(db: Session, **fields) -> Producto:
    producto = Producto(**fields)
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


def list_productos(db: Session) -> list[Producto]:
    return db.query(Producto).all()


def get_producto(db: Session, producto_id: int) -> Producto | None:
    return db.query(Producto).filter(Producto.productoid == producto_id).first()


def update_producto(db: Session, producto: Producto, **fields) -> Producto:
    for field, value in fields.items():
        setattr(producto, field, value)
    db.commit()
    db.refresh(producto)
    return producto


def delete_producto(db: Session, producto: Producto) -> None:
    db.delete(producto)
    db.commit()
