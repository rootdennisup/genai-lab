# 在线检索与生成阶段 (Retrieval & Generation)--检索优化

实际生产中的 RAG，Retriever 往往是效果瓶颈；很多 RAG 效果不好，不是因为 LLM 不够强，而是：**找错知识 → LLM 再强也只能胡说**。检索优化是提升系统从“原型”向“生产就绪”跨越的核心环节，所以生产级 RAG 会围绕检索阶段优化：
```text
Query Rewrite(Query 理解)
      ↓
Multi Query(多角度召回)
      ↓
Retriever(初步召回，粗筛)
      ↓
Rerank（精排）
      ↓
Contextual Retrieval（上下文增强）
```

## 1 Query Rewrite（查询改写）
查询重写属于“检索前处理”（Pre-Retrieval），旨在将原始的用户输入转化为一个或多个更有利于检索的表达形式，以解决用户表达模糊或由于向量偏移导致的检索偏差。

### 1.1 Query Rewrite 的本质
- **核心问题**：用户输入通常不是一个好的搜索 Query。
- 场景复现：
    ```text
    用户：它多少钱？

    聊天机器人的上下文：
        用户：我想买这个帐篷
        AI：这是3×3米防水帐篷
        用户：它多少钱？

    Retriever 检索到：它多少钱？（Embedding 没有明确语义，检索失败。）
    ```
- **目的**：把用户 Query 改写成，更适合检索的完整查询
    ```text
    用户：它多少钱？
    Rewrite Query：3×3米防水帐篷售价是多少？

    Rewrite Query --> Embedding --> Vector Search
    ```
- **Query Rewrite 的本质**
  - 将用户表达特点（口语化、短、模糊、带上下文）转化成 检索表达方式（完整、关键词丰富、语义明确）

### 1.2 常见 Query Rewrite 方法

#### 1> 大模型简单重写
借助 LLM 充当查询生成器，根据原始问题生成变体问题。助于从不同角度覆盖语义空间，提高找回相关知识的概率。示例：
- Prompt：
  ```text
    你是一个搜索优化专家。将用户问题改写成适合知识库检索的问题。
    用户问题：{query}
  ```
- 输入：`我之前买的那个什么时候发货？`
- 输出：`查询订单配送状态和预计发货时间`

#### 2> 假设性文档嵌入
- LLM 首先根据问题生成一个“假设性答案”，然后对该答案（而非问题本身）进行向量化检索。
- 该方法的逻辑是：在向量空间中，答案与目标知识块的语义往往比问题与知识块更接近

#### 3> 多步查询转换
将复杂的复合问题拆解为多个顺序执行的子问题。每一步的查询都基于前一步的推理结果生成，直到能够完整回答原问题。

### 1.3 Query Rewrite 对 RAG 的提升
主要提升 Recall。

```text
知识库：员工休假管理制度
用户：怎么请假？

原 Query 召回请假可能低。
Rewrite：员工请假申请流程 （召回提高）
```

## 2 Multi Query（多查询检索）
多查询优化通常与查询重写结合，其核心思想是“以多换准”，通过并发检索多个查询来弥补单一检索的不足。
- **子问题查询引擎**：根据可用的知识库/工具，将输入问题分解为多个可以独立解答的子问题。例如，询问“北京和上海的人口差距”，系统会分解为“查询北京人口”和“查询上海人口”两个任务并行执行。
- **融合检索**：对重写后的多个问题分别执行检索，或同时在向量索引、关键词索引等不同类型的索引上进行检索。系统会收集所有召回的节点（Nodes），利用 RRF (倒数排名融合) 算法对结果进行去重和重新评分。

### 2.1 为什么需要 Multi Query
一个 Query 可能只有一个视角。一个 Query 可能覆盖不足。

```text
用户：如何申请年假？

可能对应多个知识：
    年假申请流程
    员工休假制度
    OA审批流程
    HR考勤规定
```
Multi Query：让 LLM 生成多个查询。

