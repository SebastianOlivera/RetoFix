from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field


class UsuarioBase(BaseModel):
    mail: EmailStr
    rol: str


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioUpdatePut(UsuarioCreate):
    pass


class UsuarioPatch(BaseModel):
    mail: Optional[EmailStr] = None
    rol: Optional[str] = None
    password: Optional[str] = None


class UsuarioOut(UsuarioBase):
    usuarioid: int


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

class ProductoResponse(BaseModel):
    productoid: int
    nombrecomercial: str
    descripcion: Optional[str] = None
    imagenurl: Optional[str] = None
    categoria: Optional[str] = None
    porciones: Optional[int] = None
    mododeuso: Optional[str] = None
    pdfurl: Optional[str] = None
    claim: Optional[str] = None
    claims: List[str] = Field(default_factory=list)



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


class CodigoQRResponse(BaseModel):
    id: int
    qr_id: str
    lote_id: int
    qr_image_path: Optional[str]

    class Config:
        from_attributes = True

# app/schemas/schemas.py
from typing import Optional
from pydantic import BaseModel

class CampoBase(BaseModel):
    nombre: str
    departamento: str
    tipomanejo: str
    coordenadas: str
    archivokmz: Optional[str] = None

class CampoCreate(CampoBase):
    pass

class CampoUpdate(BaseModel):
    nombre: Optional[str] = None
    departamento: Optional[str] = None
    tipomanejo: Optional[str] = None
    coordenadas: Optional[str] = None
    archivokmz: Optional[str] = None

class CampoOut(CampoBase):
    campoid: int

    class Config:
        from_attributes = True
