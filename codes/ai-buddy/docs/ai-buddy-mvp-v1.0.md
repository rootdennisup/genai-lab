# AI-BUDDY MVP v1.0 设计文档

## 1. 版本定位

AI-BUDDY MVP v1.0 是项目的第一个阶段性版本，目标是打通 AI 陪伴应用的最小聊天闭环：

```text
用户请求
  |
  v
Chat API
  |
  v
Prompt Engine
  |
  v
LLM Runtime
  |
  v
大模型 API / Mock Runtime
  |
  v
AI 回复
```

本版本重点验证三件事：

1. 大模型 API 调用链路是否可用。
2. Prompt 工程是否从业务代码中独立出来。
3. 聊天 API 是否具备承接多轮对话的基础请求/响应结构。

v1.0 不是完整 AI 陪伴系统，也不追求一次性实现 Memory、RAG、Tool Calling、Agent Workflow 等高级能力。它的价值在于先建立稳定、清晰、可演进的基础架构。

## 2. 当前代码现状

当前项目已经具备以下代码模块：

```text
app/
├── main.py
├── api/
│   └── chat.py
├── conversation/
│   └── models.py
├── prompt_engine/
│   └── builder.py
├── llm_runtime/
│   ├── client.py
│   └── models.py
└── infra/
    └── config.py
```

各模块当前职责如下：

| 模块 | 当前职责 |
| --- | --- |
| `app.main` | FastAPI 应用入口，注册路由，提供健康检查接口 |
| `app.api.chat` | 提供 `/api/chat` 聊天接口，编排 Prompt 构建和 LLM 调用 |
| `app.conversation.models` | 定义聊天请求和响应模型 |
| `app.prompt_engine.builder` | 构建 system/user messages，承载基础陪伴型系统提示词 |
| `app.llm_runtime.client` | 统一大模型调用入口，支持 `mock` 和 `qwen` 两种模式 |
| `app.llm_runtime.models` | 定义 LLM message/request/response 数据结构 |
| `app.infra.config` | 管理应用配置和 Qwen 模型供应商配置 |

## 3. v1.0 范围

### 3.1 本版本实现

v1.0 聚焦以下能力：

- FastAPI 应用启动。
- 健康检查接口：`GET /health`。
- 聊天接口：`POST /api/chat`。
- 基础请求模型：`user_id`、`chat_id`、`message`、`persona`。
- 基础响应模型：`chat_id`、`reply`、`model`。
- Prompt Builder：构建 AI-Buddy 基础 system prompt。
- Persona 注入：支持通过请求参数追加角色补充设定。
- LLM Runtime 统一入口：业务层不直接调用模型厂商 SDK 或 HTTP API。
- Mock 模式：不依赖真实模型即可跑通本地聊天链路。
- Qwen 模式：通过 OpenAI-compatible `/chat/completions` 格式调用百炼 Qwen。
- `.env` 配置加载：区分应用配置和模型供应商配置。

### 3.2 本版本暂不实现

以下能力不纳入 v1.0：

- 对话历史持久化。
- 真正的多轮上下文拼接。
- 长对话摘要。
- 长期记忆 Memory。
- RAG 和向量检索。
- Tool Calling。
- MCP Server。
- 用户鉴权。
- 内容安全审核链路。
- 模型调用重试、限流、熔断。
- 流式响应。

这些能力将在后续版本中基于当前模块边界逐步扩展。

## 4. 架构设计

### 4.1 分层结构

v1.0 采用轻量分层架构：

```text
API Layer
  app.api.chat

Application / Orchestration Layer
  chat endpoint 内部编排

Domain Model Layer
  app.conversation.models
  app.llm_runtime.models

Prompt Layer
  app.prompt_engine.builder

LLM Runtime Layer
  app.llm_runtime.client

Infra Config Layer
  app.infra.config
```

当前阶段没有单独抽出 `conversation.service`，因为业务编排还很薄，`app.api.chat` 中直接串联 `PromptBuilder` 和 `LLMClient` 可以降低复杂度。等对话历史、上下文窗口、摘要和记忆召回进入后，再将编排逻辑下沉到 `ConversationService`。

### 4.2 请求链路

