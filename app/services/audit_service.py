from typing import Optional

from sqlalchemy.orm import Session

from app.models.audit_log import UserActionLog
from app.schemas import ActionLogCreate


def log_action(
    db: Session,
    *,
    usuario_id: int,
    path: str,
    method: str,
    status_code: int,
    action: Optional[str] = None,
    client_ip: Optional[str] = None,
    user_agent: Optional[str] = None,
    payload: Optional[str] = None,
) -> UserActionLog:
    log = UserActionLog(
        usuario_id=usuario_id,
        path=path,
        method=method,
        status_code=status_code,
        action=action,
        client_ip=client_ip,
        user_agent=user_agent,
        payload=payload,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def manual_log(db: Session, payload: ActionLogCreate) -> UserActionLog:
    return log_action(
        db,
        usuario_id=payload.usuario_id,
        path=payload.path,
        method=payload.method,
        status_code=payload.status_code,
        action=payload.action,
        client_ip=payload.client_ip,
        user_agent=payload.user_agent,
        payload=payload.payload,
    )


def list_logs(
    db: Session,
    usuario_id: Optional[int] = None,
    limit: int = 100,
) -> list[UserActionLog]:
    query = db.query(UserActionLog)
    if usuario_id is not None:
        query = query.filter(UserActionLog.usuario_id == usuario_id)
    return query.order_by(UserActionLog.created_at.desc()).limit(limit).all()
