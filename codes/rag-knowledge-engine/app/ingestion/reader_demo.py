from llama_index.core.readers.base import BaseReader
from llama_index.core.schema import Document
from typing import Any, List, Optional, Dict
from pathlib import Path

class PSQLReader(BaseReader):
    """自定义 PSQL 阅读器：读取 SQL 文件并执行，将结果转为 Document"""
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def load_data(self, file: Path, extra_info: Optional[Dict] = None) -> List[Document]:
        # 1. 读取文件中的 SQL 语句内容
        with open(file, 'r') as f:
            sql_query = f.read()
            
        # 2. 执行自定义逻辑（例如执行 SQL 语句并获取结果）
        # 这里的 execute_sql_and_return_results 是一个模拟函数 [4]
        result_text = self._execute_sql_and_return_results(sql_query)
        
        # 3. 构造元数据并返回 Document 对象列表 [2]
        metadata = {'file_suffix': 'SQL'}
        if extra_info:
            metadata.update(extra_info)
            
        return [Document(text=result_text, metadata=metadata)]

    def _execute_sql_and_return_results(self, sql: str) -> str:
        # 此处省略真实的数据库连接和执行逻辑（如使用 psycopg2） [4]
        # 模拟返回数据库查询结果
        return "(1, '测试数据A')\n(2, '测试数据B')"