from fastapi import FastAPI
from app.ef.log_decorator import log_execution_info

app = FastAPI()

@app.get("/chat")
@log_execution_info
async def chat_with_ai(prompt: str):
    # 模拟大模型推理耗时
    import asyncio
    await asyncio.sleep(0.5) 
    
    return {"response": f"AI 已收到你的提示词：{prompt}"}

if __name__ == "__main__":
    import uvicorn
    # 运行服务器
    uvicorn.run(app, host="127.0.0.1", port=8000)

    # fastapi dev app/ef/fast_logger.py 