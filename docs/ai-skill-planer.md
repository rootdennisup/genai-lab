# 大模型应用开发转型技术体系：学习资料与时长规划版

## 一、总体学习节奏

目标：从资深 Java 后端工程师转型为大模型应用开发工程师。

核心主线：

1. Python + FastAPI + Excel 工具
2. LLM API + Prompt + Function Call
3. RAG 企业知识库
4. LangChain / LangGraph
5. Agent Workflow
6. 大模型应用工程化
7. Transformers / 微调

## 总体时长规划

| 阶段   |                          模块 |   建议时长 |
| ---- | --------------------------: | -----: |
| 第一阶段 |          Python 与 AI 应用开发基础 |  40 小时 |
| 第二阶段 |                  LLM 应用调用基础 |  60 小时 |
| 第三阶段 |                  RAG 检索增强生成 | 100 小时 |
| 第四阶段 | LangChain / LangGraph 工程化框架 |  60 小时 |
| 第五阶段 |        Agent Workflow 智能体系统 |  60 小时 |
| 第六阶段 |                    大模型应用工程化 |  40 小时 |
| 第七阶段 |                     本地模型与微调 | 100 小时 |
| 合计   |                     核心 + 进阶 | 460 小时 |

建议优先完成前六个阶段，也就是 **360 小时核心转型路线**。第七阶段“本地模型与微调”作为进阶选修，不建议一开始投入太多时间。

---

# 第一阶段：Python 与 AI 应用开发基础

## 目标

快速补齐大模型应用开发所需的 Python 工程能力，能够开发脚本、API 服务和简单 AI 工具。

你是资深 Java 工程师，不需要把大量时间花在编程基础上，而应重点掌握 Python 在 AI 应用开发中的常见工程能力。

## 建议时长：40 小时

| 内容                         | 建议时长 |
| -------------------------- | ---: |
| Python 语法与工程结构             | 8 小时 |
| 虚拟环境、依赖管理、配置管理             | 4 小时 |
| pandas / openpyxl 数据处理     | 8 小时 |
| FastAPI 基础                 | 8 小时 |
| Pydantic 数据建模              | 4 小时 |
| pytest、日志、异常处理             | 4 小时 |
| 实战项目：AI Excel Assistant v1 | 4 小时 |

## 推荐学习资料

### 1. Python 官方文档

适合查语法、标准库和工程基础，不建议从头到尾看，遇到问题查即可。

### 2. FastAPI 官方文档

FastAPI 官方教程是最适合后端工程师快速上手 Python API 开发的资料。官方文档强调它基于 Python 类型提示构建 API，并提供循序渐进的 Tutorial。

重点看：

1. First Steps
2. Path Parameters
3. Query Parameters
4. Request Body
5. Response Model
6. Dependency Injection
7. File Upload
8. Background Tasks

### 3. Pydantic 官方文档

Pydantic 是 Python AI 应用里非常常用的数据校验和结构化建模工具，当前官方文档对应 Pydantic v2，并强调其基于 Python 类型提示进行数据验证。

重点看：

1. BaseModel
2. Field
3. Validation
4. Model Config
5. JSON Schema
6. Settings Management

### 4. pandas / openpyxl 文档

用于 Excel、CSV 和结构化数据处理。这个阶段不需要深入数据分析，只需要掌握电商运营表格处理能力。

## 实战项目：AI Excel Assistant v1

### 项目目标

先不接入大模型，做一个普通 Excel 批处理工具。

### 功能清单

1. 上传 Excel
2. 读取 Sheet
3. 读取表头
4. 按字段过滤数据
5. 批量清洗空值
6. 生成新列
7. 导出处理后的 Excel
8. 提供 FastAPI 接口

### 阶段验收标准

完成后你应该能做到：

1. 独立搭建 Python 项目结构
2. 使用 FastAPI 提供接口
3. 使用 pandas / openpyxl 处理 Excel
4. 使用 Pydantic 定义请求和响应模型
5. 使用 pytest 写简单测试

---

# 第二阶段：LLM 应用调用基础

## 目标

学会把大模型接入应用，掌握 Prompt、结构化输出、多轮对话、Function Call 和 Tool Calling。

这个阶段重点不是深入 Transformer 数学原理，而是掌握大模型应用开发的调用机制和工程控制能力。

## 建议时长：60 小时

