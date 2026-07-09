# LLM 应用调用基础

目标：快速补齐大模型应用开发所需的 Python 工程能力，能够开发脚本、API 服务和简单 AI 工具。


      System_Prompt
      User_Prompt
      Few_Shot
      Chain_of_Thought使用边界
      Prompt模板化
      Prompt版本管理



现在开始学习 1.Prompt工程，主要包含以下内容：
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

- 模块1：工程基础(Engineering Foundation) | 6h 
  - [环境管理*](./ch11-EF-environment-manage.md)
  - [配置分离*](./ch12-EF-config-separation.md)
  - [工程规范](./ch13-EF-engineering-specification.md)
  - [Python 执行引擎](./ch14-EF-execution-engine.md)
- 模块2：逻辑核心 (Logical Core)  | 8h
  - [基础语法](./ch21-LC-basic-grammar.md)
  - [函数与高级特性*](./ch22-LC-function&feature.md)
  - [迭代与生成*](./ch23-LC-iterator&generator.md)
  - [命名空间与异常处理](./ch24-LC-namespace&exception.md)
- 模块3：数据建模与结构 (Data Structuring) | 6h
  - [核心容器应用](./ch31-DS-data-structure.md)
  - [面向对象与类型提示*](./ch32-DS-oop-type-hints.md)
  - [Pydantic 详解*](./ch33-DS-pydantic.md)
- 模块4：IO 与文件处理 (File Processing) | 4h
  - [系统与标准库](./ch41-FP-standard-lib.md)
  - [文件与路径操作*](./ch42-FP-path-ops.md)
  - [文件与数据处理*](./ch43-FP-data-parsing.md)
- 模块5：并发与 Web 服务 (Web & Service) | 8h
  - [Web API 开发*](./ch51-ws-web-api.md)
  - [FastAPI 框架*](./ch52-ws-fastapi.md)
  - [Web 应用*](./ch53-ws-web-applicatiion.md)
  - [pytest 自动化测试框架](./ch54-ws-pytest.md)
- 实战项目：AI Excel Assistant v1 | 4h

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
