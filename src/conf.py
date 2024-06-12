import os

from pydantic import Extra
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    mongo: MongoSettings = MongoSettings()


settings = Settings()
