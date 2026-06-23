from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError
from pydantic_settings import BaseSettings

# --- 组件 1: Settings (配置管理) ---
# 作用：自动从环境变量中读取配置
class ProjectConfig(BaseSettings):
    app_name: str = "My Project API"
    admin_email: str
    items_per_user: int = 50

    class Config:
        # 告诉 Pydantic 去读取 .env 文件
        env_file = ".env"

# --- 组件 2: BaseModel (基本模型) ---
# 作用：定义数据结构并执行自动校验
class UserItem(BaseModel):
    # --- 组件 3: Field (字段定制) ---
    # 作用：添加额外的校验逻辑，如字符串长度、数值范围
    id: int = Field(..., description="项目的唯一 ID", gt=0) # 必须大于 0
    name: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0, le=10000) # 价格在 0-10000 之间
    tags: List[str] = [] # 默认空列表
    created_at: Optional[datetime] = Field(default_factory=datetime.now)

    # --- 组件 4: Validator (自定义验证器) ---
    # 作用：处理 Field 无法覆盖的复杂业务逻辑
    @field_validator('name')
    @classmethod
    def name_must_not_contain_api(cls, v: str) -> str:
        if 'api' in v.lower():
            raise ValueError('项目名称中不能包含关键字 "api"')
        return v.title() # 校验通过后，自动将首字母大写

# --- 测试运行 ---
if __name__ == "__main__":
    # 模拟从环境变量或配置中读取
    try:
        # 这里模拟没有设置环境变量导致报错的情况，或手动提供
        config = ProjectConfig(admin_email="[email protected]")
        print(f"--- 系统启动: {config.app_name} ---")

        # 场景 A: 正常数据输入
        valid_data = {
            "id": 101,
            "name": "Fastapi Learning",
            "price": 99.5,
            "tags": ["python", "pydantic"]
        }
        item = UserItem(**valid_data)
        print(f"验证成功，对象内容: {item.model_dump_json(indent=2)}")

        # 场景 B: 异常数据输入（触发校验错误）
        invalid_data = {
            "id": -5,              # 错误：id 必须大于 0
            "name": "Super API",   # 错误：名称包含了禁止的 "api"
            "price": "Free"        # 错误：无法转换为 float
        }
        UserItem(**invalid_data)

    except ValidationError as e:
        print("\n--- 捕获到校验错误 ---")
        print(e.json()) # Pydantic 会自动生成详尽的错误 JSON [1]




