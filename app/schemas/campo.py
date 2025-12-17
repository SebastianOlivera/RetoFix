from typing import Optional
from pydantic import BaseModel, ConfigDict


class CampoBase(BaseModel):
    nombre: str
    departamento: str
    tipomanejo: str
    coordenadas: str


class CampoCreate(CampoBase):
    pass


class CampoUpdatePut(CampoBase):
    pass


class CampoPatch(BaseModel):
    nombre: Optional[str] = None
    departamento: Optional[str] = None
    tipomanejo: Optional[str] = None
    coordenadas: Optional[str] = None


class CampoResponse(CampoBase):
    campoid: int
    tiene_kmz: bool = False

    model_config = ConfigDict(from_attributes=True)
