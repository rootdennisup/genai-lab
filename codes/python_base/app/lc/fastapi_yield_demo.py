import sys

# 场景：海量数据流式处理模拟，处理 10,000,000 个数据项

# 1. 传统方式：使用列表（一次性加载到内存）
def get_list_data(n):
    result = []
    for i in range(n):
        result.append(f"数据项_{i}")
    return result

# 2. 生成器方式：使用 yield（惰性求值）
def get_generator_data(n):
    for i in range(n):
        # 运行到这里会暂停，并返回当前值
        yield f"数据项_{i}"

# --- 运行测试 ---
count = 10000000

# 列表测试
list_data = get_list_data(count)
print(f"列表占用内存: {sys.getsizeof(list_data) / 1024 / 1024:.2f} MB")

# 生成器测试
gen_data = get_generator_data(count)
print(f"生成器对象占用内存: {sys.getsizeof(gen_data) / 1024:.2f} KB")

# 模拟流式处理：只处理前 3 条
print("\n开始流式读取数据：")
for _ in range(3):
    print(next(gen_data))

print("... 此时函数处于暂停状态，等待下一次 next() 调用 ...")