| 内容                              |  建议时长 |
| ------------------------------- | ----: |
| LLM 基础机制：Token、上下文、参数           |  8 小时 |
| OpenAI / Qwen / DeepSeek API 调用 | 10 小时 |
| Prompt Engineering              | 10 小时 |
| 结构化输出 JSON Schema               |  8 小时 |
| Function Call / Tool Calling    | 10 小时 |
| 多轮对话与上下文管理                      |  6 小时 |
| 错误处理、重试、限流、成本统计                 |  4 小时 |
| 实战项目                            |  4 小时 |

## 推荐学习资料

### 1. OpenAI API 官方文档

重点学习模型调用、结构化输出、工具调用和 Prompt 设计。OpenAI 官方文档将 tool calling 描述为“应用给模型提供工具、模型发起工具调用、应用侧执行工具、再把工具结果回填给模型”的多步流程，非常适合理解 Function Call 的真实工程链路。

重点看：

1. Responses API
2. Prompting
3. Structured Outputs
4. Function Calling / Tool Calling
5. Streaming
6. Error Handling

### 2. OpenAI Cookbook

OpenAI Cookbook 提供大量 API 使用示例，适合边看边改代码。官方说明它包含使用 OpenAI API 完成常见任务的示例代码和指南。

重点看：

1. Function Calling Examples
2. Structured Outputs Examples
3. RAG Examples
4. Embeddings Examples
5. Evaluation Examples

### 3. OpenAI Prompting / Prompt Engineering Guide

OpenAI 官方 Prompt 文档适合建立 Prompt 基础方法论，官方文档也强调 Prompting 既有技巧性，也需要持续实验和迭代。

重点掌握：

1. 明确任务目标
2. 给出上下文
3. 指定输出格式
4. 提供示例
5. 加入约束条件
6. 拆解复杂任务

### 4. DeepLearning.AI 相关短课

可以选择学习：

1. ChatGPT Prompt Engineering for Developers
2. Building Systems with the ChatGPT API
3. Functions, Tools and Agents with LangChain

DeepLearning.AI 的 LangChain 应用开发短课由 Andrew Ng 和 LangChain 创建者 Harrison Chase 参与授课，课程定位是帮助开发者用语言模型构建应用。

## 实战项目

### 项目一：AI Weather Assistant

目标：用户自然语言问天气，模型自动判断是否调用天气工具。

练习点：

1. Function Call
2. 参数抽取
3. 工具执行
4. 工具结果回填
5. 异常处理

### 项目二：AI Excel Assistant v2

目标：让 AI 根据自然语言操作 Excel。

示例指令：

1. “帮我统计每个 SKU 的库存”
2. “找出价格为空的行”
3. “把标题控制在 75 个字符以内”
4. “生成一列英文产品描述”

练习点：

1. 自然语言转结构化任务
2. LLM 调用工具
3. JSON 输出控制
4. Excel 操作函数封装

### 阶段验收标准

完成后你应该能做到：

1. 独立调用大模型 API
2. 控制模型输出 JSON
3. 设计 Function Call Schema
4. 处理工具调用失败
5. 构建一个简单 AI 工具型应用

---

# 第三阶段：RAG 检索增强生成

## 目标

掌握企业知识库问答系统的完整链路，让 AI 能基于指定资料回答问题，并具备引用来源、无答案拒答和准确率优化能力。

RAG 是你转型路线里最重要的核心模块。

## 建议时长：100 小时

| 内容                                             |  建议时长 |
| ---------------------------------------------- | ----: |
| RAG 基本原理与架构                                    |  8 小时 |
| 文档加载与解析                                        | 10 小时 |
| Chunk 文档切分                                     | 10 小时 |
| Embedding 原理与模型选择                              | 10 小时 |
| 向量数据库 FAISS / Milvus / Qdrant / pgvector       | 14 小时 |
| Vector Search / Keyword Search / Hybrid Search | 12 小时 |
| Metadata Filter / Query Rewrite                |  8 小时 |
| Rerank 重排                                      |  8 小时 |
| 上下文组装与引用来源                                     |  8 小时 |
| 幻觉控制与无答案拒答                                     |  6 小时 |
| RAG 评估                                         |  6 小时 |

## 推荐学习资料

### 1. LlamaIndex RAG 官方文档

LlamaIndex 官方文档对 RAG 的解释很适合入门：LLM 没有训练在你的私有数据上，而 RAG 的作用就是把你的数据添加到模型可访问的上下文中。

