# 模块2：离线索引阶段(Indexing Pipeline)-- 数据加载（Data Ingestion）

离线索引阶段简易流程：
```text
Document --> Chunking --> Node --> Embedding --> Vector DB
```

数据加载是整个 RAG 流程的起点，加载数据的质量直接决定了后续检索的精度，即所谓的“垃圾进，垃圾出（Quality in, quality out）”。

_注：RAG 叙事中使用到的组件主要基于 LlamaIndex 框架。_

## 1 文档上传与读取
在 RAG 应用中，文档上传与读取(Document Loading)是数据处理流程的第一步，其核心目标是读取来自不同数据源（本地文件、数据库、网页、云存储等）的原始知识内容，转化为大模型可以理解的格式。

### 1.1 核心概念：Document 与 Node
- **Document**（文档）：是一个通用的**数据容器**，用于存储从不同数据源（如 PDF、网页、数据库）读取的**原始数据**和**元数据**（如文件名、创建时间等）。
- **Node**（节点）：是 Document 分割后的“块”（Chunk）。Node 是 RAG 流程中索引与检索的基本单位，它会继承 Document 的元数据并记录节点间的关系（如父子、前后关系）。

### 1.2 多样化的数据加载方式
LlamaIndex 通过 **数据连接器（Data Connectors/Readers）**来连接并读取不同形态的数据：

- **本地目录加载(`SimpleDirectoryReader`)**：最常用的组件，能够自动识别扩展名并调用相应的阅读器。它支持 .pdf, .docx, .csv, .md, .jpg/png, .mp3/mp4 等多种格式。

- **网络数据读取**：
  - `SimpleWebPageReader`：简单读取网页 URL 并转换为文本。
  - `BeautifulSoupWebReader`：支持通过 BeautifulSoup 库自定义网页内容的提取规则，过滤无关信息。

- **数据库读取(`DatabaseReader`)**：支持直接通过 SQL 语句从关系型数据库（如 PostgreSQL）中查询数据并提取为 Document 对象。
- **企业级数据同步**：如 RAGFlow 等引擎还支持从 Confluence, S3, Notion, Google Drive 等企业级平台同步数据。

### 1.3 复杂文档的高级解析
对于含有嵌套表格、图表的复杂 PDF，简单的文本提取效果往往不佳：

- **LlamaParse**：是专为复杂文档设计的在线解析服务，能够精准识别并提取 PDF 中的表格，并将其转换为 Markdown 格式，以便大模型更好地理解结构化数据。
- **多模态处理**：针对文档中的图片，可以利用多模态视觉大模型（如 Qwen-VL）提取图片中的文字信息或生成图片摘要，再进行索引。

### 1.4 自定义阅读器（Custom Reader）
当内置组件无法支持特殊格式（如自定义的 .psql 文件）时，开发者可以从 `BaseReader` 派生子类，并实现 `load_data` 接口，自定义读取逻辑和元数据生成规。

#### 自定义阅读器实现示例
- **1> 定义自定义阅读器类**：创建一个继承自 `BaseReader` 的类，并重写 `load_data` 方法。该方法接收文件路径，处理后返回一个 `Document` 对象列表。[reader_demo](../codes/rag-knowledge-engine\app\ingestion\reader_demo.py)

- **2> 将自定义阅读器集成到加载流程中**：通过 SimpleDirectoryReader 的 file_extractor 参数，将特定的文件扩展名（如 .psql）映射到你的自定义阅读器实例上。[reader_load_demo](../codes/rag-knowledge-engine\app\ingestion\reader_load_demo.py)

### 1.5 全栈应用中实现步骤
文档上传通常涉及前端 UI、API 服务和后端索引服务的协作：

- **前端上传**：用户通过 Web UI 选择文件。
- **API 接收**：后端（如基于 FastAPI）通过 /uploadFile 接口接收 UploadFile 对象。 [upload_document](../codes/rag-knowledge-engine\app\api\routes.py)
- **持久化与索引**：API 服务将文件保存至临时目录，调用后端索引服务读取该文件，将其解析为 Document 并增量插入到已有的向量索引中，最后进行持久化存储。


## 2 文档解析
文档解析（Document Parsing）是将原始非结构化数据转化为大模型可理解格式，它直接决定了下游检索与生成的质量。位于文档读取之后，作为将 Document 转化为 Node（知识块）的前置处理。

### 2.1 多样化的数据解析与分割方式
由于原始知识的形态各异，文档解析通常分为以下几种方式：

- **标准文本分割（Text Splitting）**：
  - `SentenceSplitter`：基于段落和句子的自然边界进行分割，通过 `chunk_size` 控制块大小，`chunk_overlap` 保留重叠部分以维持语义连续性。
  - `TokenTextSplitter`：基于词元（Token）数量进行分割，常用于确保内容**不超出大模型的上下文窗口限制**。

