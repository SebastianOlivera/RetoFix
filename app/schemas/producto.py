from typing import List, Optional

from pydantic import BaseModel, Field


class ProductoCreate(BaseModel):
    nombrecomercial: str
    descripcion: Optional[str] = None
    imagenurl: Optional[str] = None
    categoria: Optional[str] = None
    porciones: Optional[int] = None
    mododeuso: Optional[str] = None
    pdfurl: Optional[str] = None
    claim: Optional[str] = None  # "a;b;c"


class ProductoUpdate(BaseModel):
    nombrecomercial: Optional[str] = None
    descripcion: Optional[str] = None
    imagenurl: Optional[str] = None
    categoria: Optional[str] = None
    porciones: Optional[int] = None
    mododeuso: Optional[str] = None
    pdfurl: Optional[str] = None
    claim: Optional[str] = None


class ProductoUpdatePut(BaseModel):
    nombrecomercial: str
    descripcion: Optional[str] = None
    imagenurl: Optional[str] = None
    categoria: Optional[str] = None
    porciones: Optional[int] = None
    mododeuso: Optional[str] = None
    pdfurl: Optional[str] = None
    claim: Optional[str] = None


class ProductoResponse(BaseModel):
    productoid: int
    nombrecomercial: str
    descripcion: Optional[str] = None
    imagenurl: Optional[str] = None
    imagenurl_firmada: Optional[str] = None
    categoria: Optional[str] = None
    porciones: Optional[int] = None
    mododeuso: Optional[str] = None
    pdfurl: Optional[str] = None
    claim: Optional[str] = None
    claims: List[str] = Field(default_factory=list)

    class Config:
        from_attributes = True