重点看：

1. Introduction to RAG
2. Documents / Nodes
3. Indexing
4. Query Engine
5. Retriever
6. Response Synthesis
7. Advanced RAG

### 2. LlamaIndex Question Answering 文档

LlamaIndex 官方文档说明，RAG 是让 LLM 基于不同规模、不同类型数据完成问答的主要框架，并提供从简单到高级的 RAG 技术。

重点看：

1. Simple RAG
2. Advanced Retrieval
3. Query Engines
4. Chat Engines
5. Custom Retrieval

### 3. LangChain RAG 相关文档

适合学习 LangChain 体系下的 Document Loader、Text Splitter、VectorStore、Retriever 和 Retrieval Chain。

### 4. 向量数据库官方文档

建议按这个顺序学习：

1. FAISS：适合本地实验和理解向量索引
2. Qdrant：适合轻量生产级向量数据库
3. Milvus：适合大规模向量检索系统
4. pgvector：适合已有 PostgreSQL 技术栈的团队

Milvus 官方文档定位为帮助开发者安装、使用和部署 Milvus 来构建应用；Qdrant 官方定位是开源向量搜索引擎，提供快速、可扩展的向量相似度搜索服务。

### 5. RAGAS / TruLens / LangSmith Evaluation

RAG 不能只靠“感觉效果不错”，必须建立评估体系。Ragas 官方定位是帮助 AI 应用从“主观感觉检查”走向系统化评估循环；TruLens 提供 RAG Triad，即 context relevance、groundedness、answer relevance 三类评估。

LangSmith Evaluation 官方文档强调，评估可以覆盖从部署前测试到生产监控的整个应用生命周期。

### 6. DeepLearning.AI Building and Evaluating Advanced RAG

这门短课适合补充高级 RAG 和评估方法。课程页面显示其内容包含高级检索方法、评估和实验跟踪等主题。

## 实战项目：Enterprise Knowledge Base QA

### 项目目标

搭建一个企业知识库问答系统，支持上传资料、构建索引、检索问答、引用来源和无答案拒答。

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

### 阶段验收标准

完成后你应该能做到：

1. 讲清楚 RAG 全链路
2. 独立搭建知识库问答系统
3. 理解 Chunk、Embedding、向量库、Rerank 的作用
4. 能优化检索准确率
5. 能通过评估指标定位问题

---

# 第四阶段：LangChain / LangGraph 工程化框架

## 目标

学会使用框架快速组合 AI 应用，从“会写调用代码”升级为“能搭建 AI 工作流”。

注意：LangChain 是工具，不是核心能力。核心仍然是 LLM、RAG、Tool Calling、Agent 和工程化设计。

## 建议时长：60 小时

| 内容                               |  建议时长 |
| -------------------------------- | ----: |
| LangChain 基础组件                   | 10 小时 |
| LCEL / Runnable                  |  8 小时 |
| OutputParser / Structured Output |  6 小时 |
| Retriever / RAG Chain            | 10 小时 |
| Tool Calling 集成                  |  8 小时 |
| Memory 机制                        |  6 小时 |
| LangGraph 基础                     |  8 小时 |
| 实战项目                             |  4 小时 |

## 推荐学习资料

### 1. LangChain 官方文档

LangChain 官方文档当前将 LangChain、LangGraph、Deep Agents 和 LangSmith 作为 Agent Engineering 体系的一部分，适合系统学习框架生态。

重点看：

1. Models
2. Prompts
3. Output Parsers
4. LCEL
5. Retrievers
6. Tools
7. Agents

### 2. LangGraph 官方文档

LangGraph 官方文档将其定位为用于构建、管理和部署长时间运行、有状态 Agent 的低层编排框架，适合学习 Agent 状态管理和流程编排。

重点看：

1. State
2. Nodes
3. Edges
4. Conditional Edges
5. Checkpoints
6. Interrupts
7. Human-in-the-loop

### 3. DeepLearning.AI LangChain for LLM Application Development

适合快速建立 LangChain 应用开发感觉，不建议停留太久。课程时间短，更适合作为入门导览。

### 4. LangSmith 文档

用于学习 Trace、Debug、Evaluation 和生产监控。

## 实战项目：AI Research Assistant

### 项目目标

