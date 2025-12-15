from typing import Optional

from pydantic import BaseModel


class CodigoQRResponse(BaseModel):
    id: int
    qr_id: str
    lote_id: int
    qr_image_path: Optional[str]

    class Config:
        from_attributes = True
