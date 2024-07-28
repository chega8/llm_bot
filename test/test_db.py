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

from src.conf import Role, settings
from src.db.repository import MessageRepository
from src.db.schema import TestMessage
from src.dep.postgres import get_postgres

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
    return MessageRepository(db_session, TestMessage)


@pytest.fixture
def message_service(db_session):
    return MessageService(db_session)


def test_db_and_table_exists(db_engine):
    inspector = reflection.Inspector.from_engine(db_engine)
    tables = inspector.get_table_names()
    assert 'messages_test' in tables


def test_insert_and_select_data(db_session, message_service):
    chat_id = 123
    user_id = 321
    role = Role.USER
    message_text = "Hello, world!"
    message_datetime = datetime.now()

    inserted_message = message_service.add_message(
        chat_id, user_id, message_text, role, message_datetime
    )

    selected_message = message_service.get_filtered_messages(
        chat_id=chat_id, user_id=user_id
    )[0]
    # selected_message = (
    #     db_session.query(TestMessage).filter_by(id=inserted_message.id).first()
    # )

    assert selected_message is not None
    assert selected_message.chat_id == chat_id
    assert selected_message.user_id == user_id
    assert selected_message.message == message_text


def test_select_data_by_filters(db_session, message_service):
    message_service.clear_messages()

    message1 = message_service.add_message(
        123, 321, "Hello, world!", Role.AI, datetime.now()
    )
    message2 = message_service.add_message(
        456, 654, "Goodbye, world!", Role.USER, datetime.now()
    )

    filtered_messages_by_user = message_service.get_filtered_messages(user_id=321)
    filtered_messages_by_chat = message_service.get_filtered_messages(chat_id=456)
    filtered_messages_by_role = message_service.get_filtered_messages(role=Role.AI)

    assert len(filtered_messages_by_user) == 1
    assert filtered_messages_by_user[0].id == message1.id

    assert len(filtered_messages_by_chat) == 1
    assert filtered_messages_by_chat[0].id == message2.id

    assert len(filtered_messages_by_role) == 1
    assert filtered_messages_by_role[0].id == message1.id
