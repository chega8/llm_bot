import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../.."))


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.conf import settings
from src.db.schema import Message, TestMessage, Tox


def drop_table(schema, Base):
    engine = create_engine(str(settings.postgres.dsn))
    Base.metadata.drop_all(bind=engine, tables=[schema.__table__])
    print(f'Table {schema} dropped')


# psql postgresql://postgres:password@localhost:5432/chat_db
if __name__ == "__main__":
    print(f'Connecting to {settings.postgres.dsn}')
    engine = create_engine(str(settings.postgres.dsn))
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base = declarative_base()

    drop_table(Message, Base)
    drop_table(TestMessage, Base)
    drop_table(Tox, Base)

    Base.metadata.create_all(
        bind=engine, tables=[Message.__table__, TestMessage.__table__, Tox.__table__]
    )
