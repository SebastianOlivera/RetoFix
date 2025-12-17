from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from jwt import ExpiredSignatureError, InvalidTokenError

from app.api.deps import get_db
from app.core.auth import ACCESS_TOKEN_MINUTES, crear_token, verificar_token
from app.schemas import (
    TokenResponse,
    TokenValidationRequest,
    TokenValidationResult,
    UsuarioLogin,
)
from app.services import usuario_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: UsuarioLogin, db: Session = Depends(get_db)):
    user = usuario_service.authenticate(db, payload.mail, payload.password)
    claims = {"sub": str(user.usuarioid), "mail": user.mail, "rol": user.rol}
    token = crear_token(claims)
    return TokenResponse(
        access_token=token,
        expires_in=ACCESS_TOKEN_MINUTES * 60 * 1000,
    )


@router.post("/validate", response_model=TokenValidationResult)
def validate_token(body: TokenValidationRequest):
    try:
        payload = verificar_token(body.token)
    except ExpiredSignatureError:
        return TokenValidationResult(valid=False, reason="Token expirado")
    except InvalidTokenError:
        return TokenValidationResult(valid=False, reason="Token invalido")
    return TokenValidationResult(valid=True, payload=payload)
