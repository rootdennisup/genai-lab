from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# 定义请求体模型
class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = None

# 定义 API 接口
# FastAPI 会自动完成 JSON 的读取、校验与转换 [2]
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    # 此处 item 已经是经过校验的 Pydantic 模型对象 [2, 5]
    return {"item_name": item.name, "item_id": item_id}

# 运行：
# 1.运行命令：fastapi dev app/fastapi_json.py 
# 2.访问 http://127.0.0.1:8000/docs 查看自动生成的交互式文档  
# 3.ctrl + C 退出

