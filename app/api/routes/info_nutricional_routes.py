from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.api.dependencies import get_db, get_current_user
from app.schemas.info_nutricional import (
    InfoNutricionalCreate,
    InfoNutricionalUpdate,
    InfoNutricionalResponse,
)
from app.services import info_nutricional_service

router = APIRouter(
    prefix="/info-nutricional",
    tags=["Info Nutricional"],
    dependencies=[Depends(get_current_user)],
)

@router.post("/", response_model=InfoNutricionalResponse, status_code=status.HTTP_201_CREATED)
def crear_info_nutricional(payload: InfoNutricionalCreate, db: Session = Depends(get_db)):
    try:
        return info_nutricional_service.create_info_nutricional(db, payload)
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e).lower()
        if "unique constraint" in error_msg or "duplicate key" in error_msg:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe información nutricional para el producto con ID {payload.productoid}"
            )
        elif "foreign key" in error_msg or "violates foreign key constraint" in error_msg:
            raise HTTPException(
                status_code=400,
                detail=f"El producto con ID {payload.productoid} no existe. Debe crear el producto primero."
            )
        raise HTTPException(status_code=400, detail=f"Error de integridad en la base de datos: {str(e.orig)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


@router.get("/", response_model=List[InfoNutricionalResponse])
def listar_info_nutricional(db: Session = Depends(get_db)):
    try:
        return info_nutricional_service.get_info_nutricional(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al listar información nutricional: {str(e)}")


@router.get("/{info_id}", response_model=InfoNutricionalResponse)
def obtener_info_nutricional(info_id: int, db: Session = Depends(get_db)):
    try:
        info = info_nutricional_service.get_info_nutricional_by_id(db, info_id)
        if not info:
            raise HTTPException(status_code=404, detail="Informacion nutricional no encontrada")
        return info
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener información nutricional: {str(e)}")


@router.put("/{info_id}", response_model=InfoNutricionalResponse)
def actualizar_info_nutricional(info_id: int, payload: InfoNutricionalUpdate, db: Session = Depends(get_db)):
    try:
        info = info_nutricional_service.get_info_nutricional_by_id(db, info_id)
        if not info:
            raise HTTPException(status_code=404, detail="Informacion nutricional no encontrada")
        return info_nutricional_service.update_info_nutricional(db, info, payload)
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e).lower()
        if "unique constraint" in error_msg or "duplicate key" in error_msg:
            raise HTTPException(status_code=400, detail="Ya existe información nutricional para ese producto")
        elif "foreign key" in error_msg:
            raise HTTPException(status_code=400, detail="El producto especificado no existe")
        raise HTTPException(status_code=400, detail=f"Error de integridad: {str(e.orig)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar información nutricional: {str(e)}")


@router.patch("/{info_id}", response_model=InfoNutricionalResponse)
def actualizar_info_nutricional_parcial(info_id: int, payload: InfoNutricionalUpdate, db: Session = Depends(get_db)):
    try:
        info = info_nutricional_service.get_info_nutricional_by_id(db, info_id)
        if not info:
            raise HTTPException(status_code=404, detail="Informacion nutricional no encontrada")
        return info_nutricional_service.update_info_nutricional(db, info, payload)
    except HTTPException:
        raise
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e).lower()
        if "unique constraint" in error_msg or "duplicate key" in error_msg:
            raise HTTPException(status_code=400, detail="Ya existe información nutricional para ese producto")
        elif "foreign key" in error_msg:
            raise HTTPException(status_code=400, detail="El producto especificado no existe")
        raise HTTPException(status_code=400, detail=f"Error de integridad: {str(e.orig)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al actualizar información nutricional: {str(e)}")


@router.delete("/{info_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_info_nutricional(info_id: int, db: Session = Depends(get_db)):
    try:
        info = info_nutricional_service.get_info_nutricional_by_id(db, info_id)
        if not info:
            raise HTTPException(status_code=404, detail="Informacion nutricional no encontrada")
        info_nutricional_service.delete_info_nutricional(db, info)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al eliminar información nutricional: {str(e)}")
