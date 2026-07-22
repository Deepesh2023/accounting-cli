import os
from sqlalchemy.pool import StaticPool
from sqlmodel import create_engine, Session, SQLModel

_DEFAULT = "sqlite://"  # in-memory temp file, shared across connections

DATABASE_URL = os.getenv("DATABASE_URL", _DEFAULT)

connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("DATABASE_ECHO", "false").lower() == "true",
    connect_args=connect_args,
    poolclass=StaticPool if DATABASE_URL == _DEFAULT else None,
)

def get_db():
    with Session(engine) as session:
        yield session
