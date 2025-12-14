from sqlalchemy import Column, Integer, String, Text
from app.database import Base


class Producto(Base):
    __tablename__ = "producto"

    productoid = Column(Integer, primary_key=True, index=True)
    nombrecomercial = Column(String(200), nullable=False)
    descripcion = Column(Text, nullable=True)
    imagenurl = Column(String(500), nullable=True)
    categoria = Column(String(100), nullable=True)
    porciones = Column(Integer, nullable=True)
    mododeuso = Column(Text, nullable=True)
    pdfurl = Column(String(500), nullable=True)
    claim = Column(Text, nullable=True)
