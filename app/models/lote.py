from datetime import datetime, timezone

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String

from app.db.connection import Base


class Lote(Base):
    __tablename__ = "lote"

    loteid = Column(Integer, primary_key=True, index=True)
    campoid = Column(Integer, ForeignKey("campo.campoid"), nullable=False)
    fechasiembra = Column(Date, nullable=True)
    fechacosecha = Column(Date, nullable=True)
    fechaprocesamiento = Column(Date, nullable=True)
    fechavencimiento = Column(Date, nullable=True)

    created_by = Column(Integer, ForeignKey("usuario.usuarioid"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    numero_lote = Column(String, unique=True, nullable=True, index=True)
    cantidad = Column(Integer, nullable=True)
    campo_nombre = Column(String, nullable=True)
    kmz_path = Column(String, nullable=True)
    producto_id = Column(Integer, ForeignKey("producto.productoid"), nullable=True)
    fecha_produccion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
