from typing import Optional

from pydantic import BaseModel, ConfigDict


class CodigoQRResponse(BaseModel):
    id: int
    qr_id: str
    lote_id: int
    qr_image_path: Optional[str]

    model_config = ConfigDict(from_attributes=True)
