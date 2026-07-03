import asyncio
from typing import Optional
from pydantic import BaseModel, Field, ValidationError

# ==========================================
# 1. 自定义异常 (User-defined Exceptions)
# 继承自 Exception 基类，用于表达特定业务错误 [2, 4]
# ==========================================
class TaskExecutionError(Exception):
    """当任务执行逻辑发生业务冲突时抛出"""
    pass

# ==========================================
# 2. 数据模型校验 (Pydantic 驱动)
# 自动拦截非法输入，防止后端代码处理脏数据 [2, 5]
# ==========================================
class Task(BaseModel):
    id: int
    title: str = Field(min_length=3)
    priority: int = Field(ge=1, le=5) # 优先级 1-5

# ==========================================
# 3. 模拟资源管理 (Context Manager)
# 使用 with 保证即使发生异常，资源也能被清理 [3, 6]
# ==========================================
class DatabaseSession:
    def __enter__(self):
        print(">>> [资源] 数据库连接已开启")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # 如果 exc_type 不为 None，说明发生了异常 [6]
        if exc_type:
            print(f">>> [资源] 捕获到内部错误，正在回滚事务: {exc_val}")
        print(">>> [资源] 数据库连接已安全关闭")
        # 返回 False 允许异常继续向上传播，返回 True 则抑制异常 [6]
        return False

# ==========================================
# 4. 核心逻辑函数：多层级异常处理
# ==========================================
async def submit_task_to_cloud(raw_data: dict):
    print(f"\n--- 开始处理任务: {raw_data.get('title', '未知')} ---")
    
    try:
        # 4.1 校验层：利用 Pydantic 自动抛出 ValidationError [2, 7]
        task = Task(**raw_data)
        
        # 4.2 业务层：显式触发异常 (raise) [1, 8]
        if task.priority == 5:
            # 模拟只有管理员能提交最高优先级任务
            raise TaskExecutionError("权限不足：不能提交优先级为 5 的紧急任务")

        # 4.3 资源层：结合 with 语句 [3]
        with DatabaseSession():
            print(f"正在保存任务 '{task.title}' 到数据库...")
            if task.id == 999: # 模拟特定的系统崩溃点
                raise RuntimeError("数据库写入超时")
            print("任务保存成功！")

    # 精准捕获：按从小到大的顺序排列异常类 [9]
    except ValidationError as e:
        print(f"[数据错误] 输入格式不合法: {e.json()}")
    
    except TaskExecutionError as e:
        print(f"[业务异常] 逻辑冲突: {e}")
    
    except Exception as e:
        # 捕获所有未预见的运行错误 [1]
        print(f"[系统崩溃] 发生未知错误类型: {type(e).__name__} -> {e}")
    
    else:
        # 仅在 try 块代码完全成功（未发生异常）时执行 [1, 10]
        print("✔ 流程检查：任务已成功进入云端队列")
    
    finally:
        # 无论成功还是失败，最终都会执行的操作 [1, 3]
        print("--- 任务处理流程结束 ---")

# ==========================================
# 5. 执行测试场景
# ==========================================
async def main():
    # 场景 A: 数据校验失败 (标题太短)
    await submit_task_to_cloud({"id": 1, "title": "A", "priority": 3})
    
    # 场景 B: 触发自定义业务异常 (优先级过高)
    await submit_task_to_cloud({"id": 2, "title": "重要周报", "priority": 5})
    
    # 场景 C: 触发运行时系统错误 (ID=999)
    await submit_task_to_cloud({"id": 999, "title": "系统测试", "priority": 1})
    
    # 场景 D: 完全成功的流程
    await submit_task_to_cloud({"id": 100, "title": "部署应用", "priority": 2})

if __name__ == "__main__":
    asyncio.run(main())