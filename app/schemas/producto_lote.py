from pydantic import BaseModel


class ProductoLoteRespuesta(BaseModel):
    productoid: int
    loteid: int


class ProductoLoteCambio(BaseModel):
    nuevo_productoid: int
    nuevo_loteid: int
