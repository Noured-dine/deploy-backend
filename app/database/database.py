from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
import sqlite3
import os
from contextlib import asynccontextmanager
from app.database.create_database import create_sqlite_database
import pathlib

SQL_LITE_DB_PATH = os.path.join("/home", "database.sqlite")

SQLALCHEMY_DATABASE_SQL_LITE_URL = f"sqlite:///{SQL_LITE_DB_PATH}"

POSTGRE_USERNAME = os.getenv("POSTGRE_USERNAME")
POSTGRE_PASSWORD = os.getenv("POSTGRE_PASSWORD")
POSTGRE_HOST = os.getenv("POSTGRE_HOST")
POSTGRE_DB_NAME = os.getenv("POSTGRE_DB_NAME")

SQLALCHEMY_DATABASE_POSTGRE_SQL_URL = (
    f"postgresql+psycopg2://{POSTGRE_USERNAME}:{POSTGRE_PASSWORD}@{POSTGRE_HOST}/{POSTGRE_DB_NAME}"
    if POSTGRE_USERNAME and POSTGRE_PASSWORD and POSTGRE_HOST and POSTGRE_DB_NAME
    else None
)

if SQLALCHEMY_DATABASE_POSTGRE_SQL_URL:
    engine = create_engine(SQLALCHEMY_DATABASE_POSTGRE_SQL_URL)
else:
    engine = create_engine(
        SQLALCHEMY_DATABASE_SQL_LITE_URL,
        connect_args={"check_same_thread": False}
    )

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection): 
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app):
    if SQLALCHEMY_DATABASE_POSTGRE_SQL_URL:
        Base.metadata.create_all(bind=engine)
    yield  