from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # 定义配置项及其类型提示
    app_name: str = "My FastAPI App"
    database_url: str
    api_key: str
    app_debug: bool = False
    max_connections: int = 5

    # 配置 Pydantic 读取 .env 文件
    model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def get_settings():
    """
    使用 lru_cache 确保配置对象只被创建一次，提高性能
    """
    return Settings()