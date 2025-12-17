from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.db.connection import Base

class CodigoQR(Base):
    __tablename__ = "codigos_qr"

    id = Column(Integer, primary_key=True, index=True)
    qr_id = Column(String, unique=True, nullable=False, index=True)
    lote_id = Column(Integer, ForeignKey("lote.loteid"), nullable=False)
    qr_image_path = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    lote = relationship("Lote", backref="codigos_qr")
