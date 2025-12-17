from collections.abc import Generator

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from sqlalchemy.orm import Session

from app.core.auth import verificar_token
from app.db.connection import SessionLocal
from app.services import usuario_service

_bearer = HTTPBearer(auto_error=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    db: Session = Depends(get_db),
):
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticacion requerida",
        )

    token = credentials.credentials
    try:
        payload = verificar_token(token)
    except ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expirado"
        ) from exc
    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido"
        ) from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token sin identificador de usuario",
        )

    try:
        user_id_int = int(user_id)
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token con identificador invalido",
        ) from exc

    user = usuario_service.get_by_id(db, user_id_int)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado"
        )

    request.state.user = user
    request.state.token_payload = payload
    return user