`POST /api/chat` 的处理流程如下：

```text
1. 接收 ChatRequest
2. 如果 request.chat_id 为空，则生成新的 chat_id
3. PromptBuilder 根据 user message 和 persona 构建 LLM messages
4. LLMClient 根据 settings.llm_mode 选择 mock 或 qwen
5. LLMClient 返回 LLMResponse
6. API 组装 ChatResponse 并返回
```

对应当前代码链路：

```text
app.api.chat.chat
  -> PromptBuilder.build_chat_messages
  -> LLMClient.chat
  -> LLMClient._mock_chat / LLMClient._qwen_chat
  -> ChatResponse
```

## 5. 模块设计

### 5.1 API 模块

文件：

```text
app/api/chat.py
```

当前接口：

```text
POST /api/chat
```

职责：

- 接收外部聊天请求。
- 生成或透传 `chat_id`。
- 调用 Prompt Engine 构建 messages。
- 调用 LLM Runtime 获取模型回复。
- 返回统一响应结构。

当前实现选择在模块级直接实例化：

```python
prompt_builder = PromptBuilder()
llm_client = LLMClient()
```

这是 MVP 阶段可以接受的简化。后续如果服务对象变多，建议升级为 FastAPI 依赖注入：

```text
get_prompt_builder()
get_llm_client()
get_conversation_service()
```

### 5.2 Conversation 模块

文件：

```text
app/conversation/models.py
```

当前只包含 API 请求/响应模型：

```text
ChatRequest
ChatResponse
```

`ChatRequest` 字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `user_id` | `str` | 用户 ID，当前默认值为 `user_id_001` |
| `chat_id` | `str | None` | 对话 ID，不传则由服务端生成 |
| `message` | `str` | 用户输入，不能为空 |
| `persona` | `str | None` | 可选角色补充设定 |

`ChatResponse` 字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `chat_id` | `str` | 对话 ID |
| `reply` | `str` | AI 回复内容 |
| `model` | `str` | 实际使用的模型 |

当前 `chat_id` 已进入接口结构，但尚未用于读取历史消息。这个设计为后续多轮对话保留了入口。

### 5.3 Prompt Engine 模块

文件：

```text
app/prompt_engine/builder.py
```

当前核心类：

```text
PromptBuilder
```

核心方法：

```text
build_chat_messages(user_message, persona)
```

输出结构：

```text
[
  {"role": "system", "content": "..."},
  {"role": "user", "content": "..."}
]
```

当前 system prompt 明确了 AI-Buddy 的基础定位：

- 面向长期陪伴场景的 AI 伙伴。
- 不只回答问题，也帮助用户梳理想法、获得情绪支持、学习和项目练习。
- 使用自然、温和、清晰的中文。
- 不假装拥有真实经历。
- 不编造用户未提供的个人信息。
- 用户表达情绪时先共情再建议。
- 用户学习编程时像耐心的开发指导老师一样解释。

`persona` 当前以补充设定的方式拼接在基础 system prompt 后面：

```text
当前角色补充设定：
{persona}
```

这种方式适合 MVP 快速验证，但后续建议引入模板文件和版本管理，避免 Prompt 逻辑长期硬编码在 Python 文件中。

### 5.4 LLM Runtime 模块

文件：

```text
app/llm_runtime/client.py
app/llm_runtime/models.py
```

当前核心类：

```text
LLMClient
```

统一入口：

```text
chat(messages: list[LLMMessage]) -> LLMResponse
```

当前支持两种运行模式：

| 模式 | 配置值 | 说明 |
| --- | --- | --- |
| Mock | `AI_BUDDY_LLM_MODE=mock` | 本地模拟回复，用于跑通 API 链路 |
| Qwen | `AI_BUDDY_LLM_MODE=qwen` | 调用百炼 Qwen Chat Completions API |

这个模块的关键设计原则是：

```text
业务代码 -> LLMClient -> 具体模型供应商
```

业务代码不直接依赖 Qwen、OpenAI 或其他模型 API。未来扩展 OpenAI、Claude、Gemini、本地模型时，优先在 `llm_runtime` 内新增 provider 适配，而不是改动 API 或 Prompt 业务层。

