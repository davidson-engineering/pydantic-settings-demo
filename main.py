"""
Demonstrates loading configuration settings from environment variables and .env files
using Pydantic V2's BaseSettings. Shows how environment variables take precedence over .env files
and how to handle settings for different environments (default, dev, prod).

Example .env file content:
# .env
MYAPP_DATABASE_URL=sqlite:///default.db
MYAPP_DATABASE_TOKEN=secret123
MYAPP_API_KEY=apikey123
MYAPP_DEBUG_MODE=True
MYAPP_LOG_LEVEL=INFO
MYAPP_PORT=8000

# .env.dev
MYAPP_DATABASE_URL=sqlite:///dev.db
MYAPP_DEBUG_MODE=True
MYAPP_LOG_LEVEL=DEBUG

# .env.prod
MYAPP_DATABASE_URL=sqlite:///prod.db
MYAPP_DEBUG_MODE=False
MYAPP_LOG_LEVEL=INFO

Note: This script uses Pydantic V2, with @field_validator instead of the deprecated @validator.
"""

from enum import Enum
from typing import Optional
from pydantic import SecretStr, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
import os


class LogLevel(str, Enum):
    """Valid log levels for the application."""

    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class MyAppSettings(BaseSettings):
    """Base configuration settings for the application."""

    database_url: str
    database_token: SecretStr
    api_key: SecretStr
    debug_mode: bool
    log_level: LogLevel = Field(default=LogLevel.INFO)
    port: int = Field(default=8000, ge=1, le=65535)

    model_config = SettingsConfigDict(
        env_prefix="MYAPP_",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Ensure port is within valid range."""
        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v

    @field_validator("log_level", mode="before")
    @classmethod
    def validate_log_level(cls, v: Optional[str]) -> LogLevel:
        """Ensure log_level is a valid LogLevel enum value, case-insensitive."""
        if v is None:
            return LogLevel.INFO
        try:
            return LogLevel(v.upper())
        except ValueError:
            raise ValueError(f"Invalid log level: {v}. Must be one of {list(LogLevel)}")

    def print_settings(self, mask_secrets: bool = True) -> None:
        """Print settings, optionally masking secret values."""
        if mask_secrets:
            print(f"\nSettings for {self.__class__.__name__} (secrets masked):")
        else:
            print(f"\nSettings for {self.__class__.__name__} (secrets exposed):")
        print("-" * (40 + len(self.__class__.__name__)))
        for field, value in self.__dict__.items():
            if isinstance(value, SecretStr) and (not mask_secrets):
                print(f"{field}:{value.get_secret_value()}")
            else:
                print(f"{field}: {value}")


def print_env_vars() -> None:
    """Print existing MYAPP_ environment variables."""
    env_vars = [(k, v) for k, v in os.environ.items() if k.startswith("MYAPP_")]
    if env_vars:
        print("\nExisting MYAPP_ environment variables:")
        for key, value in env_vars:
            print(f"{key}: {value}")
    else:
        print("\nNo MYAPP_ environment variables found.")


def print_settings_comparison(
    settings: MyAppSettings,
    label: str,
    initial_settings: Optional[MyAppSettings] = None,
) -> None:
    """Print settings with an optional comparison to initial settings."""
    print(f"\nSettings for {settings.__class__.__name__} ({label}):")
    print("-" * (18 + len(settings.__class__.__name__) + len(label) + 2))
    settings.print_settings(mask_secrets=True)
    if initial_settings:
        print(f"\nInitial {settings.__class__.__name__} settings (before overrides):")
        initial_settings.print_settings(mask_secrets=True)


def main() -> None:
    """Main function to demonstrate Pydantic V2 settings loading."""
    print("Starting application...")

    # Print existing environment variables
    print_env_vars()

    # Define settings classes for different environments
    class DefaultSettings(MyAppSettings):
        model_config = SettingsConfigDict(
            env_prefix="MYAPP_",
            env_file=".env",
            env_file_encoding="utf-8",
            case_sensitive=False,
            extra="allow",
        )

    class ProdSettings(MyAppSettings):
        model_config = SettingsConfigDict(
            env_prefix="MYAPP_",
            env_file=(".env", ".env.prod"),
            env_file_encoding="utf-8",
            case_sensitive=False,
            extra="allow",
        )

    class DevSettings(MyAppSettings):
        model_config = SettingsConfigDict(
            env_prefix="MYAPP_",
            env_file=(".env", ".env.dev"),
            env_file_encoding="utf-8",
            case_sensitive=False,
            extra="allow",
        )

    class CustomSettings(MyAppSettings):
        model_config = SettingsConfigDict(
            env_prefix="MYCUSTOMAPP_",
            env_file=".env",
            env_file_encoding="utf-8",
            case_sensitive=False,
            extra="allow",
        )

    try:
        # Initialize settings
        default_settings = DefaultSettings()
        initial_prod_settings = ProdSettings()
        initial_dev_settings = DevSettings()

        # Demonstrate environment variable override
        print("\nSetting MYAPP_DATABASE_URL to demonstrate env var precedence...")
        os.environ["MYAPP_DATABASE_URL"] = (
            "env.will.always.win.over.env-files/database_url"
        )
        prod_settings = ProdSettings()

        print("\nSetting MYAPP_DEBUG_MODE to demonstrate type parsing...")
        os.environ["MYAPP_DEBUG_MODE"] = "FALSE"
        dev_settings = DevSettings()

        # Print settings with comparisons
        print_settings_comparison(default_settings, "Default")
        print_settings_comparison(
            prod_settings,
            "Production",
            initial_prod_settings,
        )
        print(
            "\nNote: MYAPP_DATABASE_URL was set in the environment and overrides .env file values for both dev and prod."
        )

        print_settings_comparison(
            dev_settings,
            "Development",
            initial_dev_settings,
        )
        print(
            "\nNote: MYAPP_DEBUG_MODE was set in the environment, parsed as boolean, and only affects dev settings."
        )

        # Expose secrets (unmasked for demonstration)
        print("\nExposing unmasked secrets for all settings:")
        for settings, label in [
            (default_settings, "Default"),
            (prod_settings, "Production"),
            (dev_settings, "Development"),
        ]:
            settings.print_settings(mask_secrets=False)

        print("\nDemonstrating CustomSettings with custom `MYCUSTOMAPP_` env prefix...")
        os.environ["MYCUSTOMAPP_DATABASE_URL"] = "sqlite:///custom.db"
        custom_settings = CustomSettings()
        custom_settings.print_settings(mask_secrets=True)

    except Exception as e:
        print(f"\nError loading settings: {e}")
        print("Ensure .env files exist and are correctly formatted.")


if __name__ == "__main__":
    main()
