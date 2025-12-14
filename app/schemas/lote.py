from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date



class LoteCreate(BaseModel):
    campoid: int
    fechasiembra: Optional[date] = None
    fechacosecha: Optional[date] = None
    fechaprocesamiento: Optional[date] = None
    fechavencimiento: Optional[date] = None

class LoteUpdate(BaseModel): 
    campoid: Optional[int] = None
    fechasiembra: Optional[date] = None
    fechacosecha: Optional[date] = None
    fechaprocesamiento: Optional[date] = None
    fechavencimiento: Optional[date] = None

class LoteResponse(BaseModel):
    loteid: int
    campoid: int
    fechasiembra: Optional[date]
    fechacosecha: Optional[date]
    fechaprocesamiento: Optional[date]
    fechavencimiento: Optional[date]
    