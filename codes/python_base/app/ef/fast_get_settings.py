from fastapi import FastAPI, Depends
from app.ef.config import get_settings, Settings

app = FastAPI()

@app.get("/info")
async def get_app_info(settings: Settings = Depends(get_settings)):
    return {
        "app_name": settings.app_name,
        "debug_mode": settings.app_debug,
        "database": settings.database_url  # 生产环境建议不要直接返回敏感信息
    }

@app.get("/items/")
async def read_items(settings: Settings = Depends(get_settings)):
    # 使用配置中的 API Key 进行逻辑处理
    return {"message": f"Using API Key: {settings.api_key[:4]}****"}

## 1.f-string 语法：在 Python 中，f-string 以 f" 或 f' 开头，其中的变量或表达式必须放在花括号 {} 内部
## 2.切片操作：[:4] 是字符串切片语法，表示获取字符串的前 4 个字符


# 运行：
# 1.运行命令：fastapi dev app/ef/fast_get_settings.py 
# 2.访问 http://127.0.0.1:8000/docs 【Try it out】
# 3.ctrl + C 退出