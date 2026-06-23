# 1. 写入文件（使用 'w' 模式，会覆盖原内容）
with open('tmp/example.txt', 'w', encoding='utf-8') as f:
    f.write("Python 工程化开发\n")
    f.write("文件读写基础测试")

# 2. 读取文件（使用 'r' 模式）
with open('tmp/example.txt', 'r', encoding='utf-8') as f:
    content = f.read()
    print(f"读取到的内容：\n{content}")

# 3. 逐行读取（适合大文件）
with open('tmp/example.txt', 'r', encoding='utf-8') as f:
    print("逐行遍历：")
    for line in f:
        print(line.strip())
