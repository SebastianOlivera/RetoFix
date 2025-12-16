from typing import Optional

from pydantic import BaseModel, EmailStr


class UsuarioBase(BaseModel):
    mail: EmailStr
    rol: str
    nombre: Optional[str] = None


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdatePut(UsuarioCreate):
    pass


class UsuarioPatch(BaseModel):
    mail: Optional[EmailStr] = None
    rol: Optional[str] = None
    password: Optional[str] = None
    nombre: Optional[str] = None


class UsuarioOut(UsuarioBase):
    usuarioid: int

    class Config:
        from_attributes = True
