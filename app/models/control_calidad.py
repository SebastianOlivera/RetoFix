from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.connection import Base


class ControlDeCalidad(Base):
    __tablename__ = "controles_de_calidad"

    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("lote.id"), nullable=False, unique=True)
    estado = Column(String, nullable=False)
    observaciones = Column(Text)
    inspector = Column(String)
    fecha_inspeccion = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    lote = relationship("Lote", backref="control_calidad")
