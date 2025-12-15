from typing import Optional

from pydantic import BaseModel


class ControlCalidadBase(BaseModel):
    loteid: int
    pdfurl: Optional[str] = None
    resumenresultados: Optional[str] = None
    responsable: Optional[str] = None


class ControlCalidadCreate(ControlCalidadBase):
    pass


class ControlCalidadUpdate(BaseModel):
    loteid: Optional[int] = None
    pdfurl: Optional[str] = None
    resumenresultados: Optional[str] = None
    responsable: Optional[str] = None


class ControlCalidadResponse(ControlCalidadBase):
    controlcalidadid: int

    class Config:
        from_attributes = True
