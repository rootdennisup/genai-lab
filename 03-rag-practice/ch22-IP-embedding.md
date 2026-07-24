# 离线索引阶段(Indexing Pipeline)-- 向量化（Embedding）

## 1 向量化基础
向量化（也称嵌入，Embedding）是将分割后的**知识块（Node）**或**查询问题**转化为能够被计算机处理、表达语义信息的**高维浮点数（向量）**的过程。

### 1.1 向量化的本质
向量化的本质是把**自然语言**转化为捕捉了**语义信息的多维向量**。与传统的关键词匹配不同，基于向量的检索是根据向量在数学空间中的“相似程度”进行的。即使两个文本的表面用词不同，只要它们表达的语义相似，其生成的向量在数学上也会彼此“接近”。

#### 为什么需要向量化
因为传统关键词搜索无法理解语义。示例：
```text
用户问题：迟到半小时有什么处罚？

知识库：超过30分钟未打卡，按照半天缺勤处理。

关键词：迟到、处罚 ，没有完全匹配。

Embedding：迟到半小时-->相似-->超过30分钟未打卡 ，可以召回
```

### 1.2 向量化贯穿 RAG 的两个核心阶段
- **数据索引阶段**：将分割后的知识块（Node）通过嵌入模型转换为向量，并连同原始内容和元数据存入**向量数据库**。
- **数据查询阶段**：将用户输入的自然语言问题实时转换为向量，然后在向量库中检索语义**最接近的前 K 个知识块**（top_K），作为大模型生成的参考上下文。


## 2 Embedding Model
Embedding Model（嵌入模型，向量模型）负责把文本转换成向量（Vector），也就是把人类语言转换成机器可以计算相似度的数学空间。

### 2.1 Embedding Model 核心原理
- **输入文本**
  - **示例**：`What is RAG?`
  - **Tokenizer 拆成 token**：
    ```text
    What
    is
    RAG
    ?
    ```
  - **转换：**
    ```text
    token id

    [
    2054,
    2003,
    ...
    ]
    ```
  
  - **Transformer 编码**：

    Embedding Model 本质也是 Transformer。结构类似：
    ```text
    Token -> Embedding Layer -> Transformer Encoder -> Hidden States -> Pooling -> Vector
    ```

### 2.2 为什么不同文本会距离不同
Embedding Model 训练目标是使得：
- **相似文本**距离近：
  ```text
  A：如何申请年假？
  B：员工怎样办理休假？

  距离：0.92
  ```

- **不相关文本**距离远：
  ```text
  A：如何申请年假？
  B：Redis如何持久化？

  距离：0.12
  ```

- 从而形成**语义空间**：
  ```text
        年假申请
            ●

        ●
  休假流程


                         Redis
                            ●
  ``

### 2.3 Embedding 如何训练
- **核心思想**：`Contrastive Learning`（对比学习）。
- 给模型足够的样本：
  - 正样本：
    ```text
    问题: 什么是年假？
    答案: 员工每年享有带薪休假。
    ```
    - 希望：
       ```text
       Embedding(question)
          |
          |
       距离近
          |
       Embedding(answer)   
       ```
  - 负样本：
    ```text
    问题: 什么是年假？
    答案: Redis是一种缓存数据库。
    ```
    - 希望：距离远

- **训练目标**：
  - 最大化 `positive similarity`（正向相似性）
  - 尽量降低 `negative similarity`（负相似性）

### 2.4 常见 Embedding Model

#### 1> OpenAI Embedding
- `text-embedding-3-small`
  - 维度：1536
  - 特点：成本低、效果好、通用

- `text-embedding-3-large`
  - 维度：3072
  - 特点：更强语义能力、成本更高
  - 适用：企业知识库

#### 2> BGE 系列（国内常用）
- `BAAI/bge-large-zh`
  - 优势：中文效果优秀、开源、可私有部署
  - 很多企业 RAG 使用：
    ```text
    BGE + Milvus + Rerank
    ```
#### 3> E5 系列
- `multilingual-e5-large`
- 特点：多语言效果不错（中、英、德）


## 3 向量相似度(Embedding Similarity)

- 用户 Query
    ```text
    迟到超过30分钟如何处理？

    转换：
    Q = [
    0.12,
    0.45,
    0.78
    ]
    ```
- 知识库 Chunk：
    ```text
    员工迟到超过30分钟，按照半天缺勤处理。

    转换：
    D = [
    0.10,
    0.40,
    0.75
    ]
    ```
- 问题：怎么判断 Q 和 D 语义相似？
  - 答案：计算两个向量之间的距离。

常用的方法：
- Cosine Similarity（余弦相似度，RAG 最常用）
- Dot Product（点积）
- Euclidean Distance（欧氏距离）

### 3.1 理解向量空间
为了方便，把 Embedding 降到二维，有3个文本：
```text
A:如何申请年假？

