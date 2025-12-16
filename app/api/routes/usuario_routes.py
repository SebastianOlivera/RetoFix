from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas import UsuarioCreate, UsuarioOut, UsuarioUpdatePut, UsuarioPatch
from app.services import usuario_service

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=UsuarioOut, status_code=201)
def crear_usuario(payload: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        return usuario_service.create(db, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[UsuarioOut])
def listar_usuarios(db: Session = Depends(get_db)):
    return usuario_service.list_all(db)

@router.get("/{usuario_id}", response_model=UsuarioOut)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    u = usuario_service.get_by_id(db, usuario_id)
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return u

@router.put("/{usuario_id}", response_model=UsuarioOut)
def reemplazar_usuario(usuario_id: int, payload: UsuarioUpdatePut, db: Session = Depends(get_db)):
    try:
        u = usuario_service.update_put(db, usuario_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return u

@router.patch("/{usuario_id}", response_model=UsuarioOut)
def actualizar_parcial(usuario_id: int, payload: UsuarioPatch, db: Session = Depends(get_db)):
    try:
        u = usuario_service.patch(db, usuario_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return u

@router.delete("/{usuario_id}", status_code=204)
def borrar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    ok = usuario_service.delete(db, usuario_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None