- **结构化解析**：
  - 针对特定格式的解析器（如 MarkdownNodeParser, HTMLNodeParser, JSONNodeParser 和 CodeSplitter）能识别标题、列表等语法结构，从而按照文档原本的逻辑层级进行分割。

- **语义分割（Semantic Splitting）**：
  - `SemanticSplitterNodeParser` 不依赖固定长度，而是利用嵌入模型（Embedding Model）计算句子间的语义相似度。当语义发生显著变化时进行分割，最大限度保证了每个 Node 内容在语义上的独立性。

### 2.2 LlamaParse 与复杂文档处理
处理含有复杂布局、嵌套表格或大量图片的 PDF 时，简单的文本提取往往效果欠佳：

- **LlamaParse 服务**： 这是 LlamaIndex 提供的专业在线解析 API，支持 130 多种格式。它能精准提取 PDF 中的表格并转换为 Markdown 格式，帮助大模型更好地理解结构化数据。
- **表格增强解析**： `MarkdownElementNodeParser` 能够识别 Markdown 文档中的表格，并借助大模型自动生成表格摘要（IndexNode 类型）。检索时先匹配摘要，再递归定位到原始表格内容，大幅提升了对财务报表等事实性数据的查询准确率。
- **多模态解析**：针对文档中的图片，可以利用多模态视觉大模型（如 Qwen-VL）生成图片描述文本。这些描述随后被转换成 TextNode 进行索引，使系统能够通过自然语言查询文档中的图像知识。

### 2.3 元数据提取与丰富（Metadata Extraction）
解析不仅仅是提取文本，还包括为 Node 补充额外信息：

- **自动提取**：利用 `SummaryExtractor` 提取内容摘要、`TitleExtractor` 提取章节标题或 `QuestionsAnsweredExtractor` 生成该片段可回答的假设性问题。
- **作用**：丰富的元数据不仅能在检索阶段通过“元数据过滤”缩小搜索范围，还能在生成阶段为大模型提供更准确的上下文参考。

### 2.4 分层与递归解析策略
在大规模文档集中，单一粒度的解析往往无法兼顾检索精度与语义丰富性：

- **分层解析**（Hierarchical Parsing）：`HierarchicalNodeParser` 在多个粒度上（如 128、512、2048 Token）同时对文档进行分割。
- **自动合并与递归检索**：检索时先匹配小粒度的子节点以保证精确度，随后通过递归检索自动合并或扩展到大粒度的父节点（如 `AutoMergingRetriever` 或 `RecursiveRetriever`），从而为大模型提供足够丰富的背景上下文。


## 3 文本清洗
文本清洗（Text Cleaning）的核心目标是去除原始数据中的**噪声、无关字符和冗余信息**，防止噪声干扰嵌入模型（Embedding）的向量生成，以提高数据的质量和后续检索的精确度。位于解析与分割之间，通常作为数据摄取管道中的一个“转换器（Transformation）”。
- [text_cleaning_demo](../codes/rag-knowledge-engine\app\ingestion\text_cleaning_demo.py)

### 3.1 传统规则清洗（基于正则表达式）
利用预定义的规则（如正则表达式）来过滤掉不需要的字符或格式。在 LlamaIndex 中，可以通过自定义 `TransformComponent` 转换器来实现。

- **核心逻辑**：开发者可以定义一个清洗类（如 TextCleaner），在 __call__ 接口中编写清洗逻辑。
  - 示例应用：利用正则表达式保留中文字符、英文字母、数字和常用标点符号，剔除特殊乱码、HTML 标签或其他非法字符。

### 3.2 借助大模型的智能清洗
对于复杂的非结构化数据，简单的规则往往难以处理，此时可以利用 大语言模型（LLM） 的理解能力进行智能预处理。

- **结构化与规范化**：借助 LLM 排除文档中的重复知识，或将知识格式进行结构化处理。
- **特定内容提取**：例如在处理复杂文档时，大模型可以作为“数据清洗工具”，去除表格周围多余的说明文字，仅保留纯净的表格内容。
- **效率提升**：面对海量数据的整理、清洗与抽取，使用 LLM 进行预处理可以显著提高处理效率。

### 3.3 在数据摄取管道中集成清洗流程
为了实现自动化和连续的数据处理，通常会将文本清洗器集成到 LlamaIndex 的 **数据摄取管道（IngestionPipeline）** 中。

- **流水线作业**：原始文档加载后，先经过清洗器处理，再进行文本分割（Splitting）和元数据抽取。
- 代码实现：在构造 `IngestionPipeline` 时，将自定义的清洗转换器（如 TextCleaner()）插入到 transformations 列表中即可。
- 优势：能够确保所有进入向量库的 Node（知识块）都是经过统一标准清洗后的高质量数据。

