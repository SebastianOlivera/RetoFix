from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from jwt import ExpiredSignatureError, InvalidTokenError

from app.api.dependencies import get_current_user, get_db
from app.core.auth import ACCESS_TOKEN_MINUTES, crear_token, verificar_token
from app.schemas import (
    TokenResponse,
    TokenValidationRequest,
    TokenValidationResult,
    UsuarioLogin,
)
from app.services import token_service, usuario_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=TokenResponse)
def login(payload: UsuarioLogin, db: Session = Depends(get_db)):
    try:
        user = usuario_service.authenticate(db, payload.mail, payload.password)
    except HTTPException as exc:
        if exc.status_code == status.HTTP_401_UNAUTHORIZED:
            raise
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
    except Exception as exc:  # pragma: no cover - unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al iniciar sesion",
        ) from exc

    token_service.revoke_user_tokens(db, usuario_id=user.usuarioid)
    claims = {"sub": str(user.usuarioid), "mail": user.mail, "rol": user.rol}
    token = crear_token(claims)
    return TokenResponse(
        access_token=token,
        expires_in=ACCESS_TOKEN_MINUTES * 60 * 1000,
    )


@router.post("/logout")
def logout(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    token_payload = getattr(request.state, "token_payload", {}) or {}
    jti = token_payload.get("jti")
    if not jti:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El token no contiene identificador unico",
        )

    exp = token_payload.get("exp")
    expires_at = None
    if exp:
        try:
            expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)
        except (TypeError, ValueError):
            expires_at = None

    token_service.revoke_token(
        db, jti=jti, usuario_id=getattr(user, "usuarioid", None), expires_at=expires_at
    )
    return {"detail": "Sesion cerrada correctamente"}


@router.post("/validate", response_model=TokenValidationResult)
def validate_token(body: TokenValidationRequest, db: Session = Depends(get_db)):
    try:
        payload = verificar_token(body.token)
    except ExpiredSignatureError:
        return TokenValidationResult(valid=False, reason="Token expirado")
    except InvalidTokenError:
        return TokenValidationResult(valid=False, reason="Token invalido")
    user_id = payload.get("sub")
    try:
        user_id_int = int(user_id) if user_id is not None else None
    except (TypeError, ValueError):
        user_id_int = None

    if token_service.is_token_revoked(
        db,
        payload.get("jti"),
        usuario_id=user_id_int,
        issued_at=payload.get("iat"),
    ):
        return TokenValidationResult(valid=False, reason="Token revocado")
    return TokenValidationResult(valid=True, payload=payload)
