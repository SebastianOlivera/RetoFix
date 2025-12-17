from sqlalchemy import Column, Integer, String
from app.db.connection import Base


class Usuario(Base):
    __tablename__ = "usuario"

    usuarioid = Column(Integer, primary_key=True, index=True)
    mail = Column(String(255), unique=True, nullable=False, index=True)
    rol = Column(String(50), nullable=False)
    passwordhash = Column(String(255), nullable=False)
    nombre = Column(String(150), nullable=True)
