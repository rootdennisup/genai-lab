# HTTP 四要素理解
# 1. terminal 执行命令： fastapi dev app/http_demo.py
# 2. 浏览器访问： http://127.0.0.1:8000/items/5?q=query
# 3. 交互式文档 Swagger UI： http://127.0.0.1:8000/docs
# 4. 退出，terminal 中快捷键 ctrl+C

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 定义一个 Pydantic 数据模型，用于请求体
class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None

# 示例 A：GET 请求
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# 示例 B：PUT 请求
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}