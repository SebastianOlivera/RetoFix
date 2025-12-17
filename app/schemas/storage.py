from pydantic import BaseModel


class PresignedPutRequest(BaseModel):
    file: str


class PresignedUrlResponse(BaseModel):
    url: str
