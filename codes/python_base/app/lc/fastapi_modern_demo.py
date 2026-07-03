import asyncio
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Optional

# 1. 初始化 FastAPI：应用的主入口 [3]
app = FastAPI(title="现代工程演进 Demo")

# ==========================================
# 2.1 声明式驱动：Pydantic 数据模型 [4, 5]
# ==========================================
class Task(BaseModel):
    # 类型提示驱动：自动校验 title 为字符串，priority 为 1-5 的整数
    title: str
    description: Optional[str] = None
    priority: int = Field(ge=1, le=5, description="优先级 1-5")
    
    # 自动转换：如果输入 "99.5"，Pydantic 会尝试将其转为 float（这里示例为 int）[4]

# ==========================================
# 2.2 依赖注入 (Depends)：逻辑解耦 [3, 6]
# ==========================================
async def verify_token(x_token: str = Header(...)):
    """模拟安全认证依赖：从请求头提取 X-Token"""
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="无效的认证令牌")
    return x_token

# ==========================================
# 2.3 异步并发：非阻塞执行 [7, 8]
# ==========================================
@app.post("/tasks/")
async def create_task(
    task: Task, 
    token: str = Depends(verify_token) # 注入依赖项
):
    """
    笔记1：类型提示与自动化
    异步路径操作函数：
    1.类型提示 (Task)：只需声明 task: Task，FastAPI 利用 Pydantic 读取这些类型注解，自动完成从网络 JSON 到 Python 对象的转换和校验。
    2.依赖注入 (Depends)：自动执行 verify_token，解耦认证逻辑 [3]
    
    
    笔记2：依赖注入 (Depends)
    1.解耦：verify_token 被声明为 Depends，意味着认证逻辑与业务逻辑（创建任务）是完全分离的
    2.复用：可以将同一个 verify_token 注入到成百上千个不同的接口中，而不需要在每个函数里重复编写认证代码
    """

    # 模拟异步 IO 操作（如写入数据库或调用 AI 接口）
    await asyncio.sleep(1) 
    """
    笔记3：异步并发 (Async/Await)
    1.非阻塞：通过 async def 声明函数，应用运行在 Uvicorn（ASGI 服务器）上
    2.性能：当代码执行到 await asyncio.sleep(1) 时，线程不会被阻塞，而是去处理其他的并发请求。这使得 FastAPI 能够以极高的效率处理海量连接
    """
    
    return {
        "message": "任务创建成功",
        "task_title": task.title,
        "auth_status": f"使用令牌 {token} 验证通过"
    }

# 启动说明：在终端运行 uvicorn fastapi_modern_demo:app --reload [10]

# 运行：
# 1.运行命令：fastapi dev app/lc/fastapi_modern_demo.py
"""
笔记4：声明式驱动与自动文档
1.运行代码后访问 http://127.0.0.1:8000/docs 可看到 Swagger UI 自动生成的交互式文档
2.文档是基于代码实时生成的（启动时生成），确保了接口描述与真实逻辑的 100% 同步
"""
# 2.访问 http://127.0.0.1:8000/docs 【Try it out】
# 3.ctrl + C 退出