### 3.4 文本清洗的重要性
- **减少干扰**：原始数据若包含大量无用或矛盾的信息，会直接干扰大模型的推理和生成质量。
- **优化成本**：清洗掉冗余信息可以减少 Embedding 过程中的 Token 消耗，从而降低推理成本。
- **提升检索精度**：更干净的文本有助于嵌入模型（Embedding Model）生成更精确的语义向量，提高召回率。


## 4 元数据提取
元数据提取（Metadata Extraction）是从原始文档或知识块中自动或手动获取描述性信息的过程。元数据被定义为 **“描述数据的数据”**，它以键值对（dict 类型）的形式存储在 Document 或 Node 对象中。

### 4.1 Document & Node Metadata
在 RAG 系统中，**Document 和 Node 的 Metadata（元数据）** 是非常重要的一层信息，主要用于：
- 检索过滤（Metadata Filter）
- 权限控制（ACL）
- 数据溯源（Citation / Source）
- Chunk 管理
- 多租户隔离
- 评估分析
- 上下文组装

不同框架（LlamaIndex、LangChain）叫法略有区别：

- `Document`：通常代表原始文档，侧重于**描述来源属性**（如文件名、路径、作者）。
- `Node / Chunk`：代表切分后的知识单元，侧重于**增强片段特征**（如摘要、假设性问题、上下文窗口），用于提升检索的精确度。

假设企业知识库中上传一个文件 员工考勤管理制度.pdf ：

#### 1> Document 对象示例(Document Metadata)
```json
{
  "text": "员工每日上下班需要打卡，迟到超过30分钟视为迟到一次……",
  "metadata": {
    // 1.身份信息，用于定位原始文档
    "document_id": "doc_hr_001",
    "file_name": "员工考勤管理制度.pdf",
    "file_type": "pdf",
    
    // 2.分类信息，用于 Metadata Filter
    "department": "HR",
    "category": "考勤制度",

    // 3. 权限信息
    "security_level": "internal",
    "tenant_id": "company_001"

    // 4.版本信息，解决旧制度污染问题
    "version": "v3.2",

    "source": "HR知识库",
    "author": "人力资源部",
    "created_at": "2025-01-10",
    "language": "zh-CN"
  }
}
```

#### 2> Node 对象示例(Node Metadata)
```json
{
  "text": "员工每日需要上下班打卡。迟到超过30分钟，记迟到一次。",
  "metadata": {
      "node_id": "node_hr_001_001",
      "document_id": "doc_hr_001",
      "file_name": "员工考勤管理制度.pdf",
      "chunk_index": 1,
      "page_number": 3,
      "section_title": "第二章 考勤规则",
      "chunk_size": 512,
      "token_count": 320,
      "embedding_model":"text-embedding-3-large",
      "created_time":"2025-01-10"
  }
}
```

### 4.2 核心作用
元数据在 RAG 系统中不仅是信息的补充，更是提升性能的关键：

- **提升检索精度**：丰富的元数据（如摘要、标题、假设性问题）能提供原始文本之外的语义参考，提高召回率。
- **辅助元数据过滤**：在检索阶段，可以先通过元数据进行硬过滤（如只查找“南京地区”的文档），再进行向量搜索，从而缩小范围并减少干扰。
- **增强生成质量**：将元数据与文本一同输入大模型，能提供更丰富的上下文背景，帮助模型给出更准确的回答。

### 4.3 元数据的生成方式
元数据的生成主要分为以下三种途径：

- **1> 手动设置与自定义**：

  开发者可以在构造 Document 对象时直接指定元数据，例如：
  ```python
  doc = Document(text="...", metadata={"title": "RAG介绍", "author": "LlamaIndex"})
  ```
- **2> 框架自动生成**

  使用数据连接器（如 SimpleDirectoryReader）读取本地文件时，系统会自动提取文件的基础属性作为元数据，包括：file_path（文件路径）、file_name（文件名）、file_type（文件类型）、file_size（大小）、creation_date（创建日期）等。

- **3> 借助大模型的智能抽取（MetadataExtractor）**

  这是企业级应用中最重要的优化手段。LlamaIndex 提供了多种元数据抽取器，利用大模型自动分析内容并生成深层信息：
  - **摘要抽取器**（`SummaryExtractor`）：为每个 Node 生成内容摘要，适合回答概括性问题。
  - **标题抽取器**（`TitleExtractor`）：为 Node 抽取总结性标题。该抽取器通常是文档级别的，即来自同一文档的不同 Node 会获得相同的标题。
  - **问答抽取器**（`QuestionsAnsweredExtractor`）：生成该片段内容可以回答的多个假设性问题，这能极大增强语义检索的匹配能力。
  - **实体抽取器**（`EntityExtractor`）：自动识别并抽取文本中的地点、人物、组织等实体信息。

