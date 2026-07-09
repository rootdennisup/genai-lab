from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "ai-buddy"
    llm_mode: str = "mock"

    model_api_key: str = ""
    model_base_url: str = ""
    model_name: str = ""
    model_timeout: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AI_BUDDY_",
        extra="ignore"
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


# 分成两个配置类，是为了让项目配置和模型厂商配置隔离。
# Settings 管理应用自身配置，QwenSettings 管理百炼 Qwen 相关配置。
settings = Settings()
qwen_settings = QwenSettings()