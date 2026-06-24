from pathlib import Path

# 1. 获取路径信息
current_dir = Path.cwd() # 获取当前工作目录
print(f"当前目录: {current_dir}")

# 2. 路径拼接（使用 / 运算符）
file_path = current_dir /"tmp"/ "test_dir" / "example.txt"

# 3. 创建目录（parents=True 表示自动创建父目录，exist_ok=True 表示已存在时不报错）
file_path.parent.mkdir(parents=True, exist_ok=True)

# 4. 文件判断与属性获取
if not file_path.exists():
    file_path.write_text("Hello Pathlib!", encoding="utf-8") # 直接写文本

print(f"文件名: {file_path.name}")       # example.txt
print(f"后缀名: {file_path.suffix}")     # .txt
print(f"是否为文件: {file_path.is_file()}")