### 4.4 元数据的管理与控制
在提取元数据后，灵活控制其在“嵌入”和“生成”阶段的可见性非常重要，以避免冗余信息干扰模型或消耗过多 Token：

- **排除机制**：
  - `excluded_embed_metadata_keys`：设置哪些元数据不参与向量生成（如文件名可能对语义检索无意义）。
  - `excluded_llm_metadata_keys`：设置哪些元数据不输入给大模型生成答案。

- **显示模式**（MetadataMode）：框架支持多种输出模式（如 ALL, EMBED, LLM, NONE），决定了`get_content()`方法最终返回给模型的内容组合。

### 4.5 在数据摄取管道中的集成
为了实现自动化，元数据提取通常被集成在 IngestionPipeline 中。原始文档加载后，先经过文本分割器（Splitter），紧接着由各种抽取器进行处理，最后将带有丰富元数据的 Node 存入向量库。

### 4.6 高级应用：自动检索（Auto-Retrieval）
通过元数据提取，可以实现更智能的 `VectorIndexAutoRetriever`。该组件能让大模型根据用户的自然语言查询，自动推断出元数据过滤条件（如 catalog == '经济'），结合向量检索实现分层检索，显著提高大文档集知识库下的处理效率。


## 5 文本切分
文本切分（也称数据分割或分块）是将加载后的 `Document` 对象解析并分割成更小粒度的 `Node`（知识块）的过程，这些 `Node` 是后续索引和检索的基本处理单元。

### 5.1 为什么需要文本切分
- **适配大模型限制**：大模型的上下文窗口有限，无法一次性输入整篇长文档。
- **提高检索精确度**：知识块越小，语义通常越精确；而较大的块虽然上下文更完整，但可能引入不相关的噪声。
- **优化成本**：减少输入给大模型的冗余 Token，从而降低计算成本。

### 5.2 核心参数
在文本切分过程中，有两个至关重要的参数：

- `chunk_size`（**块大小**）：限制每个知识块的大小。在 LlamaIndex 中，通常是根据 **Token 数量**（而非字符长度）计算的，默认使用 `tiktoken` 库进行分词。
- `chunk_overlap`（**块重叠**）：允许相邻知识块之间有重叠部分。这是为了保持**语义的连续性**，防止重要的信息在切分点处被截断。

### 5.3 常用的文本分割器（Splitters）与解析器（Parsers）
LlamaIndex 提供了多种开箱即用的组件来处理不同类型的文本：
- **标准分割器**：
  - `SentenceSplitter`：最常用的分割器，基于段落和句子的自然边界进行分割，尽量确保不破坏语义完整性。
  - `TokenTextSplitter`：纯粹基于 Token 数量进行切分，支持指定主分割符和备份分割符。

- **结构化解析器**：
  - 针对特殊格式文档，如 MarkdownNodeParser、HTMLNodeParser、JSONNodeParser 和 CodeSplitter（用于源代码），它们能识别标题、列表或语法结构进行逻辑分割。

- **高级分割器**：
  - ``SemanticSplitterNodeParser``（**语义分割器**）：不依赖固定长度，而是利用嵌入模型计算句子间的语义相似度，在语义发生显著变化的地方进行切分，最大化保证块内语义的相关性。
  - `HierarchicalNodeParser`（**分层解析器**）：在多个粒度（如 128、512、2048 Token）上同时切分，并保留父子关系。这支持“从小块检索扩展到大块生成”的优化策略。

### 5.4 底层切分方法
无论使用哪种分割器，其底层通常依赖以下四种基础方法之一或其组合：

- `split_by_sep`：按指定分割符（如 \n）分割。
- `split_by_regex`：利用正则表达式提取句子，非常适合中文处理。
- `split_by_sentence_tokenizer`：利用自然语言处理库（如 NLTK）进行句子分割（目前对中文支持有限）。
- `split_by_char`：简单的按字符切分（在实际应用中较少单独使用）。

### 5.5 实现与集成
文本分割器既可以独立使用，也可以集成到 IngestionPipeline（数据摄取管道） 中实现自动化处理。
```python
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
```

### 5.6 优化建议：选择合适的块大小
确定最佳的 chunk_size 本质上是在**检索精确性**与**上下文丰富性**之间取得平衡。

- **评估法**：建议使用 ``RetrieverEvaluator`` 或 ``RAGAS`` 等评估框架，针对不同的 ``chunk_size``（如 128、1024、2048）进行对比测试，考察其在忠实度、正确性和相关性上的得分。
- **分离策略**：一种高级优化是“检索块”与“生成块”分离。例如，使用较小的块进行精确检索，但在生成阶段通过 `SentenceWindowNodeParser` 自动扩展到周围的窗口内容，为模型提供更丰富的上下文。


[数据加载示例](../codes/rag-knowledge-engine\app\ingestion\ingestion_demo.py)





