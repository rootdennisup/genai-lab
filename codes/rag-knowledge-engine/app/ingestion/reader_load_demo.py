from llama_index.core import SimpleDirectoryReader

from app.ingestion.reader_demo import PSQLReader

# 实例化自定义阅读器
psql_reader = PSQLReader()

# 使用 SimpleDirectoryReader 加载目录，并指定 .psql 文件使用自定义阅读器处理 [7]
reader = SimpleDirectoryReader(
    input_dir="./data", 
    file_extractor={".psql": psql_reader} 
)

documents = reader.load_data()

# 打印加载后的文档内容，此时内容应为 SQL 执行的结果而非 SQL 语句本身 [7]
for doc in documents:
    print(f"文档内容: {doc.text}")
    print(f"文档元数据: {doc.metadata}")