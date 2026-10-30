from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="SUPPORT_", env_file=".env", extra="ignore")
    ollama_url: str = "http://localhost:11434"
    model: str = "granite4.2:3b"
    timeout: float = 180
    knowledge_dir: Path = Path(__file__).resolve().parents[1] / "data" / "visa"
