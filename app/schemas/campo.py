from typing import Optional
from pydantic import BaseModel

class CampoBase(BaseModel):
    nombre: Optional[str] = None
    departamento: Optional[str] = None
    tipomanejo: Optional[str] = None
    coordenadas: Optional[str] = None


class CampoCreate(CampoBase):
    pass


class CampoUpdate(CampoBase):
    pass


class CampoResponse(CampoBase):
    campoid: int

    class Config:
        from_attributes = True
