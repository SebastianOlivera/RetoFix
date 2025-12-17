from sqlalchemy.orm import Session
from sqlalchemy import select, update, delete, func, literal, case

from app.models.campo import Campo  # ajustá el import a tu estructura


def list_with_kmz_flag(db: Session):
    stmt = (
        select(
            Campo.campoid,
            Campo.nombre,
            Campo.departamento,
            Campo.tipomanejo,
            Campo.coordenadas,
            (Campo.archivokmz.is_not(None)).label("tiene_kmz"),
        )
        .order_by(Campo.campoid)
    )

    rows = db.execute(stmt).mappings().all()
    return [dict(r) for r in rows]


def get_one_with_kmz_flag(db: Session, campoid: int):
    stmt = (
        select(
            Campo.campoid,
            Campo.nombre,
            Campo.departamento,
            Campo.tipomanejo,
            Campo.coordenadas,
            (Campo.archivokmz.is_not(None)).label("tiene_kmz"),
        )
        .where(Campo.campoid == campoid)
        .limit(1)
    )

    row = db.execute(stmt).mappings().first()
    return dict(row) if row else None


def get_raw_kmz(db: Session, campoid: int):
    stmt = (
        select(Campo.archivokmz)
        .where(Campo.campoid == campoid)
        .limit(1)
    )
    return db.execute(stmt).scalar_one_or_none()


def set_kmz(db: Session, campoid: int, kmz_value):
    stmt = (
        update(Campo)
        .where(Campo.campoid == campoid)
        .values(archivokmz=kmz_value)
    )
    db.execute(stmt)
    db.commit()


def exists(db: Session, campoid: int) -> bool:
    stmt = select(Campo.campoid).where(Campo.campoid == campoid).limit(1)
    return db.execute(stmt).first() is not None


# ===== CRUD base =====

def create(db: Session, data: dict):
    obj = Campo(
        nombre=data.get("nombre"),
        departamento=data.get("departamento"),
        tipomanejo=data.get("tipomanejo"),
        coordenadas=data.get("coordenadas"),
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)

    # Igual que tu RETURNING (sin archivokmz)
    return {
        "campoid": obj.campoid,
        "nombre": obj.nombre,
        "departamento": obj.departamento,
        "tipomanejo": obj.tipomanejo,
        "coordenadas": obj.coordenadas,
    }


def update_put(db: Session, campoid: int, data: dict):
    # PUT: reemplaza todo
    stmt = (
        update(Campo)
        .where(Campo.campoid == campoid)
        .values(
            nombre=data.get("nombre"),
            departamento=data.get("departamento"),
            tipomanejo=data.get("tipomanejo"),
            coordenadas=data.get("coordenadas"),
            archivokmz=data.get("archivokmz"),
        )
        .returning(
            Campo.campoid,
            Campo.nombre,
            Campo.departamento,
            Campo.tipomanejo,
            Campo.coordenadas,
        )
    )

    row = db.execute(stmt).mappings().first()
    if not row:
        db.rollback()
        raise Exception("Campo no encontrado")

    db.commit()
    return dict(row)


def update_patch(db: Session, campoid: int, data: dict):
    # PATCH: solo campos presentes (evita SQL raw)
    allowed = {"nombre", "departamento", "tipomanejo", "coordenadas", "archivokmz"}
    values = {k: v for k, v in data.items() if k in allowed}

    if not values:
        # nada para actualizar; devolvemos el campo actual (o None)
        return get_one_with_kmz_flag(db, campoid)

    stmt = (
        update(Campo)
        .where(Campo.campoid == campoid)
        .values(**values)
        .returning(
            Campo.campoid,
            Campo.nombre,
            Campo.departamento,
            Campo.tipomanejo,
            Campo.coordenadas,
        )
    )

    row = db.execute(stmt).mappings().first()
    if not row:
        db.rollback()
        raise Exception("Campo no encontrado")

    db.commit()
    return dict(row)


def delete_one(db: Session, campoid: int):
    stmt = delete(Campo).where(Campo.campoid == campoid)
    db.execute(stmt)
    db.commit()
