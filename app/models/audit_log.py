from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.sql import func

from app.db.connection import Base


class UserActionLog(Base):
    __tablename__ = "user_action_log"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.usuarioid"), nullable=False, index=True)
    path = Column(String(255), nullable=False)
    method = Column(String(16), nullable=False)
    status_code = Column(Integer, nullable=False)
    action = Column(String(128), nullable=True)
    client_ip = Column(String(64), nullable=True)
    user_agent = Column(String(255), nullable=True)
    payload = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
