from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

class DocumentOut(BaseModel):
    id: UUID
    filename: str
    minio_path: str
    uploaded_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DocumentListOut(BaseModel):
    results: list[DocumentOut]
    total: int
