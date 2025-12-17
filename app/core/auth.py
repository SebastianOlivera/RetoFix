import base64
import binascii
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Iterable, Optional

import jwt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY no esta definido en el entorno")

ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = int(os.getenv("ACCESS_TOKEN_MINUTES", "60"))

AES_KEY_B64 = os.getenv("AES_KEY")
if not AES_KEY_B64:
    raise ValueError("AES_KEY no esta definido en el entorno")

try:
    AES_KEY = base64.urlsafe_b64decode(AES_KEY_B64)
except (binascii.Error, ValueError) as exc:
    raise ValueError("AES_KEY debe estar codificado en base64 url-safe") from exc

if len(AES_KEY) != 32:
    raise ValueError("AES_KEY debe representar exactamente 32 bytes (AES-256)")

NONCE_SIZE = 12
SECURE_PAYLOAD_FIELD = "secure_payload"


def _encrypt_sensitive_data(data: Dict[str, str]) -> str:
    aesgcm = AESGCM(AES_KEY)
    nonce = os.urandom(NONCE_SIZE)
    plaintext = json.dumps(data).encode("utf-8")
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    blob = nonce + ciphertext
    return base64.urlsafe_b64encode(blob).decode("ascii")


def _decrypt_sensitive_data(blob: str) -> Dict[str, str]:
    raw = base64.urlsafe_b64decode(blob.encode("ascii"))
    nonce, ciphertext = raw[:NONCE_SIZE], raw[NONCE_SIZE:]
    aesgcm = AESGCM(AES_KEY)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return json.loads(plaintext.decode("utf-8"))


def _extract_sensitive_fields(
    payload: Dict[str, Any], sensitive_fields: Optional[Iterable[str]]
) -> Dict[str, str]:
    if not sensitive_fields:
        return {}
    extracted: Dict[str, str] = {}
    for field in sensitive_fields:
        if field in payload:
            extracted[field] = payload.pop(field)
    return extracted


def crear_token(
    data: Dict[str, Any],
    exp_minutes: Optional[int] = None,
    sensitive_fields: Optional[Iterable[str]] = None,
) -> str:
    """Crea un JWT y cifra campos sensibles antes de firmarlo."""
    to_encode = data.copy()
    minutes = exp_minutes if exp_minutes is not None else ACCESS_TOKEN_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    to_encode.update({"exp": expire})

    sensitive_data = _extract_sensitive_fields(to_encode, sensitive_fields)
    if sensitive_data:
        to_encode[SECURE_PAYLOAD_FIELD] = _encrypt_sensitive_data(sensitive_data)

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verificar_token(
    token: str, reintegrar_sensibles: bool = True
) -> Dict[str, Any]:
    """Valida la firma HS256 y descifra los campos sensibles si existen."""
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    blob = payload.pop(SECURE_PAYLOAD_FIELD, None)
    if reintegrar_sensibles and blob:
        payload.update(_decrypt_sensitive_data(blob))
    elif blob:
        payload[SECURE_PAYLOAD_FIELD] = blob

    return payload