### 5.5 Infra Config 模块

文件：

```text
app/infra/config.py
```

当前配置分为两类：

| 配置类 | 环境变量前缀 | 说明 |
| --- | --- | --- |
| `Settings` | `AI_BUDDY_` | 应用级配置 |
| `QwenSettings` | `QWEN_` | Qwen 供应商配置 |

应用配置：

```text
AI_BUDDY_APP_NAME=ai-buddy
AI_BUDDY_LLM_MODE=mock
```

Qwen 配置：

```text
QWEN_API_KEY=
QWEN_BASE_URL=
QWEN_MODEL=qwen-plus
QWEN_TIMEOUT=30
```

`QwenSettings.chat_completions_url` 会根据 `QWEN_BASE_URL` 自动补齐 `/chat/completions`，从而兼容两种配置方式：

```text
QWEN_BASE_URL=https://xxx
QWEN_BASE_URL=https://xxx/chat/completions
```

## 6. 多轮对话设计

v1.0 当前接口已经包含 `user_id` 和 `chat_id`，但尚未实现真正的历史上下文管理。阶段性设计如下。

### 6.1 v1.0 当前状态

当前每次请求只会构建：

```text
system message
user message
```

也就是说，模型不会自动看到同一 `chat_id` 下的历史消息。

当前能力更准确地说是：

```text
具备多轮对话接口形态，但尚未具备多轮上下文记忆能力。
```

### 6.2 v1.1 演进方案

下一阶段建议新增：

```text
app/conversation/
├── models.py
├── service.py
├── repository.py
└── context.py
```

职责拆分：

| 文件 | 职责 |
| --- | --- |
| `service.py` | 编排聊天流程，成为 API 和底层能力之间的应用服务 |
| `repository.py` | 负责消息读写，初期可用内存存储，后续切换数据库 |
| `context.py` | 根据 `chat_id` 裁剪历史消息，组装上下文窗口 |
| `models.py` | 定义消息、会话、请求响应等模型 |

目标链路：

```text
Chat API
  |
  v
ConversationService
  |
  +--> ConversationRepository 读取历史消息
  |
  +--> ContextBuilder 组装上下文
  |
  +--> PromptBuilder 构建 system/persona prompt
  |
  +--> LLMClient 调用模型
  |
  +--> ConversationRepository 保存 user/assistant 消息
  |
  v
ChatResponse
```

### 6.3 上下文窗口策略

后续多轮对话建议采用三层上下文：

```text
System Prompt
  +
Persona Prompt
  +
Recent Messages
```

更远期可以扩展为：

```text
System Prompt
  +
Persona Prompt
  +
Conversation Summary
  +
Relevant Memories
  +
Recent Messages
  +
Current User Message
```

v1.1 阶段先实现 `Recent Messages` 即可，不必过早引入摘要和长期记忆。

## 7. 配置和运行

### 7.1 本地 Mock 模式

`.env` 示例：

```text
AI_BUDDY_LLM_MODE=mock
```

启动：

```bash
uvicorn app.main:app --reload
```

访问：

```text
http://127.0.0.1:8000/docs
```

### 7.2 Qwen 模式

`.env` 示例：

```text
AI_BUDDY_LLM_MODE=qwen
QWEN_API_KEY=your-api-key
QWEN_BASE_URL=your-openai-compatible-base-url
QWEN_MODEL=qwen-plus
QWEN_TIMEOUT=30
```

启动后调用同一个 `/api/chat` 接口即可。API 层不需要关心当前使用的是 mock 还是真实模型。

## 8. API 设计

### 8.1 健康检查

```text
GET /health
```

响应：

```json
{
  "status": "ok"
}
```

### 8.2 聊天接口

```text
POST /api/chat
```

请求示例：

```json
{
  "user_id": "user_001",
  "chat_id": null,
  "message": "我今天想学习 FastAPI，但不知道从哪里开始。",
  "persona": "请像一位耐心的软件架构师一样回答。"
}
```

响应示例：

```json
{
  "chat_id": "generated-chat-id",
  "reply": "可以，我们先把 FastAPI 学习拆成几个小台阶...",
  "model": "mock-model"
}
```

## 9. 设计原则

