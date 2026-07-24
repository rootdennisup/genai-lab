import re
from llama_index.core.schema import TransformComponent
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter


# 1. 定义自定义清洗转换器
class TextCleaner(TransformComponent):
    """自定义数据清理转换器：利用正则表达式过滤非标准字符"""

    def __call__(self, nodes, **kwargs):
        for node in nodes:
            # 正则表达式逻辑：仅保留中文字符 (\u4e00-\u9fa5)、英文字母 (A-Za-z)、数字 (0-9) ，以及常用的中文和英文标点符号，剔除其余所有杂质字符
            node.text = re.sub(
                r"[^\u4e00-\u9fa5A-Za-z0-9，。？！“”‘’；：【】《》（）\[\]\"\'\.\,\?\!\:\;\(\)\n\r]", 
                "", 
                node.text
            )
        return nodes
        
# 2. 在数据摄取管道中使用
def run_demo():
    # 加载文档
    docs = SimpleDirectoryReader(input_dir="./data").load_data()
    
    # 构造数据摄取管道
    pipeline = IngestionPipeline(
        transformations=[
            # 1. 执行自定义的正则清洗转换器
            TextCleaner(), 
            # 2. 自动将文档分割为 Node
            SentenceSplitter(chunk_size=500, chunk_overlap=20), 
            # 还可以后续添加元数据抽取等
            # TitleExtractor(llm=llm), 
        ]
    )
    
    # 运行管道处理原始文档，处理后的 nodes 将是经过正则过滤后的“干净”知识块
    nodes = pipeline.run(documents=docs)
    return nodes

if __name__ == "__main__":
    processed_nodes = run_demo()
    print(f"处理完成，共生成 {len(processed_nodes)} 个节点")

