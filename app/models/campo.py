from sqlalchemy import Column, Integer, String
from app.db.connection import Base


class Campo(Base):
    __tablename__ = "campo"

    campoid = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    departamento = Column(String, nullable=False)
    tipomanejo = Column(String, nullable=False)
    coordenadas = Column(String, nullable=False)
    archivokmz = Column(String, nullable=True)
