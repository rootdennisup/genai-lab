"""
完整 RAG 数据加载 Demo，流程如下：

文件
 ↓
Reader           -- 文档读取
 ↓
Document         -- 原始文档对象
 ↓
Metadata         -- 元数据管理
 ↓
Text Cleaning    -- 文本清洗
 ↓
Chunk            -- 文本切分
 ↓
Node             -- 知识块对象
"""

import re
from pathlib import Path
from llama_index.core import Document, SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import TransformComponent

# =====================================================
# 1. 文本清洗组件
# =====================================================
class TextCleaner(TransformComponent):
    """
    RAG 数据预处理阶段，清洗 Document 文本，作用：
    1. 去除乱码
    2. 去除特殊字符
    3. 保留业务文本
    """
    def __call__(self, nodes, **kwargs):

        for doc in nodes:
            if isinstance(doc, Document):
                clean_text = re.sub(
                    r"[^\u4e00-\u9fa5A-Za-z0-9，。？！：；（）\n]",
                    "",
                    doc.get_content()
                )

                # Document 不支持 doc.text=  ，使用 set_content
                doc.set_content(clean_text)

        return nodes

# =====================================================
# 2. 加载 Document
# =====================================================
def load_documents():
    print("\n====== Step1 Document Loading ======")
    documents = SimpleDirectoryReader(
        input_dir="./data"
    ).load_data()

    print(
        f"加载 Document 数量:{len(documents)}"
    )

    for doc in documents:
        print("\nDocument:")
        print(
            doc.text[:100]
        )
        print(
            "Metadata:"
        )
        print(
            doc.metadata
        )
        
    return documents

# =====================================================
# 3. 添加业务 Metadata
# =====================================================
def enrich_metadata(documents):
    print("\n====== Step2 Metadata Enrich ======")
    
    for doc in documents:
        doc.metadata.update({
            "source":
            "enterprise_hr_kb",
            "department":
            "HR",
            "document_type":
            "policy",
            "version":
            "v1.0"
        })

    return documents

# =====================================================
# 4. Ingestion Pipeline
# =====================================================
def build_pipeline():

    pipeline = IngestionPipeline(
        transformations=[
            # 2. 自动将文档分割为 Node
            SentenceSplitter(chunk_size=300,chunk_overlap=50),
            # 1.文本清洗
            TextCleaner()
        ]
    )
    
    return pipeline

# =====================================================
# 5. 执行
# =====================================================
def run():

    # Step1
    documents = load_documents()

    # Step2
    documents = enrich_metadata(documents)

    # Step3
    pipeline = build_pipeline()

    print("\n====== Step3 Document -> Node ======")
    nodes = pipeline.run(documents=documents)

    print(f"生成 Node 数量:{len(nodes)}")

# 查看 Node
    for i,node in enumerate(nodes[:3]):
        print("\n----------------")
        print(f"Node {i}")
        print(node.text)
        print("Metadata:")
        print(node.metadata)

if __name__ == "__main__":
    run()





