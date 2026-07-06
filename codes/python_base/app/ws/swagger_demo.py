from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="商品管理系统", description="演示 Swagger UI 自动化功能")

# 定义数据模型，Pydantic 会自动将其转换为 JSON Schema 驱动文档生成
class Item(BaseModel):
    name: str
    price: float
    is_offer: Optional[bool] = None

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    """
    获取商品信息：
    - **item_id**: 路径参数（必须是整数）
    - **q**: 查询参数（可选字符串）
    """
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    """
    更新商品信息：
    - **item**: 请求体数据（由 Pydantic 模型定义结构）
    """
    return {"item_name": item.name, "item_id": item_id}


# 1. terminal 执行命令： fastapi dev app/ws/swagger_demo.py
# 2. 浏览器访问： http://127.0.0.1:8000/items/5?q=query
# 3. 交互式文档 Swagger UI： http://127.0.0.1:8000/docs
# 4. 退出，terminal 中快捷键 ctrl+C

