import os
import sys
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.engine import reflection
from sqlalchemy.ext.declarative import declarative_base

from src.conf import settings
from src.db.repository import MessageRepository
from src.db.schema import Message
from src.dep.postgres import get_postgres
from src.services.message_service import MessageService

Base = declarative_base()


# Set up a test database URL
@pytest.fixture(scope='module')
def db_engine():
    engine = create_engine(str(settings.postgres.dsn))
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope='module')
def db_session():
    return get_postgres()


@pytest.fixture
def message_repository(db_session):
    return MessageRepository(db_session)


@pytest.fixture
def message_service(db_session):
    return MessageService(db_session)


def test_db_and_table_exists(db_engine):
    inspector = reflection.Inspector.from_engine(db_engine)
    tables = inspector.get_table_names()
    assert 'messages_test' in tables


def test_insert_and_select_data(db_session, message_service):
    chat_id = "chat1"
    user_id = "user1"
    message_text = "Hello, world!"
    message_datetime = datetime.now()

    inserted_message = message_service.add_message(
        chat_id, user_id, message_text, message_datetime
    )
    selected_message = (
        db_session.query(Message).filter_by(id=inserted_message.id).first()
    )

    assert selected_message is not None
    assert selected_message.chat_id == chat_id
    assert selected_message.user_id == user_id
    assert selected_message.message == message_text
    assert selected_message.datetime == message_datetime


def test_select_data_by_filters(db_session, message_service):
    message1 = message_service.add_message(
        "chat1", "user1", "Hello, world!", datetime.now()
    )
    message2 = message_service.add_message(
        "chat2", "user2", "Goodbye, world!", datetime.now()
    )

    filtered_messages_by_user = message_service.get_filtered_messages(user_id="user1")
    filtered_messages_by_chat = message_service.get_filtered_messages(chat_id="chat2")

    assert len(filtered_messages_by_user) == 1
    assert filtered_messages_by_user[0].id == message1.id

    assert len(filtered_messages_by_chat) == 1
    assert filtered_messages_by_chat[0].id == message2.id
