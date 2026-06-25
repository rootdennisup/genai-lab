from typing import Union, List, Optional
from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel

app = FastAPI()

# 1. 定义 Pydantic 模型（数据校验与序列化）
#    Pydantic 声明一次：通过定义 Task 类，你同时获得了数据验证、类型转换和 JSON Schema 生成功能
class Task(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 1  # 默认优先级为1

# 模拟数据库
db = []

# 2. 模拟依赖注入：模拟一个简单的权限检查 [5]
def common_parameters(q: Union[str, None] = None, skip: int = 0, limit: int = 10):
    return {"q": q, "skip": skip, "limit": limit}

# 3. POST 请求：创建任务（请求体校验 + 201 状态码）  
@app.post("/tasks/", status_code=status.HTTP_201_CREATED)
async def create_task(task: Task):
    db.append(task)
    return task

# 4. GET 请求：列表查询（查询参数 + 依赖注入） 
#    异步机制：使用 async def 声明函数，让应用利用 Starlette 的异步特性处理并发请求
#    依赖注入 (Depends)：在 read_tasks 中通过注入 common_parameters 实现了代码逻辑的复用，这在处理认证和数据库连接时非常有用
@app.get("/tasks/")
async def read_tasks(params: dict = Depends(common_parameters)):
    # 模拟分页与过滤逻辑
    results = db[params["skip"] : params["skip"] + params["limit"]]
    if params["q"]:
        results = [t for t in results if params["q"] in t.title]
    return {"tasks": results, "params": params}

# 5. GET 请求：获取单个任务（路径参数 + 错误处理） 
@app.get("/tasks/{task_id}")
async def read_task(task_id: int):
    if task_id >= len(db) or task_id < 0:
        # 自动生成清晰的错误响应 [3]
        raise HTTPException(status_code=404, detail="任务不存在")
    return db[task_id]