B:员工怎样办理休假？

C:Redis如何持久化？
```
Embedding：
```text
A = [0.8, 0.6]

B = [0.7, 0.7]

C=[-0.8,0.2]
```
- A vs. B 两个向量方向接近，因此语义相似。
    ```text
          y

          |
      B ● |
        / |
       /  |
      /   |
     ● A  |
   --------- x
    ```
- B vs. C 方向差异大，因此语义不相似
    ```text
          y

          |
          |
     B ●  |
        \ |
         \|
  --------+----------x
        /
       /
   C ●
    ```

### 3.2 Cosine Similarity（余弦相似度）
- **核心思想**：不是比较长度，而比较**两个向量夹角**。
- **公式**：
    $$
    \text{similarity}(A,B)=\cos(\theta)=\frac{A \cdot B}{\|A\|\|B\|}
    $$
    - `\frac{分子}{分母}` → 分数
    - `A \cdot B` → 向量点积
    - `\|A\|` → 向量的 L2 范数（长度）
    - `\theta` → 两个向量夹角
#### 分子：向量点积
$$
A \cdot B = a_1b_1 + a_2b_2 + ... + a_nb_n
$$

示例：
```text
A：[0.8,0.6]
B：[0.7,0.7]

A⋅B = 0.8*0.7 + 0.6*0.7 = 0.98
```
#### 分母：向量长度
$$
\|A\|=\sqrt{x_1^2+x_2^2+\cdots+x_n^2}
$$
- `\sqrt{}` → 开根号
- `x_1^2` → x1 的平方
- `\cdots` → 数学省略号
- `\|A\|` → 向量范数（比 |A| 更严谨）

示例：
```text
A：[0.8,0.6]
长度：√(0.8²+0.6²) = 1

B：[0.7,0.7]
长度：√(0.7²+0.7²) = 0.99
```

最终结果，接近 1，说明非常相似：
$$
Similarity(A,B)=\frac{0.98}{1 \times 0.99}
\approx 0.99
$$

### 3.3 在 RAG 中向量演绎
- 离线阶段
    ```text
    Chunk1:员工迟到规则
    Embedding:[0.23,0.55,...]

    Chunk2:Redis缓存机制
    Embedding:[0.91,0.12,...]

    Chunk3:请假流程
    Embedding:[0.31,0.51,...]
    ```
- Query 向量化
- 计算 Similarity
   ```text
    Query vs Chunk1  --> 0.91

    Query vs Chunk2 --> 0.12

    Query vs Chunk3 --> 0.85
   ```
- 排序:
   ```text
    Chunk1 > Chunk3 > Chunk2
   ```
- 取 TopK

### 3.4 pgvector 中向量演绎
- 表结构：
    ```sql
    CREATE TABLE knowledge_chunk (
        id BIGSERIAL,
        content TEXT,
        embedding VECTOR(1536)
    );
    ```
- 用户query，先生成 query_embedding
- 查询SQL
    ```sql
    SELECT content, embedding <=> query_embedding AS distance
    FROM knowledge_chunk
    ORDER BY distance
    LIMIT 5;
    ``

| 操作符 | 含义                               | 本质                | 常用场景            |
| ------ | ---------------------------------- |--------------------|--------------------|
| `<=>`  | Cosine Distance(余弦距离)          | 计算两个向量夹角     | 文本 RAG 最常用     |
| `<->`  | L2 Distance(欧氏距离)              | 两个点之间的直线距离 | 图像、空间数据       |
| `<#>`  | Inner Product Distance（内积距离） | 向量点积            | 归一化向量           |

### 3.5 Similarity 和 Distance 的区别
- Similarity:越大越相似
  ```text
  1   很相似
  0   无关系
  -1  相反
  ```
- Distance:越小越相似
  ```text
  0    最近
  1+   更远
  ```

