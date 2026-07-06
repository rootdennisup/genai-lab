from typing import Annotated, Generator
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# ==========================================
# 1. 数据库依赖项 (解耦连接管理)
# ==========================================
def get_db_session() -> Generator:
    """
    模拟数据库 Session 的开启与关闭
    利用 yield 实现异步上下文管理模式 [3]
    """
    print(">>> [资源开启] 数据库连接已建立")
    db = {"connection": "active", "data": "Mock DB"}
    try:
        # yield 之前的代码在请求处理前运行
        yield db 
    finally:
        # yield 之后的代码在响应返回后运行，确保资源释放 [3, 4]
        print(">>> [资源释放] 数据库连接已安全关闭")

# ==========================================
# 2. 认证依赖项 (解耦安全逻辑)
# ==========================================
async def get_current_user(token: str):
    """
    模拟身份验证逻辑。在真实场景中这里会处理 OAuth2 或 JWT [1, 2]
    """
    if token != "secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证"
        )
    return {"username": "admin", "role": "superuser"}

# ==========================================
# 3. 声明式路由 (逻辑集成)
# ==========================================
@app.get("/secure-data/")
async def read_private_data(
    # 通过 Depends 注入数据库和用户信息
    # FastAPI 会自动按顺序执行这些子项 [2, 5]
    db: Annotated[dict, Depends(get_db_session)],
    user: Annotated[dict, Depends(get_current_user)]
):
    # 此时函数内部只需关注业务逻辑，无需处理认证和连接细节
    return {
        "message": f"欢迎回来, {user['username']}",
        "db_status": db["connection"],
        "data": "这是受保护的机密信息"
    }