开发一个 AI 研究助手，支持上传多篇文档，自动总结、对比、问答，并提供引用来源。

### 功能清单

1. 上传多篇 PDF
2. 自动总结每篇文档
3. 提取关键观点
4. 生成对比表格
5. 基于文档问答
6. 引用来源
7. 多步骤任务编排
8. 输出结构化结果

### 阶段验收标准

完成后你应该能做到：

1. 使用 LangChain 组合 RAG 应用
2. 使用 LCEL 组织链路
3. 使用 LangGraph 设计有状态流程
4. 理解 Node、Edge、State、Checkpoint
5. 能调试框架执行过程

---

# 第五阶段：Agent Workflow 智能体系统

## 目标

让 AI 从“回答问题”升级为“能规划任务、调用工具、执行流程、检查结果、完成人机协作”的智能体系统。

真正重要的不是 Agent 概念，而是底层能力：

1. Planning
2. Tool Use
3. State Management
4. Reflection
5. Human-in-the-loop
6. Workflow Orchestration
7. Failure Recovery

## 建议时长：60 小时

| 内容                       |  建议时长 |
| ------------------------ | ----: |
| Agent 基本结构               |  6 小时 |
| ReAct / Plan-and-Execute |  8 小时 |
| Tool Use 工具调用            | 10 小时 |
| Reflection 与结果校验         |  6 小时 |
| LangGraph Agent 编排       | 12 小时 |
| Human-in-the-loop        |  6 小时 |
| Multi-Agent 基础           |  6 小时 |
| 实战项目                     |  6 小时 |

## 推荐学习资料

### 1. LangGraph 官方文档

Agent Workflow 最推荐用 LangGraph 学，因为它强调状态、节点、边、检查点和长流程编排。LangGraph 官方文档明确表示它是面向长运行、有状态 Agent 的低层编排框架。

重点看：

1. Build a Basic Chatbot
2. Add Tools
3. Add Memory
4. Add Human-in-the-loop
5. Add Persistence
6. Multi-Agent

### 2. OpenAI Function Calling / Tool Calling 文档

Agent 的底层能力之一就是工具调用。OpenAI 官方 Function Calling 文档给出了工具调用的完整流程：模型选择工具、应用执行工具、工具结果再回填给模型。

### 3. OpenAI Structured Outputs 文档

Structured Outputs 对 Agent 非常重要，因为工具调用、状态流转和执行结果都需要结构化输出。OpenAI 官方文档说明结构化输出可以通过 function calling 或 json_schema response format 实现。

### 4. LangSmith / TruLens

Agent 必须可观测，否则很难调试。LangSmith 适合 Trace 和 Evaluation；TruLens 可用于评估 Agent 和 RAG 工作流。

## 实战项目：Takealot Seller Operations Agent

### 项目目标

结合你的真实业务，开发一个 takealot 卖家运营 Agent，帮助完成商品资料处理、标题生成、文案生成、客服邮件生成等任务。

### 输入

1. SKU 表格
2. 产品中文名称
3. 产品卖点
4. 产品规格
5. 平台标题规则
6. 平台文案风格
7. 客服邮件背景

### 工作流

1. 读取 SKU 表格
2. 分析产品信息
3. 生成核心关键词
4. 生成主标题
5. 生成副标题
6. 检查标题字符数
7. 检查关键词重复
8. 生成产品描述
9. 生成客服邮件
10. 等待人工确认
11. 导出 Excel 或 Markdown

### 阶段验收标准

完成后你应该能做到：

1. 设计 Agent 状态机
2. 设计 Tool Schema
3. 设计 Human Approval 节点
4. 设计失败重试和回退逻辑
5. 用 LangGraph 实现一个真实业务 Agent

---

# 第六阶段：大模型应用工程化

## 目标

把 AI Demo 变成稳定、可维护、可观测、可部署的真实系统。

这部分是你作为资深 Java 工程师的优势区。很多人会调 API，但不一定能做成稳定系统。

## 建议时长：40 小时

| 内容                        | 建议时长 |
| ------------------------- | ---: |
| FastAPI 服务化               | 6 小时 |
| PostgreSQL / Redis / 对象存储 | 6 小时 |
| Celery / 异步任务队列           | 6 小时 |
| Prompt 版本管理               | 4 小时 |
| 模型路由与降级                   | 4 小时 |
| Token 成本统计                | 4 小时 |
| 日志、Trace、监控               | 4 小时 |
| Docker 部署                 | 6 小时 |

