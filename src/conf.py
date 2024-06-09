import os

from pydantic import Extra
from pydantic_settings import BaseSettings, SettingsConfigDict


class TelegramSettings(BaseSettings):
    token: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="TG_", extra="allow"
    )


class LLMSettings(BaseSettings):
    path: str
    temperature: float
    max_tokens: int
    ctx: int

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="LLM_", extra="allow"
    )


class BotSettings(BaseSettings):
    start_message: str = "Hello!"


class MongoSettings(BaseSettings):
    host: str
    port: int

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="MONGO_", extra="allow"
    )


class Settings(BaseSettings):
    model: LLMSettings = LLMSettings()
    telegram: TelegramSettings = TelegramSettings()
    bot: BotSettings = BotSettings()
    mongo: MongoSettings = MongoSettings()


settings = Settings()
