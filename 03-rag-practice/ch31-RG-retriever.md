# 模块3：在线检索与生成阶段 (Retrieval & Generation)--检索模块 (Retriever)

在线检索与生成阶段简易流程：
```text
User Query --> Query Rewrite (可选) --> Embedding Model --> Query Vector --> Retriever --> TopK Nodes --> Rerank --> Context --> LLM --> Answer
```

## 1 Retriever 是什么
- Retriever（检索器）负责从知识库中，根据用户 Query 找到最相关的知识片段（Node/Chunk），提供给 LLM 生成答案。
- 从上述 RAG 流程中，我们可以理解：
  - Embedding Model：负责把文本（用户问题）变成向量
  - Vector Database：负责存储和快速搜索
  - **Retriever**：负责**制定检索策略并返回最有用的上下文**
  - Retriever 是连接**用户问题**和**知识库**的桥梁。

### 1.1 检索器的作用与接口
检索器的存在是“增强生成”的前提。如果没有它，大模型只能依赖其预训练知识回答问题。
- **核心方法**：`retrieve(query_str)`。该方法接收查询字符串，返回一组与输入条件相关并带有相关性评分（Score）的节点。
- **核心返回对象**：`NodeWithScore`。它包含了检索到的节点内容及其与查询的相似度得分。

### 1.2 检索器的构造方式
检索器通常是基于各种索引组件构造的，主要有两类构造方法：
- **高层 API 快速构造**：使用索引对象的 `as_retriever()` 方法。这种方式简单快捷，支持通过参数（如 similarity_top_k）进行基础配置。
- **底层 API 显式构造**：直接实例化具体的检索器类（如 VectorIndexRetriever）。这种方法提供了更精细的配置能力，但要求开发者熟悉具体的检索器类型。


## 2 Retriever 的核心职责

### 2.1 Query 改写
有时需要通过用户 query 改写，提高检索效果。
```text
用户：迟到半小时怎么办？

query 改写：员工迟到超过30分钟处罚规则
```

### 2.2 Query Embedding
```text
原始 Query：迟到半小时怎么办？

Embedding：
[
0.23,
0.56,
...
]
```

### 2.3 召回 Candidate
- 假设 向量数据库有100万 Node：
    ```text
    Node1
    Node2
    ...
    Node1000000
    ```
- Retriever 计算：
    ```text
    Query Vector VS Node Embedding
    ```
- 找到：TopK=20

### 2.4 Metadata Filter
例如企业知识库：
```text
用户query：查询财务报销制度

Metadata：
{
 "department":"HR"
}

过滤：department=Finance

然后搜索：Finance 文档
```

### 2.5 多路召回
现代 RAG ，Retriever 不只是向量搜索。
```text
          Query
            |
   ------------------
   |                |
Vector Search    Keyword Search
   |                |
Embedding        BM25
   |                |
Top50             Top50
        Merge
          |
       Rerank
```

## 3 Retriever 类型

### 3.1 Vector Retriever
- 原理：
  Embedding Similarity：Query Vector --> Cosine Distance -- > TopK
- 优点：理解语义、泛化能力强
- 缺点：精确关键词弱
- 适合：需要语义理解场景，例如：什么是员工年假？  

### 3.2 Keyword Retriever（BM25）
传统关键词搜索。
```text
Query：TSIN 103997441
BM25匹配：103997441
```

### 3.3 Hybrid Retriever（企业最常用）
结合：Vector Search（语义搜索） + BM25（精确匹配）


### 3.4 Hybrid Retriever 如何融合

#### 方法1：加权融合
- 示例：
    ```text
    final_score = 0.7 * vector_score + 0.3 * keyword_score
    ```
- 假设，Node A：
    ```text
    Vector:0.9
    BM25:0.5
    ```
- 最终：
    ```text
    0.7*0.9 + 0.3*0.5 = 0.78 
    ```

#### 方法2：RRF（Reciprocal Rank Fusion）
- 思想：不是比较分数，而比较排名。

- Vector:
  ```text
    1. Node A
    2. Node B
    3. Node C
  ```
- BM25:
  ```text
    1. Node B
    2. Node D
    3. Node A
  ```
- RRF:
  ```text
    Node A:
        vector排名1
        keyword排名3

    Node B:
        vector排名2
        keyword排名1
  ```
- 最终结果：
  ```text
    Node B
    Node A
  ```

## 4 不同索引类型的检索模式
不同类型的索引对应着不同的检索算法和模式：
- **向量存储索引** (VectorStoreIndex)：仅支持语义相似度检索。常用参数包括 similarity_top_k（召回节点数量）和 filters（元数据过滤器）。
- **文档摘要索引** (DocumentSummaryIndex)： 支持 llm（利用大模型判断摘要相关性）和 embedding（基于摘要向量的相似度匹配）两种模式。
- **树索引 (TreeIndex)**： 支持从根节点逐层向下筛选的 select_leaf 模式，或直接返回所有叶子节点的 all_leaf 模式。
- **关键词表索引** (KeywordTableIndex)： 支持利用大模型提取关键词匹配的 default 模式，或利用 RAKE 工具提取关键词的 rake 模式。
- **知识图谱索引** (PropertyGraphIndex)： 支持 Text-to-Cypher（转换为图查询语言）、向量搜索及关键词搜索等多种子检索器协作















