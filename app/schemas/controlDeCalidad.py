from typing import Optional

from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)
