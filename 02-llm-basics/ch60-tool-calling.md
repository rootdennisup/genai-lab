# Tool Calling（工具调用）

Tool Calling（工具调用）是大模型通往“智能体（Agent）”的桥梁，让 AI 能够突破文本生成的限制，去查询数据库、调用 API、甚至操作你的本地电脑。

## 1 基本概念
- **模型角色**： 模型本身“不执行”代码，而是充当 “智能 API 调用者”，负责根据需求生成结构化的参数。
- 形态演进：
  - ``Text Completion``：生成非结构化文本。
  - ``Function/Tool Calling``：输出遵循 ``JSON Schema`` 的结构化指令。

- **接口规范**： 强烈建议使用 API 原生的 tools 字段，而非在 Prompt 中手动描述，这能显著降低错误率并保持模型处于训练分布内。

## 2 工具定义与 Schema 约束
- **JSON Schema 构造**： 为工具定义准确的 name、description 和 parameters。
- **语义化命名** (Semantic Correctness)：
  - **工具名**（如 semantic_search）和参数名（如 query）必须具备清晰的语义，这对模型决策至关重要。
- **描述字段** (Description)： 编写 1-2 句简洁且关键的描述，说明工具的作用及“何时”应该调用它。
- **示例锚定** (# Examples)： 在 Prompt 中提供具体的工具调用示例，帮助模型理解复杂的参数逻辑或多工具组合场景。

## 3 决策策略与参数抽取 (Model Decision & Extraction)
- **参数提取完备性** (Extraction Completeness)： 在处理长文档抽取时，明确要求模型提取所有必填字段，缺失项填入 null 而非推测。

- **主动性控制** (Agentic Eagerness)：
  - 降低主动性：通过调低 reasoning_effort 限制模型进行发散性工具调用。
  - 增强主动性：设置显式的完成标准，鼓励模型在遇到困难时重试或自主探索路径。 

- **决策规约**：提供“决策规则”而非绝对化指令（如 ALWAYS/NEVER），赋予模型在模糊场景下询问用户或继续搜索的灵活性

## 4 工具执行与并行化处理

- 并行调用 (Parallel Tool Calling)：
  - 支持单回合内发起多个调用（如同时扫描三个数据库）以提高效率。
  - 排序原则：建议将并行项与响应按固定顺序排列，以维持推理的稳定性。

- 特定编码工具：
  - apply_patch：用于结构化地修改文件，比生成全量代码更高效。
  - shell：允许模型在受控终端中执行命令，形成“计划-执行”闭环。

- 响应截断策略 (Truncation)：当工具返回结果过长时，采用 10k Token 限制，并执行“中间截断”（保留首尾，截断中间）。


## 5 状态管理与推理持久化
- 推理持久化 (Reasoning Persistence)：
  - 利用 previous_response_id 回传先前的推理标记（Reasoning Tokens），消除每次回填结果后重新构建计划（Planning）的需要。

- 对话阶段标识 (Phase Handling)：
  - 通过 phase 参数区分 commentary（思考/前导）与 final_answer（最终答案）。
  - 状态回传：在多轮工具调用中，必须保留并原样传回助手消息的 phase 字段，以防止模型过早停止或逻辑断层。

## 6 交互透明度与校验 (UX & Reliability)
- 工具前导说明 (Tool Preambles)：要求模型在执行重大工具调用前生成 1-2 句说明，向用户同步“正在做什么”及“为什么”。
- 验证循环 (Verification Loops)：在执行高风险、不可逆操作（如删除、扣费）前，指令模型进行一次“自检”或编写单元测试进行验证。
- 失败重试逻辑：针对“软失败”实施指数退避（Exponential Backoff）重试，确保系统的稳健性。



