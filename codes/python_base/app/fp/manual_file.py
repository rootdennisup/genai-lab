# 1. 打开 (Open)
# 使用 open() 函数，指定文件名和模式（'w' 表示写入）
f = open('tmp/workfile.txt', 'w', encoding='utf-8') 

try:
    # 2. 操作 (Operate)
    # 调用文件对象的方法进行数据写入
    f.write('这是第一行测试数据。\n')
    f.write('这是第二行测试数据。')
    print("文件操作完成。")
    
finally:
    # 3. 关闭 (Close)
    # 显式调用 close() 释放系统资源
    f.close()
    print("文件已安全关闭。")