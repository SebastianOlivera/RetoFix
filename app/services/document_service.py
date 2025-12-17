import uuid
from sqlalchemy.orm import Session
from app.models.document import Document

# Acá después conectás MinIO real
def list_docs(db: Session, limit: int, offset: int):
    query = db.query(Document)
    total = query.count()
    docs = query.offset(offset).limit(limit).all()
    return docs, total


def get_doc(db: Session, doc_id: uuid.UUID):
    return db.get(Document, doc_id)


def create_doc(db: Session, filename: str, minio_path: str):
    doc = Document(
        filename=filename,
        minio_path=minio_path,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def delete_doc(db: Session, doc: Document):
    db.delete(doc)
    db.commit()
