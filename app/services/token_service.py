from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.token_revocado import TokenRevocado


def _cleanup_if_expired(db: Session, record: TokenRevocado) -> bool:
    if record.expirado():
        db.delete(record)
        db.commit()
        return True
    return False


def is_token_revoked(db: Session, jti: str) -> bool:
    if not jti:
        return False
    record = db.query(TokenRevocado).filter(TokenRevocado.jti == jti).first()
    if not record:
        return False
    return not _cleanup_if_expired(db, record)


def revoke_token(
    db: Session,
    *,
    jti: str,
    usuario_id: int | None = None,
    expires_at: datetime | None = None,
) -> TokenRevocado:
    if not jti:
        raise ValueError("Se requiere el identificador unico del token (jti)")

    record = db.query(TokenRevocado).filter(TokenRevocado.jti == jti).first()
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