### 9.1 业务层不直接调用模型供应商

当前 `app.api.chat` 只依赖：

```text
LLMClient
```

而不是直接调用 Qwen API。这样可以保证后续模型切换时，改动集中在 `llm_runtime` 内部。

### 9.2 Prompt 独立管理

Prompt 构建逻辑放在 `prompt_engine`，而不是散落在 API 层。这样后续可以自然演进出：

- Prompt 模板文件。
- Prompt 版本号。
- Persona 配置。
- A/B 实验。
- 安全提示词策略。

### 9.3 先打通闭环，再增加复杂能力

v1.0 不引入数据库、向量库、工具调用和 Agent 编排。这样可以先验证最核心链路：

```text
请求 -> Prompt -> LLM -> 响应
```

等闭环稳定后，再逐步引入状态管理和长期记忆。

## 10. 当前风险和改进点

| 风险 / 不足 | 影响 | 建议 |
| --- | --- | --- |
| 没有真正保存历史消息 | `chat_id` 暂时不能形成真实多轮上下文 | v1.1 增加 `ConversationService` 和 `ConversationRepository` |
| Prompt 硬编码在 Python 文件中 | 后续版本管理和实验不方便 | 引入 `prompt_engine/templates/*.yaml` |
| 缺少模型错误统一处理 | Qwen API 异常会直接向上抛出 | 增加统一异常和 API 错误响应 |
| 缺少重试和超时策略抽象 | 网络波动时稳定性不足 | 在 `llm_runtime` 增加 retry/timeout 策略 |
| 缺少测试 | 后续重构风险较高 | 增加 API、PromptBuilder、LLMClient mock 测试 |
| 缺少流式响应 | 陪伴场景响应体感不够好 | 后续增加 SSE 或 StreamingResponse |

## 11. 后续版本路线

### v1.1 多轮对话

- 新增 `ConversationService`。
- 新增会话消息存储。
- 支持按 `chat_id` 读取历史消息。
- 实现最近 N 轮上下文拼接。
- 将 API 层编排下沉到 service 层。

### v1.2 Prompt 工程增强

- 将 system prompt 迁移到 YAML 模板。
- 增加 Prompt 版本号。
- 增加 Persona 模板。
- 增加 Prompt 渲染变量。

### v1.3 LLM Runtime 增强

- 增加统一异常类型。
- 增加 retry、timeout、限流。
- 增加流式输出。
- 预留多模型 provider 接口。

### v1.4 Memory MVP

- 从对话中抽取用户事实和偏好。
- 建立 memory repository。
- 在聊天时召回相关记忆。
- 将陪伴体验从短期聊天推进到长期关系。

### v1.5 Tools / Agent 预研

- 建立工具注册表。
- 支持 Function Calling。
- 预留 MCP Server 接入。
- 引入轻量 Agent workflow。

## 12. v1.0 验收标准

v1.0 可以按以下标准验收：

- 应用可以通过 `uvicorn app.main:app --reload` 启动。
- `GET /health` 返回 `{"status": "ok"}`。
- `POST /api/chat` 在 mock 模式下可以返回模拟回复。
- `POST /api/chat` 在 qwen 模式且配置正确时可以返回真实模型回复。
- API 层没有直接调用 Qwen HTTP 接口。
- Prompt 构建逻辑集中在 `PromptBuilder`。
- 请求和响应模型由 Pydantic 明确定义。
- `chat_id` 可以生成并返回，为后续多轮对话保留协议基础。

## 13. 总结

AI-BUDDY MVP v1.0 的核心目标是建立 AI 陪伴应用的第一条可运行主链路。当前代码已经完成了从 FastAPI 接口、Prompt 构建、LLM Runtime 到 Mock/Qwen 调用的基础闭环。

从架构上看，当前版本最重要的成果不是功能复杂度，而是边界清晰：

```text
API 负责接入
Prompt Engine 负责提示词
LLM Runtime 负责模型调用
Conversation Model 负责协议结构
Infra Config 负责配置隔离
```

下一阶段应优先补齐真正的多轮对话状态管理，再继续推进 Prompt 模板化、LLM Runtime 稳定性和长期记忆能力。
