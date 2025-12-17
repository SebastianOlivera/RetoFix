from sqlalchemy.orm import Session
from sqlalchemy import text


def list_with_kmz_flag(db: Session):
    sql = text("""
        SELECT
            campoid,
            nombre,
            departamento,
            tipomanejo,
            coordenadas,
            (archivokmz IS NOT NULL) AS tiene_kmz
        FROM campo
        ORDER BY campoid
    """)
    rows = db.execute(sql).mappings().all()
    return [dict(r) for r in rows]


def get_one_with_kmz_flag(db: Session, campoid: int):
    sql = text("""
        SELECT
            campoid,
            nombre,
            departamento,
            tipomanejo,
            coordenadas,
            (archivokmz IS NOT NULL) AS tiene_kmz
        FROM campo
        WHERE campoid = :campoid
        LIMIT 1
    """)
    row = db.execute(sql, {"campoid": campoid}).mappings().first()
    return dict(row) if row else None


def get_raw_kmz(db: Session, campoid: int):
    sql = text("SELECT archivokmz FROM campo WHERE campoid = :campoid LIMIT 1")
    return db.execute(sql, {"campoid": campoid}).scalar()


def set_kmz(db: Session, campoid: int, kmz_value):
    sql = text("UPDATE campo SET archivokmz = :kmz WHERE campoid = :campoid")
    db.execute(sql, {"kmz": kmz_value, "campoid": campoid})
    db.commit()


def exists(db: Session, campoid: int) -> bool:
    sql = text("SELECT 1 FROM campo WHERE campoid = :campoid LIMIT 1")
    return db.execute(sql, {"campoid": campoid}).scalar() is not None


# ===== CRUD base =====

def create(db: Session, data: dict):
    sql = text("""
        INSERT INTO campo (nombre, departamento, tipomanejo, coordenadas)
        VALUES (:nombre, :departamento, :tipomanejo, :coordenadas)
        RETURNING campoid, nombre, departamento, tipomanejo, coordenadas
    """)
    row = db.execute(sql, data).mappings().first()
    db.commit()
    return dict(row)


def update_put(db: Session, campoid: int, data: dict):
    data["campoid"] = campoid
    sql = text("""
        UPDATE campo
        SET nombre=:nombre,
            departamento=:departamento,
            tipomanejo=:tipomanejo,
            coordenadas=:coordenadas,
            archivokmz=:archivokmz
        WHERE campoid=:campoid
        RETURNING campoid, nombre, departamento, tipomanejo, coordenadas
    """)
    row = db.execute(sql, data).mappings().first()
    if not row:
        raise Exception("Campo no encontrado")
    db.commit()
    return dict(row)


def update_patch(db: Session, campoid: int, data: dict):
    sets = ", ".join(f"{k}=:{k}" for k in data.keys())
    data["campoid"] = campoid

    sql = text(f"""
        UPDATE campo
        SET {sets}
        WHERE campoid=:campoid
        RETURNING campoid, nombre, departamento, tipomanejo, coordenadas
    """)
    row = db.execute(sql, data).mappings().first()
    if not row:
        raise Exception("Campo no encontrado")
    db.commit()
    return dict(row)


def delete(db: Session, campoid: int):
    sql = text("DELETE FROM campo WHERE campoid = :campoid")
    db.execute(sql, {"campoid": campoid})
    db.commit()
