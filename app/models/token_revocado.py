from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.db.connection import Base


class TokenRevocado(Base):
    __tablename__ = "token_revocado"

    id = Column(Integer, primary_key=True, index=True)
    jti = Column(String(255), unique=True, nullable=False, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.usuarioid"), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    def expirado(self, referencia: datetime | None = None) -> bool:
        if not self.expires_at:
            return False
        referencia = referencia or datetime.now(tz=self.expires_at.tzinfo)
        return self.expires_at <= referencia
