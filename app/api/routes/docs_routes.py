from uuid import UUID
from fastapi import APIRouter, Depends, UploadFile, File, Query, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.document import DocumentOut, DocumentListOut
from app.services import document_service

router = APIRouter(prefix="", tags=["Docs"])

@router.get("/get_docs", response_model=DocumentListOut)
def get_docs(
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    docs, total = document_service.list_docs(db, limit, offset)
    return {"results": docs, "total": total}

@router.get("/get_single_doc/{id}", response_model=DocumentOut)
def get_single_doc(id: UUID, db: Session = Depends(get_db)):
    doc = document_service.get_doc(db, id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return doc

@router.get("/get/{id}/doc")
def get_pdf(id: UUID, download: bool = False):
    raise HTTPException(status_code=501, detail="MinIO no implementado aún")

@router.post("/create_doc", response_model=DocumentOut)
def create_doc(
    filename: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Solo PDFs")

    minio_path = f"docs/{file.filename}"

    doc = document_service.create_doc(db, filename, minio_path)
    return doc

@router.delete("/delete_doc/{id}", response_model=DocumentOut)
def delete_doc(id: UUID, db: Session = Depends(get_db)):
    doc = document_service.get_doc(db, id)
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado")

    document_service.delete_doc(db, doc)
    return doc
