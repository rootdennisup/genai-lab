import csv

# 要写入的数据
data = [["姓名", "年龄", "城市"], ["Alice", 25, "北京"], ["Bob", 30, "上海"]]

# 以写入模式打开名为 output.csv 的文件，并指定编码为 UTF-8。newline='' 用于避免在 Windows 系统中出现空行。
with open('tmp/users.csv', 'w', newline='', encoding='utf-8') as f:
    ## 创建一个 csv.writer 对象，用于写入文件内容
    writer = csv.writer(f)
    # 一次性写入多行
    writer.writerows(data) 

    # # 逐行写入数据
    # for row in data:
    #     writer.writerow(row)



# 读取 CSV
with open('tmp/users.csv', 'r', encoding='utf-8') as f:     # 以只读模式打开名为 data.csv 的文件，并指定编码为 UTF-8。
    # 创建一个 csv.reader 对象，用于读取文件内容
    reader = csv.reader(f)

    # 逐行读取文件内容，每一行数据会被解析为一个列表
    for row in reader:
        print(row) 