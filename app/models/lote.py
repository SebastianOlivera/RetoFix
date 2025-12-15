from sqlalchemy import Column, Date, Integer

from app.db.connection import Base


class Lote(Base):
    __tablename__ = "lote"

    loteid = Column(Integer, primary_key=True, index=True)
    fechasiembra = Column(Date, nullable=True)
    fechacosecha = Column(Date, nullable=True)
    fechaprocesamiento = Column(Date, nullable=True)
    fechavencimiento = Column(Date, nullable=True)
