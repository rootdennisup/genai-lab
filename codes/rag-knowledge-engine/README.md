# RAG Knowledge Engine

这是一个面向 RAG 学习的企业知识库问答 MVP。它遵循 `docs/technical-architecture.md` 的模块化单体设计，使用一个 FastAPI 进程同时提供页面与 API。

## 当前可学习的完整链路

1. 上传 PDF、DOCX、XLSX 或 Markdown；服务端校验扩展名、大小并用随机文件名落盘。
2. 各格式 Parser 输出统一结构块，保留页码、章节、段落或工作表行号。
3. 结构优先切块并生成稳定 Chunk ID，重复构建保持幂等。
4. 同时执行本地 BM25 和哈希向量检索，再使用 RRF 融合和轻量 Rerank。
5. 在证据阈值通过后抽取原文作答，并映射结构化引用；证据不足则拒答。
6. 使用 `query_id` 保存召回、排序、上下文、延迟和答案轨迹，并支持分类反馈。

本地哈希向量与抽取式生成是可离线运行的教学适配器，不等同于生产级语义 Embedding 和 LLM。它们让你先看懂数据链路；后续可在保持领域层不变的前提下接入 OpenAI-compatible 服务。

## 启动

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn app.main:app --reload
```

打开 <http://127.0.0.1:8000> 使用工作台，或打开 <http://127.0.0.1:8000/docs> 调试 API。

## 测试

```powershell
pytest -q
```

查询时设置 `options.include_debug=true`，可以观察每个 Chunk 的 `keyword_score`、`vector_score`、`fusion_score` 和 `rerank_score`，这也是调试 RAG 召回问题的起点。

## 目录边界

- `app/ingestion`：文档格式解析与 Chunk。
- `app/retrieval`：BM25、向量、RRF 与重排。
- `app/application`：上传索引和问答用例编排。
- `app/infrastructure`：SQLite 等可替换适配器。
- `app/api`：HTTP 协议与输入校验。
- `static`：无构建步骤的原生单页工作台。

## LlamaIndex Reader 学习参考

项目保留了两套互不影响的解析实现：

- `app/ingestion/parsers.py`：直接使用 pypdf、python-docx、openpyxl，便于理解格式解析细节。
- `app/ingestion/parsers_llama.py`：使用 LlamaIndex Reader，再通过防腐层映射为项目的 `ParsedBlock`。

安装并单独调用参考实现：

```powershell
pip install -e ".[llama]"
```

```python
from pathlib import Path
from app.ingestion.parsers_llama import parse_document

blocks = parse_document(Path("data/example.pdf"), "pdf")
```

参考实现没有替换线上摄取链路，方便对照两种方案的结构保真度、来源定位能力和依赖成本。
