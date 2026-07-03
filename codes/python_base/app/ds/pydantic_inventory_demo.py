from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, ValidationError

# ==========================================
# 1. 定义数据模型 (The Data Contract)
# 继承 BaseModel 使其具备自动校验与转换能力
# ==========================================

class Product(BaseModel):
    # 基础校验：id 必须为整数，name 长度至少 2 位
    id: int
    name: str = Field(..., min_length=2, description="商品名称")
    
    # 范围校验：价格必须大于 0，库存不能为负数
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)
    
    # 可选字段与自动转换：Pydantic 会尝试将字符串日期转为 datetime 对象
    last_updated: Optional[datetime] = None

    # 2. 自定义验证器 (Custom Validator)
    # 模拟业务逻辑：禁止包含特定非法词汇
    @field_validator('name')
    @classmethod
    def name_must_not_contain_prohibited_words(cls, v: str) -> str:
        if "禁运" in v:
            raise ValueError('商品名称包含违禁词汇')
        return v.title() # 顺便执行数据清洗：将名称转为首字母大写

class InventoryReport(BaseModel):
    # 3. 嵌套模型 (Nested Models)
    # 能够精准校验深层嵌套的 JSON 对象
    warehouse_name: str
    items: List[Product]

# ==========================================
# 4. 执行演示 (Execution & Validation)
# ==========================================

def run_demo():
    print("--- 场景 A：正常数据处理（触发类型强制转换） ---")
    valid_data = {
        "warehouse_name": "北京 1 号仓",
        "items": [
            {
                "id": "1001",           # 输入是字符串，Pydantic 会自动转为 int
                "name": "macbook pro",   # 验证器会将其转为 "Macbook Pro"
                "price": "12999.5",     # 自动转为 float
                "stock": 50,
                "last_updated": "2023-10-27T10:00:00" # 自动转为 datetime 对象
            }
        ]
    }
    
    try:
        report = InventoryReport(**valid_data)
        print(f"成功加载仓库: {report.warehouse_name}")
        print(f"首个商品对象: {report.items}")
        # 展示序列化：将模型转回字典
        print(f"导出 JSON 模型: {report.model_dump_json(indent=2)}")
    except ValidationError as e:
        print(e.json())

    print("\n--- 场景 B：非法数据拦截（触发报错） ---")
    invalid_data = {
        "warehouse_name": "海外仓",
        "items": [
            {
                "id": 2002,
                "name": "禁运电子烟",     # 触发自定义验证器报错
                "price": -10,            # 触发 Field(gt=0) 报错
                "stock": "abc"           # 触发类型错误
            }
        ]
    }
    
    try:
        InventoryReport(**invalid_data)
    except ValidationError as e:
        print(f"发现 {e.error_count()} 处错误：")
        for error in e.errors():
            print(f"  - 字段 '{error['loc'][-1]}': {error['msg']}")

if __name__ == "__main__":
    run_demo()