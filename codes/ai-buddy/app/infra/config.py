from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    app_name: str = "ai-buddy"
    llm_mode: Literal["mock", "qwen"] = "mock"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AI_BUDDY_",
        extra="ignore",
    )


class QwenSettings(BaseSettings):
    api_key: str = ""
    base_url: str = ""
    model: str = "qwen-plus"
    timeout: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="QWEN_",
        extra="ignore",
    )

    @property
    def chat_completions_url(self) -> str:
        base_url = self.base_url.rstrip("/")
        if base_url.endswith("/chat/completions"):
            return base_url
        return f"{base_url}/chat/completions"


# Keep app settings separate from model-provider settings.
settings = Settings()
qwen_settings = QwenSettings()