### 2.2 Multi Query 流程
```text
    User Query
        |
        |
    LLM Query Generator
        |
 ---------------------
 |          |          |
Q1         Q2         Q3
 |          |          |
Vector   Vector    Vector
Search   Search    Search
 |          |          |
TopK     TopK      TopK
       Merge
         |
      Deduplicate
         |
      Rerank
```

- 为什么有效？
  - Embedding Search 本质是**寻找语义附近区域**。
  - 一个 Query只能代表一个点，2而Multi Query相当于多个搜索入口。

- Multi Query 缺点
  - 增加了 延迟、token、费用
  - 只用于复杂 query

## 3 Rerank（重排序）
重排序属于“检索后处理”（Post-Retrieval），是提升检索精确度的最重要手段。它可以确保最准确、最相关的知识块排在上下文的最前端，从而显著减少大模型的生成幻觉并提高回答质量

- 为什么需要 Rerank？
  - Vector Search 的目标是快速找到候选；但 Embedding Similarity 不够精确。
  - 示例：
    ```text
    TOP 5
        1. 员工迟到处罚
        2. 员工请假流程
        3. 考勤系统说明
        4. 公司文化
        5. 入职流程
    
    真正答案: 1

    Vector Similarity 结果可能是：
        3
        2
        1

    所以需要增加 Reranker
    ```
### 3.1 Retriever vs Reranker
- Retriever 负责：100万 --> 100 ，目标是 Recall（召回）。
- Reranker 负责：100 --> 5，目标是 Precision（精确）。

### 3.2 Rerank 原理
- Retriever 使用 Bi-Encoder。结构如下：
    ```text
    Query
    ↓
    Embedding


    Document
    ↓
    Embedding

    Similarity
    ```
    执行速度快。

- Reranker 使用 Cross Encoder。输入 `Query + Document` 一起进入大模型，示例：
    ```text
    Query:迟到超过30分钟如何处理？
    Document:员工迟到超过30分钟按半天缺勤处理

    模型直接输出：0.98
    ```

### 3.3 常见 Rerank 模型
- Cohere Rerank：商业闭源模型，效果优秀且易于通过 API 调用。
- BGE-Reranker： 开源的高性能重排序模型，适合本地部署（如使用 TEI 工具）。


### 3.4 Rerank 代价
缺点：慢


## 4 Contextual Retrieval（上下文检索）
这是 Anthropic 提出的一个 RAG 优化方向。用于解决 Chunk 单独存在时，语义不完整。
- 句子窗口检索：这是最典型的上下文增强策略。检索时使用较小的知识块（如单句）以实现语义的精确匹配；但在生成阶段，通过 元数据替换处理器 (MetadataReplacementPostProcessor)，自动将该节点替换为其在原始文档中前后关联的完整“窗口”内容（如前后各 3 句）输入给 LLM。
- Agent 上下文检索器： 在多工具 Agent 场景下，给 Agent 配备专门的上下文检索器（如存储术语缩写解释、背景规则等）。Agent 在选择工具或理解问题时先检索这些背景知识，从而显著降低工具选择出错的概率。
- 父子节点递归检索：构造分层索引，先检索语义更集中的子节点（小块），一旦命中，则递归召回对应的父节点（大块）作为上下文。


### 4.1 为什么 Chunk 会丢上下文
- 原文
  ```text
    第三章 请假制度
    员工连续工作满12个月，可以享受带薪年假。
    年假最多15天。
  ```
- 切 Chunk
  ```text
    Chunk1：员工连续工作满12个月，可以享受带薪年假。
    Chunk2：年假最多15天。
  ```
- 问题：Chunk2 不知道哪个公司？什么条件？什么年假

### 4.2 Contextual Retrieval 思路
切 Chunk 后：给每个 Chunk 增加上下文。
```text
原：年假最多15天。

变：
【员工考勤与休假管理制度】
第五章 员工年假管理：
员工连续工作满12个月，可以享受带薪年假。
年假最多15天。
```

### 4.3 流程
- 传统流程：`Document --> Chunk --> Embedding`
- Contextual Retrieval:
  ```text
    Document --> Chunk --> LLM生成Chunk Context --> Context + Chunk --> Embedding
  ```






