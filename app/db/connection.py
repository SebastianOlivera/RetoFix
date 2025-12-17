import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

def _build_database_url() -> str:
    # Prioridad 1: DATABASE_URL (ideal para Docker/K8s)
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return database_url

    # Prioridad 2: DB_* (también válido)
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME")

    missing = [k for k, v in {
        "DB_USER": user,
        "DB_PASSWORD": password,
        "DB_HOST": host,
        "DB_NAME": name,
    }.items() if not v]

    if missing:
        raise RuntimeError(
            "Falta configuración de Postgres. Seteá DATABASE_URL o estas env vars: "
            + ", ".join(missing)
        )

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"

DATABASE_URL = _build_database_url()
SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "0") == "1"

engine = create_engine(DATABASE_URL, echo=SQLALCHEMY_ECHO, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
