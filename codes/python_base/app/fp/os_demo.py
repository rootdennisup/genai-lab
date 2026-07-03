import os  # 推荐使用这种导入方式，避免覆盖内置函数 open()

# 1. 获取当前工作目录 (Current Working Directory)
# 模拟查看程序当前运行的物理路径
cwd = os.getcwd()
print(f"当前工作目录: {cwd}")

# 2. 访问操作系统环境变量 (Environment Variables)
# 用于实现“代码与配置分离”，例如获取系统路径或自定义变量
path_value = os.environ.get("PATH")
print(f"系统 PATH 变量片段: {path_value[:50]}...")

# 3. 列出指定目录下的文件和文件夹
# 模拟探索当前目录的文件结构
print("\n当前目录下的文件列表:")
for item in os.listdir("."):
    print(f" - {item}")

# 4. 路径与文件状态检查 (os.path 子模块)
# 检查某个文件或目录是否存在
target_file = "test_dir"
if not os.path.exists(target_file):
    # 创建新目录
    os.mkdir(target_file)
    print(f"\n已创建目录: {target_file}")
else:
    # 删除目录
    os.rmdir(target_file)
    print(f"\n已清理目录: {target_file}")

# 5. 探索模块内置功能
# 利用内置函数查看 os 模块支持的所有接口
# print(dir(os))  # 取消注释可查看完整函数列表
# help(os)       # 取消注释可查看详细帮助手册