### 3.6 Embedding Similarity 的局限
- **问题1：语义相似但答案不同**
  ```text
  两个文档：
     员工年假10天
     员工年假20天
  
  Embedding 值非常接近，但是答案不同
  ```
  - 解决方法：`Embedding + Rerank`

- **问题2：Embedding 不擅长精确数字**
    ```text
    产品尺寸是多少？
    
    Embedding 不擅长 120cm
    ```
  - 解决方法：`Embedding + BM25 Keyword Search + Metadata Filter + Rerank`

## 4 向量维度 & 向量质量
向量维度和向量质量是衡量嵌入模型（Embedding Model）性能及其对业务支撑能力的核心指标。

### 4.1 向量维度(Vector Dimensions)
- 向量维度是指将一段文本（知识块）通过嵌入模型转换后得到的高维浮点数**数组的长度**。
- 向量维度代表了文本在数学空间中被拆解的特征维度，**每一个数值都捕捉了语义的一个侧面**。

    ```text
    ## 执行：
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input="员工迟到超过30分钟如何处理"
    )

    ## 返回：
    {
    "embedding": [
        0.0023,
        -0.0123,
        0.0345,
        ...
    ]
    }
    ```
    如上示例，数组长度是 1536 ，即维度。

- **存储与性能影响**：
  - **存储开销**：维度越高，占用的存储空间越大。例如在 pgvector 中，每个向量占用的存储约为 4 * 维度 + 8 字节。
  - **检索速度**：维度越高，计算向量相似度（如余弦相似度）时的数学运算量越大，在大规模数据检索时会对性能产生挑战。
  ```text
  Q：维度越高就越好吗？
  A：维度低表达关系比较简单，维度越高表达能力越强，但是存储也更大、搜索更慢。
  ```

- **数据库限制与应对**：
  - 某些索引类型对维度有限制。例如 pgvector 的 vector 类型最多支持 2,000 维。
  - **应对策略**：对于超高维度（如 16,000 维），可以采用 **半精度向量** (halfvec) 将存储减半，或者使用 **二进制量化** (Binary Quantization) 将向量映射为位（bit）类型，从而在索引时支持高达 64,000 维。

## 4.2 向量质量 (Vector Quality)
向量质量直接决定了 RAG 系统的“检索召回精确度”，进而影响大模型的生成效果。

- **质量的核心体现**：高质量的向量应能精准捕获文本语义。这意味着：
  - **语义相似度匹配**：即使两段文本的表面词汇完全不同，只要语义接近，其向量在数学空间中也应当“彼此靠近”。
  - **区分度**：高质量向量能有效区分细微的语义差别，避免在检索时召回大量无关的噪声数据。

- **影响向量质量的因素**：
  - **嵌入模型的能力**：不同模型生成向量的质量差异巨大，可以通过 **MTEB** (Massive Text Embedding Benchmark) 等基准测试来评估模型的优劣。
  - **数据预处理**：在向量化之前，通过 **文本清洗** 去除冗余字符、噪声信息（如 HTML 标签、OCR 乱码），能显著提升向量表达的纯净度。
  - **切分粒度**：过大或过小的知识块（Chunk）都会影响向量对语义的表达。例如，使用 SemanticSplitterNodeParser（语义分割器）可以确保每个 Node 内的语义具有高度相关性，从而提升向量化后的质量。

- **向量质量的评估指标**：通常使用以下指标量化向量检索的质量：
  - **命中率(Hit Rate)**：期望的知识块是否出现在检索出的前 K 个结果中。
  - **平均倒数排名(MRR)**：衡量正确答案在检索结果中的排名位置，排名越靠前质量越高。
  - **忠实度(Faithfulness)**：生成的答案是否能从检索出的向量上下文中得到证实，从侧面反映了检索质量对幻觉的抑制能力。

## 5 LlamaIndex 中的向量化实现
在 LlamaIndex 框架中，向量化主要通过以下方式实现：

- **统一接口**：所有嵌入模型组件都派生自 BaseEmbedding，提供 `get_text_embedding`（处理单条文本）和 `get_text_embedding_batch`（批量处理）接口。
- **自动化流水线**：嵌入模型本身也是一个转换器（TransformComponent）。它可以被插入到 IngestionPipeline（数据摄取管道）中，使文档在分割后自动生成向量并存入向量库，无需额外编码。


















