from sqlalchemy import Column, ForeignKey, Integer

from app.db.connection import Base


class ProductoLotePertenece(Base):
    __tablename__ = "productolotepertenece"

    productoid = Column(Integer, ForeignKey("producto.productoid"), primary_key=True)
    loteid = Column(Integer, ForeignKey("lote.loteid"), primary_key=True)
