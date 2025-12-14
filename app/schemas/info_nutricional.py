from typing import Optional
from pydantic import BaseModel


class InfoNutricionalBase(BaseModel):
    producto: Optional[str] = None
    porcion: Optional[str] = None
    calorias: Optional[str] = None
    proteinas: Optional[str] = None
    grasas: Optional[str] = None
    carbohidratos: Optional[str] = None
    sodio: Optional[str] = None


class InfoNutricionalCreate(InfoNutricionalBase):
    pass


class InfoNutricionalUpdate(InfoNutricionalBase):
    pass


class InfoNutricionalResponse(InfoNutricionalBase):
    infoid: int

    class Config:
        from_attributes = True
