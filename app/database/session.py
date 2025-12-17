"""Session and engine helpers for the modern SQLAlchemy stack."""

import os
from typing import Iterable

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


def _first_env(keys: Iterable[str]) -> str | None:
    """Return the first populated environment variable from the provided keys."""
    for key in keys:
        value = os.getenv(key)
        if value:
            return value
    return None


def _build_database_url() -> str:
    # Priority 1: explicit audit connection string, fallback to shared DATABASE_URL.
    url = _first_env(("AUDIT_DATABASE_URL", "DATABASE_URL"))
    if url:
        return url

    user = _first_env(("AUDIT_DB_USER", "DB_USER"))
    password = _first_env(("AUDIT_DB_PASSWORD", "DB_PASSWORD"))
    host = _first_env(("AUDIT_DB_HOST", "DB_HOST"))
    port = _first_env(("AUDIT_DB_PORT", "DB_PORT")) or "5432"
    name = _first_env(("AUDIT_DB_NAME", "DB_NAME"))

    missing = []
    if not user:
        missing.append("AUDIT_DB_USER/DB_USER")
    if not password:
        missing.append("AUDIT_DB_PASSWORD/DB_PASSWORD")
    if not host:
        missing.append("AUDIT_DB_HOST/DB_HOST")
    if not name:
        missing.append("AUDIT_DB_NAME/DB_NAME")

    if missing:
        raise RuntimeError(
            "Postgres no esta configurado para app.database. "
            "Define AUDIT_DATABASE_URL, DATABASE_URL o las variables: "
            + ", ".join(missing)
        )

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


DATABASE_URL = _build_database_url()
SQLALCHEMY_ECHO = os.getenv("AUDIT_SQLALCHEMY_ECHO", os.getenv("SQLALCHEMY_ECHO", "0")) == "1"

engine = create_engine(DATABASE_URL, echo=SQLALCHEMY_ECHO, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()


__all__ = ("Base", "SessionLocal", "engine")