## 推荐学习资料

### 1. FastAPI 官方文档

继续深入学习依赖注入、后台任务、文件上传、WebSocket、异常处理和部署相关内容。FastAPI 官方文档强调其基于标准 Python 类型提示构建，适合高性能 API 开发。

### 2. Docker 官方文档

重点掌握 Dockerfile、Docker Compose、环境变量、日志挂载和服务部署。

### 3. PostgreSQL / Redis 官方文档

重点不是数据库基础，而是 AI 应用中的存储设计：

1. 会话记录
2. 用户反馈
3. Prompt 版本
4. 调用日志
5. Token 成本
6. 任务状态

### 4. LangSmith Evaluation / Observability

LangSmith 官方文档说明 Evaluation 可以用于离线评估、实验对比和生产质量监控。

### 5. Ragas / TruLens

用于建立 RAG 和 Agent 的评估闭环。Ragas 强调系统化评估循环，TruLens 强调对 retrieved context、tool calls、plans 等 Agent 执行流程的评估。

## 实战项目：AI Application Platform Mini

### 项目目标

开发一个简化版 AI 应用平台，支持模型调用、RAG、Agent、Prompt 管理、调用日志和用户反馈。

### 功能清单

1. 用户上传文档
2. 创建知识库
3. 配置 Prompt
4. 调用模型
5. 查看调用日志
6. 查看 Token 成本
7. 查看检索结果
8. 提交用户反馈
9. 支持模型切换
10. 支持 Docker 部署

### 阶段验收标准

完成后你应该能做到：

1. 将 AI 应用服务化
2. 设计 AI 应用后端架构
3. 处理成本、性能、稳定性问题
4. 建立日志、Trace、反馈闭环
5. 用 Docker 部署完整应用

---

# 第七阶段：本地模型与微调

## 目标

作为进阶选修模块，了解本地模型调用、推理加速和 LoRA 微调，具备参与企业私有化模型项目的基础。

这个阶段不要过早投入。对大模型应用开发来说，优先级应该排在 LLM 调用、RAG、Agent、工程化之后。

## 建议时长：100 小时

| 内容                             |  建议时长 |
| ------------------------------ | ----: |
| Transformers 基础                | 12 小时 |
| Tokenizer / Model / Pipeline   |  8 小时 |
| 本地模型调用：Qwen / Llama / DeepSeek | 12 小时 |
| Ollama / llama.cpp             | 10 小时 |
| vLLM 推理服务                      | 10 小时 |
| LoRA / QLoRA 原理                | 12 小时 |
| SFT 数据集构造                      | 10 小时 |
| 微调训练脚本                         | 12 小时 |
| 模型评估                           |  6 小时 |
| 部署与 API 封装                     |  8 小时 |

## 推荐学习资料

### 1. Hugging Face Transformers 官方文档

Hugging Face Transformers 官方文档说明，其生态中有超过 100 万个 Transformers 模型 checkpoint 可用，非常适合作为本地模型调用和微调入门资料。

重点看：

1. Pipeline
2. AutoTokenizer
3. AutoModelForCausalLM
4. Text Generation
5. Training
6. PEFT
7. Quantization

### 2. Hugging Face Course

适合系统学习 Transformers、Tokenizer、Datasets、Trainer。

### 3. PEFT 官方文档

重点学习 LoRA / QLoRA。

### 4. TRL 官方文档

重点学习 SFTTrainer、DPO 等训练方式。

### 5. Ollama 官方文档

适合本地快速运行模型。

### 6. vLLM 官方文档

适合学习推理服务化和高性能部署。

## 实战项目：客服语气改写模型微调

### 项目目标

微调一个客服语气改写模型，把普通回复改写成专业、礼貌、适合跨境电商平台沟通的英文客服邮件。

### 为什么选这个项目

“让模型只回答业务范围内的问题”通常不适合靠微调解决，更适合通过 RAG、Prompt、权限控制和拒答策略解决。

微调更适合解决：

1. 语气风格
2. 输出格式
3. 固定任务模式
4. 领域表达习惯

### 功能清单

1. 准备客服邮件样本
2. 构造 instruction 数据集
3. 使用 LoRA 微调
4. 对比微调前后效果
5. 部署为 API
6. 接入客服邮件生成工具

### 阶段验收标准

