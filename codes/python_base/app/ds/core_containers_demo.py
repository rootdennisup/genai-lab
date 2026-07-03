from typing import List, Tuple, Dict, Set

# 案例模拟：电商后台库存与订单管理系统
# 将列表 (List)、元组 (Tuple)、字典 (Dictionary) 和 集合 (Set) 有机地结合在一起，展示了它们在处理复杂业务逻辑时的不同角色

# ==========================================
# 1. 集合 (Set)：处理唯一性与类别
# 场景：记录全店所有不重复的商品类别
# ==========================================
# [2] 创建集合用于去重
categories = {"电子产品", "办公用品", "生活家电"}
categories.add("电子产品")  # 重复添加不会生效
print(f"1. 商品类别库 (Set): {categories}")

# ==========================================
# 2. 字典 (Dictionary)：结构化数据与快速索引
# 场景：模拟数据库，通过 ID 快速查找商品详情 (JSON 基石)
# ==========================================
# [2, 4] 键必须不可变，字典保持插入顺序 (Python 3.7+)
product_catalog = {
    101: {"name": "MacBook Pro", "price": 12999, "category": "电子产品"},
    102: {"name": "键盘", "price": 299, "category": "办公用品"},
    103: {"name": "咖啡机", "price": 899, "category": "生活家电"}
}
print(f'2. 商品目录 (Dict): 查找到 ID 101 为 {product_catalog[101]["name"]}')

# ==========================================
# 3. 元组 (Tuple)：不可变的记录
# 场景：存储不可更改的订单单项快照 (ID, 购买数量, 成交价)
# ==========================================
# [4] 元组保证数据安全性，常用于存储异质数据集
order_item_1 = (101, 1, 12500) # 成交价可能与原价不同
order_item_2 = (102, 2, 280)
print(f"3. 订单项快照 (Tuple): {order_item_1}")

# ==========================================
# 4. 列表 (List)：有序序列与队列操作
# 场景：待处理订单队列 (FIFO)
# ==========================================
# [1] 列表适合实现堆栈或队列
order_queue: List[Tuple] = []
order_queue.append(order_item_1) # 压入订单
order_queue.append(order_item_2)
print(f"4. 当前待处理订单数 (List): {len(order_queue)}")

# ==========================================
# 5. 综合应用：推导式与嵌套结构 (Engineering Practice)
# 场景：提取所有订单中涉及的商品名称
# ==========================================
def process_order_summary(queue: List[Tuple], catalog: Dict):
    # [3] 嵌套结构：从订单列表中提取 ID，再去目录字典里查名字
    # [3] 列表推导式：高效完成数据转换
    item_names = [catalog[item[0]]["name"] for item in queue]
    
    # 场景：计算订单总金额
    total_amount = sum(item[2] for item in queue)
    
    return item_names, total_amount

# 执行处理逻辑
names, total = process_order_summary(order_queue, product_catalog)
print(f"\n--- 处理结果 ---")
print(f"订单商品清单: {names}")
print(f"所有订单总额: {total}")

# [1] 队列模拟：处理完一个订单，将其移出 (FIFO)
processed_order = order_queue.pop(0)
print(f"已处理并移出订单: {processed_order}")
print(f"剩余订单数: {len(order_queue)}")
