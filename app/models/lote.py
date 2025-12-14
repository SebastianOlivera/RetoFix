from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Date
from app.db.connection import Base



class Lote(Base):
    __tablename__ = "lote" 

    loteid = Column("loteid", Integer, primary_key=True, index=True)
    campoid = Column("campoid", Integer, ForeignKey("campo.campoid"), nullable=False)
    id = Column(Integer, primary_key=True, index=True)
    numero_lote = Column(String, unique=True, nullable=False, index=True)
    producto_id = Column(Integer, ForeignKey("producto.productoid"), nullable=False)
    cantidad = Column(Integer, nullable=False)

    # Placeholder hasta que lote-campo esté bien definido
    campo_nombre = Column(String)

    kmz_path = Column(String)
    fecha_produccion = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_by = Column(Integer, ForeignKey("usuario.usuarioid"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    fechasiembra = Column("fechasiembra", Date, nullable=True)
    fechacosecha = Column("fechacosecha", Date, nullable=True)
    fechaprocesamiento = Column("fechaprocesamiento", Date, nullable=True)
    fechavencimiento = Column("fechavencimiento", Date, nullable=True)