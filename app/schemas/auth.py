from typing import Any

from pydantic import BaseModel, EmailStr


class UsuarioLogin(BaseModel):
    mail: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    expires_in: int
    token_type: str = "bearer"


class TokenValidationRequest(BaseModel):
    token: str


class TokenValidationResult(BaseModel):
    valid: bool
    reason: str | None = None
    payload: dict[str, Any] | None = None
