from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

router = APIRouter(prefix="/qr", tags=["QR"])


@router.get("/productos/{producto_id}/lotes/{lote_id}")
def obtener_payload_qr(producto_id: int, lote_id: int, db: Session = Depends(get_db)):
    """
    Devuelve el payload QR con la información del producto, lote,
    info nutricional y control de calidad sin depender de los modelos ORM.
    """
    stmt = text(
        """
        SELECT
            p.productoid,
            p.nombrecomercial,
            p.descripcion,
            p.imagenurl,
            p.categoria,
            p.porciones,
            p.mododeuso,
            p.pdfurl,
            p.claim,
            l.loteid,
            l.fechasiembra,
            l.fechacosecha,
            l.fechaprocesamiento,
            l.fechavencimiento,
            info.*,
            qc.controlcalidadid,
            qc.loteid AS qc_loteid,
            qc.pdfurl AS qc_pdfurl,
            qc.resumenresultados,
            qc.responsable
        FROM producto p
        JOIN productolotepertenece pl ON pl.productoid = p.productoid
        JOIN lote l ON pl.loteid = l.loteid
        -- La columna real en info_nutricional es "producto" y está como texto; casteamos a INT para comparar
        LEFT JOIN info_nutricional info ON info.producto::int = p.productoid
        LEFT JOIN control_de_calidad qc ON qc.loteid = l.loteid
        WHERE pl.productoid = :producto_id AND pl.loteid = :lote_id
        LIMIT 1
        """
    )

    row = db.execute(stmt, {"producto_id": producto_id, "lote_id": lote_id}).mappings().first()
    if not row:
        raise HTTPException(status_code=404, detail="No se encontró información para ese producto/lote")

    payload = {
        "producto": {
            "productoid": row["productoid"],
            "nombrecomercial": row["nombrecomercial"],
            "descripcion": row["descripcion"],
            "imagenurl": row["imagenurl"],
            "categoria": row["categoria"],
            "porciones": row["porciones"],
            "mododeuso": row["mododeuso"],
            "pdfurl": row["pdfurl"],
            "claim": row["claim"],
        },
        "lote": {
            "loteid": row["loteid"],
            "fechasiembra": row["fechasiembra"],
            "fechacosecha": row["fechacosecha"],
            "fechaprocesamiento": row["fechaprocesamiento"],
            "fechavencimiento": row["fechavencimiento"],
        },
    }

    def pick(key_options: list[str]):
        for key in key_options:
            if key in row and row[key] is not None:
                return row[key]
        return None

    info_id = pick(["infonutricionalid", "infonutricional_id", "infonutricionalid"])
    info_producto = pick(["info_producto", "producto", "productoid"])

    has_info = any(
        pick([col])
        is not None
        for col in ["calorias", "proteinas", "grasas", "carbohidratos", "vitaminas", "minerales", "beneficios"]
    )

    if info_id is not None or has_info:
        payload["info_nutricional"] = {
            "infonutricionalid": info_id,
            "productoid": info_producto,
            "calorias": pick(["calorias"]),
            "proteinas": pick(["proteinas"]),
            "grasas": pick(["grasas"]),
            "carbohidratos": pick(["carbohidratos"]),
            "vitaminas": pick(["vitaminas"]),
            "minerales": pick(["minerales"]),
            "beneficios": pick(["beneficios"]),
        }

    if row["controlcalidadid"] is not None:
        payload["control_de_calidad"] = {
            "controlcalidadid": row["controlcalidadid"],
            "loteid": row["qc_loteid"],
            "pdfurl": row["qc_pdfurl"],
            "resumenresultados": row["resumenresultados"],
            "responsable": row["responsable"],
        }

    return payload
