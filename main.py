import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    audit,
    auth,
    campo_routes,
    control_calidad_routes,
    cultivo_routes,
    info_nutricional_routes,
    lote_routes,
    producto_routes,
    producto_lote_routes,
    public_routes,
    qr_routes,
    storage_routes,
    usuario_routes,
)
from app.db.connection import (
    Base,
    engine,
    get_db,
)
from app.services import audit_service

import app.models  # noqa: F401
import app.models.audit_log  # noqa: F401
import app.models.campo  # noqa: F401
import app.models.info_nutricional  # noqa: F401
import app.models.usuario  # noqa: F401
import app.models.token_revocado  # noqa: F401

logger = logging.getLogger(__name__)

app = FastAPI(title="Goland QR API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://goland-qr-frontend.reto-ucu.net",
    ],
    allow_origin_regex=r"http://localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


@app.middleware("http")
async def audit_middleware(request: Request, call_next):
    response = await call_next(request)
    user = getattr(request.state, "user", None)
    if user:
        endpoint = request.scope.get("endpoint")
        action_name = endpoint.__name__ if endpoint else None
        client = request.client.host if request.client else None
        db = next(get_db())
        try:
            audit_service.log_action(
                db,
                usuario_id=user.usuarioid,
                path=request.url.path,
                method=request.method,
                status_code=response.status_code,
                action=action_name,
                client_ip=client,
                user_agent=request.headers.get("user-agent"),
                payload=request.url.query or None,
            )
        finally:
            db.close()
    return response


@app.get("/")
def root():
    return {"status": "Goland QR API funcionando!"}

app.include_router(usuario_routes.router)
app.include_router(auth.router)
app.include_router(audit.router)
app.include_router(producto_routes.router)
app.include_router(lote_routes.router)
app.include_router(cultivo_routes.router)
app.include_router(public_routes.router)
app.include_router(campo_routes.router)
app.include_router(control_calidad_routes.router)
app.include_router(info_nutricional_routes.router)
app.include_router(qr_routes.router)
app.include_router(producto_lote_routes.router)
app.include_router(storage_routes.router)
