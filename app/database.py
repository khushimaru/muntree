from sqlmodel import SQLModel, create_engine, Session
from app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    from app.models import Link, Admin
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
