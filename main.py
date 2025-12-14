from fastapi import FastAPI

from app.api.routes import (
    campo_routes,
    control_calidad_routes,
    cultivo_routes,
    info_nutricional_routes,
    lote_routes,
    producto_routes,
    public_routes,
    usuario_routes,
)
from app.db.connection import Base, engine


import app.models

app = FastAPI(title="Goland QR API")

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"status": "Goland QR API funcionando!"}


app.include_router(usuario_routes.router)
app.include_router(producto_routes.router)
app.include_router(lote_routes.router)
app.include_router(cultivo_routes.router)
app.include_router(public_routes.router)
app.include_router(campo_routes.router)
app.include_router(info_nutricional_routes.router)
app.include_router(control_calidad_routes.router)

