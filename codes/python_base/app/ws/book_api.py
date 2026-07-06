from typing import Optional
from fastapi import FastAPI, Path, Query

app = FastAPI()

# 1. 声明式路由：定义方法与路径
@app.get("/books/{book_id}")
async def get_book(
    # 2. 路径参数与自动校验：声明 book_id 必须为 int 且大于 0
    book_id: int = Path(..., gt=0, description="图书的唯一数字 ID"),
    
    # 3. 查询参数与自动校验：声明 q 为可选字符串，长度 3-10 位
    q: Optional[str] = Query(None, min_length=3, max_length=10, description="搜索关键词")
):
    results = {"book_id": book_id}
    if q:
        results.update({"query": q})
    return results

# fastapi dev app/ws/book_api.py
# http://127.0.0.1:8000/books/1
# http://127.0.0.1:8000/books/1?q=py