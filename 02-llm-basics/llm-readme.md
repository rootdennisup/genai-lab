# LLM 应用开发基础

目标：快速补齐大模型应用开发所需的 Python 工程能力，能够开发脚本、API 服务和简单 AI 工具。

1.LLM 基础机制：Token、上下文、参数
2.OpenAI / Qwen / DeepSeek API 调用
3.Prompt Engineering
4.结构化输出 JSON Schema
5.Function Call / Tool Calling
6.多轮对话与上下文管理
7.记忆
8.错误处理、重试、限流、成本统计


      
 现在开始学习 结构化输出，主要包含以下内容：
1.JSON输出
2.Schema约束
3.Pydantic解析
4.输出校验
5.失败重试
要求：
1.如果你觉得这个模块还有其他必要的知识可以补充，如果有不明确的地方可以提出质疑
2.按我接下来的指令一个一个的拆解学习
3.教我用 notebooLM 提示词，比如 学习 JSON输出，在会话中提示词应该怎么写     
      
      
      
      



现在开始学习 1.LLM 基础认知，主要包含以下内容：
1.Token
2.上下文窗口
3.Temperature
4.TopP
5.模型能力边界
6.幻觉
要求：
1.如果你觉得这个模块还有其他必要的知识可以补充
2.按我接下来的指令一个一个的拆解学习
3.教我用 notebooLM 提示词，比如 学习 Token，在会话中提示词应该怎么写

## LLM 基础技能体系



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

| 资料                   | 用途                                 |
| ---------------------- | ------------------------------------ |
| 大模型应用开发极简入门        | 指导书 |
| OpenAI API 官方文档        | 模型调用、结构化输出、工具调用和 Prompt 设计 |
| OpenAI Cookbook       | 提供大量 API 使用示例，适合边看边改代码      |
| OpenAI Prompting / Prompt Engineering | 建立 Prompt 基础方法论                 |

- 《大模型应用开发极简入门》
- [OpenAI API 官方文档](https://developers.openai.com/api/docs)
- [llm-cookbook](https://github.com/datawhalechina/llm-cookbook)
- [OpenAI Prompting](https://developers.openai.com/api/docs/guides/prompt-guidance)
- [Prompt Engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)
- [GPT-5 Prompting Guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide)
- [mem0](https://github.com/mem0ai/mem0)
