from datetime import date
from typing import Optional

from pydantic import BaseModel


class LoteCreate(BaseModel):
    fechasiembra: Optional[date] = None
    fechacosecha: Optional[date] = None
    fechaprocesamiento: Optional[date] = None
    fechavencimiento: Optional[date] = None


class LoteUpdate(BaseModel):
    fechasiembra: Optional[date] = None
    fechacosecha: Optional[date] = None
    fechaprocesamiento: Optional[date] = None
    fechavencimiento: Optional[date] = None


class LoteResponse(BaseModel):
    loteid: int
    fechasiembra: Optional[date]
    fechacosecha: Optional[date]
    fechaprocesamiento: Optional[date]
    fechavencimiento: Optional[date]

    class Config:
        from_attributes = True
