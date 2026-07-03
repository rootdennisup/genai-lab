
### 业务场景模拟：从数据库或 API 获取一组用户列表后，需要根据特定字段（如年龄、姓名长度）进行快速排序

# 1. 模拟从 Web 接口获取的原始数据（列表嵌套字典）
users = [
    {"name": "Charlie", "age": 30, "score": 85},
    {"name": "Alice", "age": 25, "score": 92},
    {"name": "Bob", "age": 20, "score": 88},
    {"name": "David", "age": 25, "score": 95}
]

print("--- 原始数据 ---")
for u in users: print(u)

# 场景 A：使用 list.sort() 原地修改排序
# 逻辑：lambda 接收列表中的每个字典 x，返回 x["age"] 作为排序依据
users.sort(key=lambda x: x["age"])
print("\n--- 按年龄从小到大排序 (sort) ---")
for u in users: print(u)

# 场景 B：使用 sorted() 返回新列表 + 多级排序
# 逻辑：先按年龄排序，年龄相同时按分数(score)降序排列
# 注意：lambda 可以返回一个元组来实现多级排序逻辑
sorted_users = sorted(
    users, 
    key=lambda x: (x["age"], -x["score"]) 
)
print("\n--- 多级排序：按年龄升序，年龄相同时按分数降序 (sorted) ---")
for u in sorted_users: print(u)

# 场景 C：根据字符串长度排序
# 逻辑：根据名字 (name) 的长度进行排序
users.sort(key=lambda x: len(x["name"]))
print("\n--- 按名字长度排序 ---")
for u in users: print(u)


### 适用场景总结
## 适用：逻辑只有一行、单次使用、提升代码简洁度。
## 禁用：当逻辑变得复杂（需要 if/else 嵌套或多行操作）时，务必改用标准的 def 函数，以保证代码的可读性和可维护性。