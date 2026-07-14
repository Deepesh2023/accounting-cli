from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# In a real app, this would come from an environment variable
DATABASE_URL = "postgresql://user:password@localhost/printos_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
