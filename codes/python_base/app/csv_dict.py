import csv

data = [
    {'Name': 'Alice', 'Age': '30', 'City': 'New York'},
    {'Name': 'Bob', 'Age': '25', 'City': 'Los Angeles'}
]

with open('tmp/output.csv', mode='w', encoding='utf-8', newline='') as file:
    fieldnames = ['Name', 'Age', 'City']
    # 将字典写入 CSV 文件
    csv_dict_writer = csv.DictWriter(file, fieldnames=fieldnames)
   
    # 写入表头
    csv_dict_writer.writeheader()
   
    # 写入数据
    for row in data:
        csv_dict_writer.writerow(row)


with open('tmp/output.csv', mode='r', encoding='utf-8') as file:
    # 将 CSV 文件的每一行解析为字典
    csv_dict_reader = csv.DictReader(file)
   
    for row in csv_dict_reader:
        print(row)




