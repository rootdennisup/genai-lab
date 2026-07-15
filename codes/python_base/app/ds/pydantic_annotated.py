from typing import Annotated
from pydantic import BaseModel, Field
from fastapi import FastAPI, Query

app = FastAPI()

# 1. 定义可复用的带约束类型（核心优势：逻辑解耦与复用）
Username = Annotated[str, Field(min_length=3, max_length=20, description="用户登录名")]
UserAge = Annotated[int, Field(gt=18, description="必须成年")]

class UserRegister(BaseModel):
    # 使用定义好的带约束类型
    username: Username
    age: UserAge
    # 也可以直接就地声明
    email: Annotated[str, Field(pattern=r".+@.+\..+")] 

@app.post("/register")
async def register(
    user: UserRegister,
    # 在 FastAPI 路径参数中同样推荐 Annotated
    token: Annotated[str, Query(description="邀请码")] = None
):
    return {"message": f"用户 {user.username} 注册成功"}