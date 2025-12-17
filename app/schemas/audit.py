from datetime import datetime

from pydantic import BaseModel


class ActionLogBase(BaseModel):
    usuario_id: int
    path: str
    method: str
    status_code: int
    action: str | None = None
    client_ip: str | None = None
    user_agent: str | None = None
    payload: str | None = None


class ActionLogCreate(ActionLogBase):
    pass


class ActionLogResponse(ActionLogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
