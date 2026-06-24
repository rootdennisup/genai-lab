from pydantic import BaseModel, Field, ValidationError
from typing import List, Optional

# 定义数据模型：由类型提示驱动 [1]
class UserProfile(BaseModel):
    id: int
    username: str
    email: str
    tags: List[str] = [] # 默认空列表
    is_active: Optional[bool] = True

# 模拟输入 JSON 数据（包含类型转换：字符串 "123" 转为 int 123）
raw_json = {
    "id": "123", 
    "username": "coder_api",
    "email": "[email protected]"
}

try:
    # 自动执行数据验证与类型强制转换 [1]
    user = UserProfile(**raw_json)
    print(f"解析成功，用户 ID 类型: {type(user.id)}") # 输出: <class 'int'>
    print(user.model_dump_json(indent=2))
except ValidationError as e:
    # 数据无效时自动生成清晰的错误信息 
    print(f"数据校验失败: {e.json()}")