from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Text

from app.db.connection import Base


class InfoNutricional(Base):
    __tablename__ = "info_nutricional"

    infonutricionalid = Column(Integer, primary_key=True, index=True)
    productoid = Column(Integer, ForeignKey("producto.productoid"), nullable=False, unique=True)
    calorias = Column(Numeric(10, 2), nullable=True)
    proteinas = Column(Numeric(10, 2), nullable=True)
    grasas = Column(Numeric(10, 2), nullable=True)
    carbohidratos = Column(Numeric(10, 2), nullable=True)
    vitaminas = Column(Text, nullable=True)
    minerales = Column(Text, nullable=True)
    beneficios = Column(Text, nullable=True)
