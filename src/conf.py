import os
from enum import Enum

from pydantic import AnyUrl, Extra, root_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Role(Enum):
    USER = "user"
    AI = "ai"
    SYSTEM = "system"


class PostgresSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    db: str
    dsn: AnyUrl = None

    @root_validator(pre=True, skip_on_failure=True, allow_reuse=True)
    def init_postgres_dsn(cls, values):
        values[
            "dsn"
        ] = f"postgresql://{values['user']}:{values['password']}@{values['host']}:{values['port']}/{values['db']}"
        return values

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="PG_", extra="allow"
    )


class BotSettings(BaseSettings):
    token: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="BOT_", extra="allow"
    )


class ChatSettings(BaseSettings):
    max_history_len: int

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="CHAT_", extra="allow"
    )


class LLMSettings(BaseSettings):
    path: str
    temperature: float
    max_tokens: int
    ctx: int

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="LLM_", extra="allow"
    )


class MongoSettings(BaseSettings):
    host: str
    port: int

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="MONGO_", extra="allow"
    )


class Settings(BaseSettings):
    model: LLMSettings = LLMSettings()
    chat: ChatSettings = ChatSettings()
    bot: BotSettings = BotSettings()
    postgres: PostgresSettings = PostgresSettings()


settings = Settings()
