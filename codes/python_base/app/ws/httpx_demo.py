import httpx
import asyncio

async def call_api():
    # 使用 AsyncClient 实现高性能异步通信
    async with httpx.AsyncClient() as client:
        response = await client.get("http://127.0.0.1:8000/items/5")
        return response.json()