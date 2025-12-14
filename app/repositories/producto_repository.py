from sqlalchemy.orm import Session

from app.models import Producto


def create_producto(nombre: str, descripcion: str, db: Session) -> Producto:
    producto = Producto(nombre=nombre, descripcion=descripcion)
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


def list_productos(db: Session) -> list[Producto]:
    return db.query(Producto).all()


def get_producto(db: Session, producto_id: int) -> Producto | None:
    return db.query(Producto).filter(Producto.productoid == producto_id).first()
