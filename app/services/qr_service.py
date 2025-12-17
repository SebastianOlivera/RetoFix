import qrcode
import uuid
from io import BytesIO
from pathlib import Path

import qrcode


def generar_qr_id_unico() -> str:
    """
    Genera un identificador único para el código QR.
    Formato: QR-XXXXXXXX (8 caracteres alfanuméricos)

    Returns:
        str: Identificador único
    """
    return f"QR-{uuid.uuid4().hex[:8].upper()}"


def guardar_qr_en_disco(qr_id: str, texto: str, directorio: str = "qr_codes") -> str:
    """
    Genera y guarda un código QR en disco.

    Args:
        qr_id: Identificador único del QR
        texto: Texto a codificar (ej: URL del producto)
        directorio: Directorio donde guardar las imágenes

    Returns:
        str: Ruta relativa del archivo guardado
    """
    # Crear directorio si no existe
    Path(directorio).mkdir(exist_ok=True)

    # Generar QR
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(texto)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar archivo
    filename = f"{qr_id}.png"
    filepath = Path(directorio) / filename
    img.save(str(filepath))

    return str(filepath)

