import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI(title="流式传输与 SSE 演示")

# ==========================================
# 1. 核心生成器 (Generator)
# 利用 yield 实现“惰性求值”和流式分发
# ==========================================
async def fake_log_generator():
    """模拟持续产生日志的异步生成器"""
    for i in range(1, 11):
        await asyncio.sleep(1) # 模拟每秒产生一条数据
        # SSE 格式规范：必须以 'data: ' 开头，以 '\n\n' 结尾
        yield f"data: 正在处理第 {i} 条日志记录...\n\n"

# ==========================================
# 2. 流式接口实现 (StreamingResponse)
# ==========================================
@app.get("/log-stream")
async def stream_logs():
    """
    通过 StreamingResponse 将生成器内容通过 HTTP 流返回
    """
    return StreamingResponse(
        fake_log_generator(), 
        media_type="text/event-stream" # 声明为 SSE 专用媒体类型
    )

# 1. terminal 执行命令： fastapi dev app/ws/stream_api.py
# 2. 浏览器访问： http://127.0.0.1:8000/log-stream
# 3. 交互式文档 Swagger UI： http://127.0.0.1:8000/docs