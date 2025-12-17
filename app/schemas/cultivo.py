from typing import Optional

from pydantic import BaseModel


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

    class Config:
        from_attributes = True
