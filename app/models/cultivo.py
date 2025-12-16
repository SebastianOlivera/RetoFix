from sqlalchemy import Column, Integer, String, Text

from app.db.connection import Base


class Cultivo(Base):
    __tablename__ = "cultivo"

    cultivoid = Column("cultivoid", Integer, primary_key=True, index=True)
    variedad = Column("variedad", String(200))
    practicasagronomicas = Column("practicasagronomicas", Text)
    usofertilizante = Column("usofertilizante", String(200))
    condicionesclimaticas = Column("condicionesclimaticas", Text)
