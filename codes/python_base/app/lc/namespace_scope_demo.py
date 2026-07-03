# ==========================================
# G (Global): 全局命名空间
# 记录模块级别的变量，模块定义读入时创建 [1]
# ==========================================
app_name = "工程逻辑核心系统"
version = 1.0

def namespace_master_demo():
    # ==========================================
    # E (Enclosing): 嵌套/外层函数命名空间
    # 用于嵌套函数场景，如闭包 [2]
    # ==========================================
    processor_status = "初始化"
    processed_count = 0

    print(f"--- [外层函数] 当前状态: {processor_status} ---")

    def inner_processor():
        # ==========================================
        # L (Local): 最内层局部命名空间
        # 函数调用时创建，记录内部参数和变量 [1]
        # ==========================================
        # 1. 尝试直接访问 B (Built-in) 内置命名空间
        # 包含内置函数如 len(), abs() 等 [1] 局部空间则极其短暂，随函数调用创建，随函数返回或异常而销毁

        built_in_len = len(app_name) 
        
        # 2. 使用 nonlocal 修改 E (Enclosing) 作用域变量
        # 告诉解释器“去外层函数找一个现成的变量” [2] LEGB 查找逻辑
        nonlocal processor_status, processed_count
        processor_status = "运行中"
        processed_count += 1
        
        # 3. 使用 global 修改 G (Global) 作用域变量
        # 告诉解释器“去最外层的全局作用域找变量”，否则会创建同名局部变量 [2]
        global version
        version = 2.0
        
        # L 层的局部变量
        local_task = "清洗数据"
        
        print(f"[内部处理] 任务: {local_task}")
        print(f"[内部处理] 状态已更新为: {processor_status}")
        print(f"[内部处理] 字符串长度 (来自内置函数): {built_in_len}")

    # 执行内部函数
    inner_processor()
    
    print(f"--- [外层函数] 处理结束。最终状态: {processor_status}, 处理数: {processed_count} ---")

# ==========================================
# 执行测试
# ==========================================
if __name__ == "__main__":
    print(f"开始前全局版本: {version}")
    
    namespace_master_demo()
    
    print(f"结束后全局版本 (已被 global 修改): {version}")

    # 演示 NameError 异常
    try:
        # 尝试访问 inner_processor 内部的局部变量(local_task 编译不通过)
        print(local_task)
    except NameError:
        print("\n[异常触发] 无法在外部访问局部变量 'local_task'，因为它已随函数结束而销毁 [1, 2]")