import sqlalchemy
from sqlalchemy import Column, DateTime, Enum, Float, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

from src.conf import Role

Base = declarative_base()

role_type = sqlalchemy.types.Enum(
    Role, name='role', values_callable=lambda obj: [e.value for e in obj]
)


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, index=True)
    user_id = Column(String, index=True)
    message = Column(String)
    # role = Column(Enum("user", "ai", "system", name="role", create_type=False), default=Role.USER.value)
    role = Column(role_type, default=Role.USER.value)
    datetime = Column(DateTime)


class Tox(Base):
    __tablename__ = 'tox'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, index=True)
    user_id = Column(String, index=True)
    message = Column(String)
    tox = Column(Float)
    datetime = Column(DateTime)


class TestMessage(Base):
    __tablename__ = 'messages_test'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, index=True)
    user_id = Column(String, index=True)
    message = Column(String)
    # role = Column(String, default=Role.USER.value)
    role = Column(role_type, default=Role.USER.value)
    datetime = Column(DateTime)
