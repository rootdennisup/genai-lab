# RAG 工程实践
- **学习目标**：掌握企业知识库问答系统的完整链路，让 AI 能基于指定资料回答问题，并具备引用来源、无答案拒答和准确率优化能力。

## RAG 技能体系
| 内容                                           | 建议时长 |
| ---------------------------------------------- | -------: |
| RAG 基本原理与架构                             |   8 小时 |
| 文档加载与解析                                 |  10 小时 |
| Chunk 文档切分                                 |  10 小时 |
| Embedding 原理与模型选择                       |  10 小时 |
| 向量数据库 FAISS / Milvus / Qdrant / pgvector  |  14 小时 |
| Vector Search / Keyword Search / Hybrid Search |  12 小时 |
| Metadata Filter / Query Rewrite                |   8 小时 |
| Rerank 重排                                    |   8 小时 |
| 上下文组装与引用来源                           |   8 小时 |
| 幻觉控制与无答案拒答                           |   6 小时 |
| RAG 评估                                       |   6 小时 |


## 学习资料
| 资料                                         | 用途                               |
| -------------------------------------------- | ---------------------------------- |
| 基于大模型的RAG应用开发与优化                | 主教材，建立 RAG 系统框架          |
| all-in-rag                                   | 主教材，建立 RAG 系统框架          |
| LlamaIndex 官方文档                          | 学知识库、索引、检索、query engine |
| 向量库：Qdrant / Milvus / pgvector 官方文档  | 学向量数据库工程化                 |
| 评估体系：RAGAS/TruLens/LangSmith Evaluation | RAG 评估体系                       |

- 《基于大模型的RAG应用开发与优化——构建企业级LLM应用.pdf》
- [all-in-rag](https://datawhalechina.github.io/all-in-rag/)
- [llama_index](https://github.com/run-llama/llama_index)
- [LlamaIndex官方文档](https://developers.llamaindex.ai/python/framework/)
- [langchain](https://github.com/langchain-ai/langchain)
- [LangChain官方文档](https://docs.langchain.com/)
- [ragflow](https://github.com/infiniflow/ragflow)
- 向量库：
  - [qdrant](https://github.com/qdrant/qdrant)
  - [milvus](https://github.com/milvus-io/milvus)
  - [pgvector](https://github.com/pgvector/pgvector)
- 评估体系：
  - [RAGAS 官方文档](https://docs.ragas.io/en/stable)
  - [TruLens 官方文档](https://www.trulens.org/docs/)
  - [LangSmith Evaluation 官方文档](https://docs.langchain.com/langsmith/evaluation)
- [rag 企业级开源项目](https://github.com/nageoffer/ragent)


## 实战项目：rag-knowledge-engine

- 项目目标：搭建一个企业知识库问答系统，支持上传资料、构建索引、检索问答、引用来源和无答案拒答。

### 功能清单
1. 上传 PDF / Word / Excel / Markdown
2. 文档解析
3. Chunk 切分
4. Embedding 向量化
5. 向量索引构建
6. 关键词检索
7. 向量检索
8. Hybrid Search
9. Metadata Filter
10. Rerank
11. 上下文组装
12. 答案生成
13. 引用来源
14. 无答案拒答
15. 用户反馈
16. RAG 评估


## 阶段验收标准
- [☑️] 讲清楚 RAG 全链路
- [☑️] 独立搭建知识库问答系统
- [☑️] 理解 Chunk、Embedding、向量库、Rerank 的作用
- [☑️] 能优化检索准确率
- [☑️] 能通过评估指标定位问题


## 学习资料



- [Python 官方教程](https://docs.python.org/zh-cn/3.14/tutorial/index.html)
- [Python3 菜鸟教程](https://www.runoob.com/python3/python3-tutorial.html)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)
- [Pydantic 官方文档](https://pydantic.com.cn/)
- [Pytest 官方文档](https://pytest.cn/en/stable/)
