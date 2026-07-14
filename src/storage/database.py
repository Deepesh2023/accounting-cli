from sqlmodel import create_engine, Session, SQLModel

# In a real app, this would come from an environment variable
DATABASE_URL = "postgresql://user:password@localhost/printos_db"

engine = create_engine(DATABASE_URL)

def get_db():
    with Session(engine) as session:
        yield session
