from sqlalchemy.orm import Session
from app.models.lote import Lote
from app.schemas.lote import LoteCreate,LoteUpdate, LoteResponse

def create_Lote(db: Session, data: LoteCreate):
    lote=Lote(
        campoid=data.campoid,
        fechasiembra=data.fechasiembra,
        fechacosecha=data.fechacosecha,
        fechaprocesamiento=data.fechaprocesamiento,
        fechavencimiento=data.fechavencimiento,
    )
    db.add(lote)
    db.commit()
    db.refresh(lote)
    return lote

def get_lotes(db: Session):
    return db.query(Lote).all()


def get_lote_by_id(db: Session, lote_id: int):
    return db.query(Lote).filter(Lote.loteid == lote_id).first()


def update_lote(db: Session, lote: Lote, data: LoteUpdate):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(lote, field, value)
    db.commit()
    db.refresh(lote)
    return lote




def delete_lote(db: Session, lote: Lote):
    db.delete(lote)
    db.commit()