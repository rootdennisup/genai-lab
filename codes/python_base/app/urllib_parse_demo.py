from urllib.parse import urlparse, urlencode

# 1. 解析 URL
url = "https://www.example.com/search?q=python&page=1"
parsed = urlparse(url)
print(f"路径部分: {parsed.path}") # 输出: /search
print(f"查询参数: {parsed.query}") # 输出: q=python&page=1
print(parsed) # ParseResult(scheme='https', netloc='www.example.com', path='/search', params='', query='q=python&page=1', fragment='')

# 2. 编码查询参数
params = {'name': '张三', 'city': '北京'}
encoded_query = urlencode(params)
print(f"编码后的参数: {encoded_query}") # 自动处理中文编码
