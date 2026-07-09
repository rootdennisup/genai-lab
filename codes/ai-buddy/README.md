# AI-BUDDY

## 1 项目简介
AI-BUDDY 是一个基于 Python + FastAPI 的 AI 陪伴类应用 MVP，核心目标不是单纯做聊天接口，而是用这个项目系统实践 LLM 应用工程能力，包括：
- LLM Runtime：统一封装模型调用，支持流式、重试、限流、多模型适配
- Conversation：管理当前会话、历史消息、上下文窗口、长对话摘要
- Prompt Engine：管理系统提示词、角色设定、Prompt 模板和版本
- Memory：构建长期记忆，覆盖用户事实、偏好、行为和历史事件
- Recommend：实现主动陪伴能力，比如话题推荐、情绪陪伴、兴趣推荐
- Tools：为后续 Agent 能力接入天气、搜索、日历、数据库查询、MCP 等工具
- Infra：隔离数据库、Redis、向量库、文件存储等基础设施


- **核心流程**：
    ```text
    User
    |
    v
    Conversation
    |
    v
    Context Assembly
    |
    +------------+
    |            |
    Memory       Tools
    |
    Prompt Engine
    |
    LLM Runtime
    |
    Response
    ```

- **项目实践主线**：
  - 先把 LLM Runtime 做成稳定边界，避免业务层直接依赖具体模型厂商。
  - 再建设 Conversation + Prompt Engine，形成最小可用聊天闭环。
  - 然后引入 Memory，让陪伴从“单轮问答”进入“长期关系”。
  - 最后逐步扩展 Recommend / Tools / Agent Workflow / MCP，增强主动性和行动能力。


## 2. 项目目录结构
```text
ai-buddy/
├── app/
│   ├── common/
│   ├── conversation/
│   ├── prompt_engine/
│   ├── memory/
│   ├── recommend/
│   ├── tools/
│   ├── llm_runtime/
│   └── infra/
├── tests/
├── docs/
├── scripts/
├── pyproject.toml
├── uv.lock
└── README.md
```
模块说明如下。

### 2.1 common
- 职责：存放项目公共能力。包括：
  - 通用异常
  - 通用类型
  - 常量
  - 工具函数

- 目录：
    ```
    common/
    ├── __init__.py
    ├── constants.py    -- 项目常量
    ├── exceptions.py   -- 统一异常
    ├── enums.py        -- 枚举  
    └── utils.py        -- 通用工具
    ```

### 2.2 conversation
- 职责：负责用户对话**上下文管理**。包含：
  - 当前会话
  - 历史消息
  - Context Window
  - 对话摘要

- 目录：
    ```
    conversation/
    ├── __init__.py
    ├── models.py       -- 定义消息模型
    ├── service.py      -- 核心业务
    ├── context.py      -- 上下文处理：上下文拼接|Token控制|历史裁剪
    ├── summary.py      -- 长对话摘要
    └── repository.py
    ```

### 2.3 prompt_engine
- 职责:Prompt 工程管理。负责：
  - System Prompt
  - Role Prompt
  - Prompt Template
  - Prompt Version

- 目录：
    ```
    prompt_engine/
    ├── __init__.py
    ├── templates/
    │   ├── companion.yaml
    │   └── system.yaml
    ├── builder.py          -- 负责动态构建 Prompt
    ├── variables.py
    └── version.py
    ```

### 2.4 memory
- 职责：长期记忆系统。负责：
  - 用户事实
  - 用户偏好
  - 用户行为
  - 历史事件

- 目录：
    ```
    memory/
    ├── __init__.py
    ├── models.py
    ├── extractor.py        -- 从聊天中抽取记忆
    ├── service.py
    ├── retriever.py        -- 查询相关 Memory
    └── repository.py
    ```

### 2.5 recommend
- 职责：AI 主动推荐能力。例如：
  - 推荐聊天主题
  - 情绪陪伴
  - 兴趣推荐

- 目录：
    ```
    recommend/
    ├── __init__.py
    ├── models.py
    ├── service.py
    └── strategy.py     -- 推荐策略
    ```

### 2.6 tools
- 职责：Agent 外部工具能力。例如：
  - 天气
  - 搜索
  - 日历
  - 查询数据库

- 目录：
    ```
    tools/
    ├── __init__.py
    ├── base.py         -- 定义工具接口
    ├── weather.py
    ├── search.py
    └── registry.py     -- 工具注册

    未来扩展 MCP Server
    ```
### 2.7 llm_runtime
- 职责：LLM 调用抽象层。用来屏蔽：
  - OpenAI
  - Claude
  - Gemini
  - Qwen

- 目录：
    ```
    llm_runtime/
    ├── __init__.py
    ├── client.py       -- 统一接口
    ├── models.py
    ├── streaming.py    -- 流式处理
    ├── retry.py        -- 超时/重试/限流
    └── token.py
    ```

## 2.8 infra
- 职责:外部技术依赖。例如：
  - 数据库
  - Redis
  - Vector DB
  - 文件存储

- 目录：
    ```
    infra/
    ├── __init__.py
    ├── database/
    │   ├── postgres.py
    │   └── redis.py
    ├── vector_db/
    │   ├── chroma.py
    │   └── embedding.py
    ├── storage/
    │   └── file_storage.py
    └── config/
        └── settings.py
    ```

## 3 模块调用关系
```
API
 |
 v
Conversation Service
 |
 +----------------+
 |                |
 v                v
Memory        Prompt Engine
 |
 v
LLM Runtime
 |
 v
Response
```

## 4 MVP 开发顺序

### Phase 1：LLM Runtime
实现：
- API调用
- Streaming
- Retry

### Phase 2：Conversation
实现：
- Chat API
- 历史上下文

### Phase 3：Prompt Engine
实现：
- System Prompt
- Persona

### Phase 4：Memory
实现：
- Memory Extract
- Memory Retrieve

### Phase 5：recommend
实现：
- 主动推荐

### Phase 6：Tools
实现：
- Function Calling
- MCP

## 5 设计原则

- **原则1：业务能力模块化**。
  - 例如：memory、conversation、tools

- **原则2：LLM调用统一入口**。
  - 禁止：业务代码直接调用OpenAI SDK
  - 必须：业务-->llm_runtime-->OpenAI

- **原则3：基础设施隔离**。
  - 业务不关心：Redis、Vector DB、Vector DB

- **原则4：为 Agent 演进设计**。
    
    未来扩展：
    ```
    agent/
    workflow/
    planner/
    executor/
    mcp/
    ```
