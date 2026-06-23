# 使用 with 语句处理文件
# 1. 它会自动打开文件
with open('data.txt', 'w', encoding='utf-8') as f:
    # 2. 在缩进块内进行操作 (Operate)
    f.write('这是通过 with 语句写入的内容。\n')
    f.write('它会自动帮我关闭文件，非常安全。')
    
    print("正在写入数据...")
    # 此时文件是打开状态

# 3. 释放资源 (自动 Close)
# 一旦代码运行出缩进块，Python 会自动调用 f.close()
print("代码已退出 with 块，文件已被自动关闭。")

# 验证：尝试在外部读取会发现 f 已经关闭
print(f.closed)  # 会输出 True