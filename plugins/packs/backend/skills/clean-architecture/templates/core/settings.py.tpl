# app/core/settings.py - the one configuration object.
#
# Rules:
# - Required values have no default: a missing variable fails at startup, never a guessed value.
# - Secrets are SecretStr; call .get_secret_value() only where the value is used.
# - No module-level Settings() instance; everything calls get_settings() (cached).
# - Every field added here is also added to .env.example with a placeholder in the same task.
# - Keep only the fields the workspace actually uses; rename to the workspace's .env names.
from functools import lru_cache
from typing import Literal

from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # extra="ignore" only because the shared .env also carries variables for other tools
    # (for example the Postgres MCP); use the default "forbid" when the file is app-only.
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_uri: SecretStr = Field(validation_alias=AliasChoices("DATABASE_URI", "DATABASE_URL"))
    environment: Literal["dev", "test", "staging", "production"]


@lru_cache
def get_settings() -> Settings:
    return Settings()  # values come from the environment (pydantic.mypy plugin knows this)
