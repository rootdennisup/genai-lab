# LLM 应用开发基础
- **学习目标**：学习把大模型接入应用，掌握大模型应用开发的调用机制和工程控制能力。
- **学习思路**：底层机制 → 推理控制 → 接口规范 → 提示工程 → 核心能力（工具/上下文）。

## LLM 基础技能体系

- 模块1：LLM 基础底层机制 (The Physics of LLMs)
  - [Token 与分词机制*](./ch11-LP-llm-physics.md)
  - [推理参数与模型边界*](./ch12-LP-param-bound.md)
- 模块2：API 工程化与结构化交互 (API Engineering & Structured Interfacing)
  - [接口规范与消息流控制*](./ch21-API-inf-msg.md)
  - [JSON Schema 约束*](./ch22-API-json-schema.md)
- [模块3：提示词工程(Prompt Engineering)](./ch30-prompt-engineering.md)
- [模块4：工具调用(Tool Calling)](./ch40-tool-calling.md)
- [模块5：上下文工程（Context Engineering）](./ch50-context-engineering.md)


## 实战项目：

### 项目一：AI Weather Assistant
目标：用户自然语言问天气，模型自动判断是否调用天气工具。

练习点：

- Function Call
- 参数抽取
- 工具执行
- 工具结果回填
- 异常处理

### 项目二：AI Excel Assistant v2
- 目标：让 AI 根据自然语言操作 Excel。

示例指令：

- “帮我统计每个 SKU 的库存”
- “找出价格为空的行”
- “把标题控制在 75 个字符以内”
- “生成一列英文产品描述”

练习点：

- 自然语言转结构化任务
- LLM 调用工具
- JSON 输出控制
- Excel 操作函数封装

## 最小验收标准
- [☑️] 独立调用大模型 API
- [☑️] 控制模型输出 JSON
- [☑️] 设计 Function Call Schema
- [☑️] 处理工具调用失败
- [☑️] 构建一个简单 AI 工具型应用


## 学习资料

| 资料                   | 用途                                      |
| ---------------------- | ---------------------------------------- |
| 大模型应用开发极简入门   | 指导书                                    |
| OpenAI API 官方文档     | 模型调用、结构化输出、工具调用和 Prompt 设计 |
| OpenAI Cookbook        | 提供大量 API 使用示例，适合边看边改代码      |
| OpenAI Prompting / Prompt Engineering | 建立 Prompt 基础方法论      |

- 《大模型应用开发极简入门》
- [OpenAI API 官方文档](https://developers.openai.com/api/docs)
- [llm-cookbook](https://github.com/datawhalechina/llm-cookbook)
- [OpenAI Prompting](https://developers.openai.com/api/docs/guides/prompt-guidance)
- [Prompt Engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [GPT-5 Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide)
- [mem0](https://github.com/mem0ai/mem0)
