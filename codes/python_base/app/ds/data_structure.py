#!/usr/bin/python3
from collections import deque

# class Stack:
#     def __init__(self):
#         self.stack = []

#     def push(self, item):
#         self.stack.append(item)

#     def pop(self):
#         if not self.is_empty():
#             return self.stack.pop()
#         else:
#             raise IndexError("pop from empty stack")

#     def peek(self):
#         if not self.is_empty():
#             return self.stack[-1]
#         else:
#             raise IndexError("peek from empty stack")

#     def is_empty(self):
#         return len(self.stack) == 0

#     def size(self):
#         return len(self.stack)

# # 使用示例
# stack = Stack()
# stack.push(1)
# stack.push(2)
# stack.push(3)

# print("栈顶元素:", stack.peek())  # 输出: 栈顶元素: 3
# print("栈大小:", stack.size())    # 输出: 栈大小: 3

# print("弹出元素:", stack.pop())  # 输出: 弹出元素: 3
# print("栈是否为空:", stack.is_empty())  # 输出: 栈是否为空: False
# print("栈大小:", stack.size())    # 输出: 栈大小: 2

# # 创建一个空队列
# queue = deque()

# # 向队尾添加元素
# queue.append('a')
# queue.append('b')
# queue.append('c')

# print("队列状态:", queue)  # 输出: 队列状态: deque(['a', 'b', 'c'])

# # 从队首移除元素
# first_element = queue.popleft()
# print("移除的元素:", first_element)  # 输出: 移除的元素: a
# print("队列状态:", queue)            # 输出: 队列状态: deque(['b', 'c'])

# # 查看队首元素（不移除）
# front_element = queue[0]
# print("队首元素:", front_element)    # 输出: 队首元素: b

# # 检查队列是否为空
# is_empty = len(queue) == 0
# print("队列是否为空:", is_empty)     # 输出: 队列是否为空: False

# # 获取队列大小
# size = len(queue)
# print("队列大小:", size)            # 输出: 队列大小: 2


# # 案例 1：列表推导式 - 获取 1-10 中所有偶数的平方
# # 语法结构：[表达式 for 变量 in 序列 if 条件]
# squares = [x**2 for x in range(1, 11) if x % 2 == 0]
# print(f"偶数的平方列表: {squares}")  # 输出: [4, 16, 36, 64, 100]

# # 案例 2：字典推导式 - 将名字列表转为 {名字: 长度} 的字典
# names = ["Alice", "Bob", "Charlie"]
# name_lengths = {name: len(name) for name in names}
# print(f"名字长度字典: {name_lengths}") # 输出: {'Alice': 5, 'Bob': 3, 'Charlie': 7}


# 嵌套结构案例：字典中嵌套列表
user_data = {
    "username": "coder_api",
    "roles": ["admin", "developer"], # 字典的值是一个列表
    "projects": [
        {"id": 1, "name": "FastAPI 学习"}, # 列表里又嵌套了字典
        {"id": 2, "name": "Pytest 自动化"}
    ]
}

# 访问嵌套数据
# 获取第一个项目的名称
first_project_name = user_data["projects"][0]["name"]
print(f"第一个项目名称: {first_project_name}")

# 结合推导式处理嵌套结构
# 提取所有项目的 ID 列表
project_ids = [p["id"] for p in user_data["projects"]]
print(f"所有项目 ID: {project_ids}")





