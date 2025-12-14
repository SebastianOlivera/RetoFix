from sqlalchemy import Column, Integer, String
from app.database import Base


class InfoNutricional(Base):
    __tablename__ = "info_nutricional"

    infoid = Column(Integer, primary_key=True, index=True)
    producto = Column(String(200), nullable=True)
    porcion = Column(String(100), nullable=True)
    calorias = Column(String(50), nullable=True)
    proteinas = Column(String(50), nullable=True)
    grasas = Column(String(50), nullable=True)
    carbohidratos = Column(String(50), nullable=True)
    sodio = Column(String(50), nullable=True)
