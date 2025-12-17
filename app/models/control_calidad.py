from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.connection import Base


class ControlDeCalidad(Base):
    __tablename__ = "control_de_calidad"

    controlcalidadid = Column(Integer, primary_key=True, index=True)
    loteid = Column(Integer, ForeignKey("lote.loteid"), nullable=False, unique=True)
    pdfurl = Column(String(500), nullable=True)
    resumenresultados = Column(Text, nullable=True)
    responsable = Column(String(200), nullable=True)

    lote = relationship("Lote", backref="control_de_calidad")
