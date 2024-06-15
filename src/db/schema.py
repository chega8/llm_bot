from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base

from src.conf import Role

Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, index=True)
    user_id = Column(String, index=True)
    message = Column(String)
    role = Column(String, default=Role.USER.value)
    datetime = Column(DateTime)


class TestMessage(Base):
    __tablename__ = 'messages_test'
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(String, index=True)
    user_id = Column(String, index=True)
    message = Column(String)
    datetime = Column(DateTime)
