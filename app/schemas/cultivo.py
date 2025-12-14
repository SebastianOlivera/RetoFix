from pydantic import BaseModel
from typing import Optional


# ---------- Base ----------
class CultivoBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None


# ---------- Create ----------
class CultivoCreate(CultivoBase):
    pass


# ---------- Update ----------
class CultivoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None


# ---------- Response ----------
class CultivoResponse(CultivoBase):
    id: int

    class Config:
        from_attributes = True
