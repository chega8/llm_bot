import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.conf import settings
from src.db.schema import Message, TestMessage

# psql postgresql://postgres:password@localhost:5432/chat_db
if __name__ == "__main__":
    print(f'Connecting to {settings.postgres.dsn}')
    engine = create_engine(str(settings.postgres.dsn))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()
    Base.metadata.create_all(
        bind=engine, tables=[Message.__table__, TestMessage.__table__]
    )
