from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.conf import settings


def get_postgres():
    engine = create_engine(str(settings.postgres.dsn))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    return db
