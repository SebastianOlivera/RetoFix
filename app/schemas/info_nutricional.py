from typing import Optional

from pydantic import BaseModel


class InfoNutricionalBase(BaseModel):
    productoid: int
    calorias: Optional[float] = None
    proteinas: Optional[float] = None
    grasas: Optional[float] = None
    carbohidratos: Optional[float] = None
    vitaminas: Optional[str] = None
    minerales: Optional[str] = None
    beneficios: Optional[str] = None


class InfoNutricionalCreate(InfoNutricionalBase):
    pass


class InfoNutricionalUpdate(BaseModel):
    productoid: Optional[int] = None
    calorias: Optional[float] = None
    proteinas: Optional[float] = None
    grasas: Optional[float] = None
    carbohidratos: Optional[float] = None
    vitaminas: Optional[str] = None
    minerales: Optional[str] = None
    beneficios: Optional[str] = None


class InfoNutricionalResponse(InfoNutricionalBase):
    infonutricionalid: int

    class Config:
        from_attributes = True
