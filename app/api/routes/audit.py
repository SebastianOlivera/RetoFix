from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user, get_db
from app.schemas import ActionLogCreate, ActionLogResponse
from app.services import audit_service

router = APIRouter(
    prefix="/audit",
    tags=["Audit"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/logs", response_model=list[ActionLogResponse])
def listar_logs(
    usuario_id: int | None = None,
    limit: int = Query(default=100, le=500),
    db: Session = Depends(get_db),
):
    return audit_service.list_logs(db, usuario_id=usuario_id, limit=limit)


@router.post(
    "/logs",
    response_model=ActionLogResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_log(payload: ActionLogCreate, db: Session = Depends(get_db)):
    return audit_service.manual_log(db, payload)
