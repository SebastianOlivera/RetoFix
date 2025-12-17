import base64
import os

# Configure minimal secrets so route module imports succeed during tests
os.environ.setdefault("SECRET_KEY", "test-secret")
os.environ.setdefault("AES_KEY", base64.urlsafe_b64encode(b"0" * 32).decode("ascii"))
os.environ.setdefault("DATABASE_URL", "postgresql://user:pass@localhost:5432/db")

from app.api.routes import storage_routes
from app.schemas.storage import PresignedPutRequest


def test_generar_put_url_uses_provided_filename(monkeypatch):
    captured = {}

    def fake_presigned_put_url(object_name: str):
        captured["name"] = object_name
        return f"https://minio.local/{object_name}"

    monkeypatch.setattr(
        storage_routes.minio_service, "get_presigned_put_url", fake_presigned_put_url
    )

    response = storage_routes.generar_put_url(PresignedPutRequest(file="example.png"))

    assert response.url == "https://minio.local/example.png"
    assert captured["name"] == "example.png"
