from urllib.request import urlopen

# 像打开本地文件一样打开互联网资源，如果互联网资源打不开会抛异常
# 1.使用urlopen 打开url
with urlopen('https://docs.python.org/zh-cn/3.14/tutorial/index.html') as response:
    # 2.使用 getcode() 获取响应状态码，200--成功，404--不存在
    print(response.getcode())   # 200

    # 3.使用 read() 读取并返回的字节流数据
    data = response.read(300).decode('utf-8')
    print(f"服务器返回内容: {data}")

# 笔记
## 1.read() 是读取整个网页内容，可使用 response.read(300) 指定读取字节长度
## 2.readline() ，读取文件的一行内容 
## 3.readlines()，读取文件的全部内容，把读取的内容赋值给一个列表变量。