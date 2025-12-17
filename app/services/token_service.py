from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.models.token_revocado import TokenRevocado

USER_SCOPE_PREFIX = "user:"


def _as_datetime(value: datetime | float | int | None) -> datetime | None:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if value is None:
        return None
    try:
        return datetime.fromtimestamp(float(value), tz=timezone.utc)
    except (TypeError, ValueError):
        return None


def _cleanup_if_expired(db: Session, record: TokenRevocado) -> bool:
    if record.expirado():
        db.delete(record)
        db.commit()
        return True
    return False


def _get_by_jti(db: Session, jti: str) -> TokenRevocado | None:
    return db.query(TokenRevocado).filter(TokenRevocado.jti == jti).first()


def _get_user_scope_record(db: Session, usuario_id: int | None) -> TokenRevocado | None:
    if not usuario_id:
        return None
    return _get_by_jti(db, f"{USER_SCOPE_PREFIX}{usuario_id}")


def is_token_revoked(
    db: Session,
    jti: str,
    *,
    usuario_id: Optional[int] = None,
    issued_at: datetime | float | int | None = None,
) -> bool:
    issued_at_dt = _as_datetime(issued_at)

    if jti:
        record = _get_by_jti(db, jti)
        if record and not _cleanup_if_expired(db, record):
            return True

    user_record = _get_user_scope_record(db, usuario_id)
    if user_record and not _cleanup_if_expired(db, user_record):
        if issued_at_dt is None or issued_at_dt <= user_record.created_at:
            return True
    return False


def revoke_token(
    db: Session,
    *,
    jti: str,
    usuario_id: int | None = None,
    expires_at: datetime | None = None,
    ) -> TokenRevocado:
    if not jti:
        raise ValueError("Se requiere el identificador unico del token (jti)")

    record = _get_by_jti(db, jti)
    if record:
        record.usuario_id = usuario_id or record.usuario_id
        record.expires_at = expires_at or record.expires_at
    else:
        record = TokenRevocado(
            jti=jti,
            usuario_id=usuario_id,
            expires_at=expires_at,
            created_at=datetime.now(timezone.utc),
        )
        db.add(record)
    db.commit()
    db.refresh(record)
    return record


def revoke_user_tokens(
    db: Session, *, usuario_id: int, until: datetime | float | int | None = None
) -> TokenRevocado:
    if not usuario_id:
        raise ValueError("Se requiere el identificador de usuario para revocar sus tokens")

    expires_at = _as_datetime(until)
    record = _get_user_scope_record(db, usuario_id)
    if record:
        record.expires_at = expires_at or record.expires_at
        record.created_at = datetime.now(timezone.utc)
    else:
        record = TokenRevocado(
            jti=f"{USER_SCOPE_PREFIX}{usuario_id}",
            usuario_id=usuario_id,
            expires_at=expires_at,
            created_at=datetime.now(timezone.utc),
        )
        db.add(record)
    db.commit()
    db.refresh(record)
    return record