完成后你应该能做到：

1. 理解本地模型加载
2. 理解 Tokenizer
3. 理解 LoRA 微调流程
4. 能构造简单 SFT 数据集
5. 能判断什么时候用 RAG，什么时候用微调

---

# 八、推荐学习排期

## 方案一：3 个月快速转型版

适合每天投入 4 小时左右。

总投入：约 360 小时。

| 月份     | 重点                                          |   学习时长 |
| ------ | ------------------------------------------- | -----: |
| 第 1 个月 | Python、FastAPI、LLM API、Prompt、Function Call | 100 小时 |
| 第 2 个月 | RAG、Embedding、向量库、Hybrid Search、Rerank      | 120 小时 |
| 第 3 个月 | LangChain、LangGraph、Agent、工程化落地             | 140 小时 |

3 个月内不建议重点做微调。

---

## 方案二：6 个月稳扎稳打版

适合每天投入 2.5 小时左右。

总投入：约 460 小时。

| 月份     | 重点                                 |  学习时长 |
| ------ | ---------------------------------- | ----: |
| 第 1 个月 | Python、FastAPI、Excel 工具            | 50 小时 |
| 第 2 个月 | LLM API、Prompt、Function Call       | 70 小时 |
| 第 3 个月 | RAG 基础、文档解析、Chunk、Embedding        | 80 小时 |
| 第 4 个月 | 向量库、Hybrid Search、Rerank、RAG 评估    | 80 小时 |
| 第 5 个月 | LangChain、LangGraph、Agent Workflow | 90 小时 |
| 第 6 个月 | 工程化、本地模型、微调入门                      | 90 小时 |

---

# 九、推荐资料优先级

## 第一优先级：必须学

1. FastAPI 官方文档
2. Pydantic 官方文档
3. OpenAI API 官方文档
4. OpenAI Cookbook
5. LlamaIndex RAG 官方文档
6. LangChain 官方文档
7. LangGraph 官方文档
8. Ragas / TruLens / LangSmith Evaluation

## 第二优先级：建议学

1. DeepLearning.AI Prompt Engineering
2. DeepLearning.AI Building Systems with ChatGPT API
3. DeepLearning.AI LangChain for LLM Application Development
4. DeepLearning.AI Building and Evaluating Advanced RAG
5. Hugging Face Course
6. Hugging Face Transformers 文档

## 第三优先级：进阶选修

1. PEFT
2. TRL
3. vLLM
4. Ollama
5. llama.cpp
6. Milvus 深度部署
7. 多 Agent 协作框架

---

# 十、最终推荐路线

## 核心 360 小时路线

| 顺序 | 模块                    |     时长 |
| -- | --------------------- | -----: |
| 1  | Python 与 AI 应用开发基础    |  40 小时 |
| 2  | LLM 应用调用基础            |  60 小时 |
| 3  | RAG 检索增强生成            | 100 小时 |
| 4  | LangChain / LangGraph |  60 小时 |
| 5  | Agent Workflow        |  60 小时 |
| 6  | 大模型应用工程化              |  40 小时 |

完成这 360 小时后，你就应该具备大模型应用开发工程师的核心能力。

## 进阶 100 小时路线

| 顺序 | 模块      |     时长 |
| -- | ------- | -----: |
| 7  | 本地模型与微调 | 100 小时 |

这部分用于增强你对模型侧的理解，不作为第一阶段转型重点。

---

# 十一、最终能力画像

完成这套路线后，你的能力画像应该是：

1. Java 后端工程能力
2. Python AI 应用开发能力
3. FastAPI 服务化能力
4. LLM API 调用能力
5. Prompt Engineering 能力
6. Function Call / Tool Calling 能力
7. RAG 知识库系统能力
8. LangChain / LangGraph 编排能力
9. Agent Workflow 设计能力
10. 大模型应用工程化能力
11. 基础本地模型与微调理解能力

最终定位：

大模型应用开发工程师，不是纯算法工程师。

更准确的岗位方向：

1. AI Application Engineer
2. LLM Application Engineer
3. RAG Engineer
4. AI Agent Engineer
5. AI Backend Engineer

一句话总结：

这条路线的核心不是把所有 AI 概念都学一遍，而是围绕真实项目，把 LLM、RAG、Tool Calling、Agent Workflow 和后端工程化能力串起来，形成可落地的大模型应用开发能力。
