from typing import Optional

from pydantic import BaseModel, ConfigDict


class CultivoBase(BaseModel):
    variedad: Optional[str] = None
    practicasagronomicas: Optional[str] = None
    usofertilizante: Optional[str] = None
    condicionesclimaticas: Optional[str] = None


class CultivoCreate(CultivoBase):
    pass


class CultivoUpdate(BaseModel):
    variedad: Optional[str] = None
    practicasagronomicas: Optional[str] = None
    usofertilizante: Optional[str] = None
    condicionesclimaticas: Optional[str] = None


class CultivoResponse(CultivoBase):
    cultivoid: int

    model_config = ConfigDict(from_attributes=True)
