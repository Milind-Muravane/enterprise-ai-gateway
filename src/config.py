"""
Responsibilities:
- Load environment variables from .env
- Validate required API keys
- Expose a single settings object for the application
"""

from pathlib import Path
from dotenv import load_dotenv
from pydantic import ValidationError
from pydantic_settings import BaseSettings,SettingsConfigDict

# Loading .env file from the project root
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """

    gemini_api_key: str
    groq_api_key: str
    tavily_api_key: str

    app_name : str = "Smart Enterprise AI gateway"
    debug : bool = False

    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding = "utf-8",
        extra = "ignore"
    )

try:
    settings = Settings()
except ValidationError as e:
     raise RuntimeError(
        "\n CONFIG ERROR!!!\n"
        "One or more required environment variables are missing.\n"
        "Please check your .env file.\n"
    ) from e