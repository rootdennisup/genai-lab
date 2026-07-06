# 模块四：IO 与文件处理 (File Processing)--文件与数据处理


## 1 JSON 数据解析
- JSON (JavaScript Object Notation) 是数据交换、配置管理和 API 开发的核心。
- Python 通过标准库和现代第三方库（如 Pydantic 和 FastAPI）提供了从基础到工业级的完整解决方案。

### 1.1 Python 标准库：json 模块
用于将内存中的 Python 对象（如列表、字典）转换为 JSON 格式的字符串（序列化），或者将 JSON 数据解析回 Python 对象（反序列化）。

- **适用场景**：简单的脚本开发、小型配置文件的读写。
- **常用操作**：
    - **文件操作**：使用 json.dump() 将数据写入文件，使用 json.load() 从文件中读取。
    - **字符串操作**：使用 json.dumps() 将对象转为字符串，使用 json.loads() 将字符串转为对象。

- **JSON 类型转换对应表**：

    |          Python -->           |           JSON -->         | Python                      | 
    | ------------------------------|----------------------------|---------------------------- |
    | dict                          | object                     | dict                        |
    | list, tuple                   | array                      | list                        |
    | str                           | string                     | str                         |
    |int,float, int- & float-derived Enums| number               | number(int)-->int，number(real)-->float |
    | True                          | true                       | True                        |
    | False                         | false                      | False                       |
    | None                          | null                       | None                        |

## 1.2 工程化方案：Pydantic
在处理复杂或嵌套的数据时，标准库往往难以胜任。Pydantic 是目前 Python 中最流行的选择，它将 JSON 处理提升到了“数据验证”的层面。

- **类型驱动的校验**：Pydantic 利用 Python 的类型提示 (Type Hints) 来控制序列化。你只需定义一个模型，它就能确保输入的 JSON 数据完全符合预期的格式和类型。
- **JSON Schema 生成**：Pydantic 模型可以自动生成 JSON Schema。这使得你的数据结构可以被其他工具理解，是实现自动化文档的基础。
- **嵌套对象支持**：它能够轻松应对多层嵌套的复杂 JSON 对象，并在每一层都执行严格的校验。

## 1.3 Web 开发中的自动化：FastAPI
在 FastAPI 框架中，JSON 处理几乎是全自动化的，它将 json 模块和 Pydantic 深度集成。
- **输入转换（反序列化）**：当你声明一个请求体参数时，FastAPI 会自动从网络请求中读取 JSON 数据，验证其合法性，并将其转换为对应的 Python 数据类型（如 Pydantic 模型对象）。
- **输出转换（序列化**）：当你从函数返回 Python 字典、列表或数据库模型时，FastAPI 会自动将其转换为符合标准的 JSON 响应发送给客户端。
- **支持高级类型**：除了基础类型外，它还能自动处理 datetime、UUID 等标准库对象的 JSON 序列化。
- **性能增强**：如果对性能有极高要求，FastAPI 还支持使用 orjson 或 ujson 等第三方可选依赖来替代标准 JSON 编码器。

### 1.4 工程实践 & 总结

- **工程实践**：
    - **简单任务**：如果只是读写一个简单的本地 .json 配置文件，使用内置的 json 模块即可。[simple_json](../codes/python_base/app/fp/simple_json.py)   
    - **数据模型**：在编写需要确保数据准确性的逻辑时，务必使用 Pydantic BaseModel。[pydantic_json](../codes/python_base/app/ds/pydantic_json.py)
    - **API 接口**：在开发 Web 服务时，利用 FastAPI 的自动序列化特性，只需声明一次类型，即可获得数据验证、转换和自动生成的交互式文档（Swagger UI）。[fastapi_json](../codes/python_base/app/fp/fastapi_json.py)
   

- **总结**：
    - 内置 json 解决了数据的“存储”问题。
    - Pydantic 通过类型提示解决了数据的“准确性”和“安全性”问题。
    - FastAPI 将上述能力整合，解决了 Web 工程中的“自动化”和“标准化”问题。

## 2 CSV处理
- CSV（Comma-Separated Values，逗号分隔值） 是处理表格数据最常用的轻量级格式。
- Python 通过内置的 csv 模块对以纯文本形式存储的表格数据进行读取和写入的操作。

CSV 的特点：
- **简单易读**：CSV 是纯文本文件，可以使用任何文本编辑器或 Excel 打开。
- **跨平台兼容**：它是不同系统（如数据库、Excel、Web 应用）之间交换数据的通用标准。
- **轻量高效**：相比于 Excel (.xlsx) ，CSV 没有复杂的格式元数据，处理速度更快，占用空间更小。
- **工程化对接**：在 FastAPI 应用中，常用于处理用户上传的批量数据脚本或导出报表。

### 2.1 操作流程
CSV 的操作建立在文件读写的基础之上，基本流程如下：
- **打开文件**：使用 open() 函数，配合 newline='' 参数（防止跨平台换行符问题）。
- **创建处理器**：将文件对象传递给 csv.reader（读取）或 csv.writer（写入）。
- **执行操作**：循环遍历行数据，或使用 writerow() 写入数据。
- **自动关闭**：配合 with 语句确保资源释放。

demo 示例：
- [csv_base](../codes/python_base/app/fp/csv_base.py)
- [csv_dict](../codes/python_base/app/fp/csv_dict.py)

### 2.2 关键点说明

- **newline='' 的必要性**：在 Python 3 中打开 CSV 文件时，必须指定 newline=''，否则在 Windows 等系统上可能会出现多余的空行。
- **编码问题**：处理中文时建议统一使用 encoding='utf-8' 或 encoding='utf-8-sig'（后者能让 Excel 正常识别 UTF-8 编码的中文）。
- **数据验证**：在现代工程中，读取 CSV 每一行后，通常会将其传入 Pydantic 模型进行类型校验，确保数据符合业务要求。

### 2.3 适用场景与局限性

- **适用场景：**
    - 小型数据集的导入导出。
    - 数据库表的简单备份。
    - 自动化测试的参数化数据源。

- **局限性：**
    - 无数据类型：CSV 里的所有东西默认都是字符串，需要手动转换类型。
    - 非结构化：不适合存储复杂的嵌套对象（此时应选 JSON）。
    - 性能瓶颈：对于数百万行的大规模数据分析，纯 csv 模块效率不如专业工具。

### 2.4 替代方案
- **Pandas (read_csv)**：如果是进行**大规模数据分析或复杂的清洗工作**，Pandas 是 Python 界的行业标准。
- **SQLModel / SQLAlchemy**：如果数据具有**复杂的关联关系**，应直接存入关系型数据库。
- **FastAPI UploadFile**：在 Web 环境下，使用 FastAPI 的文件处理类可以更方便地接收前端上传的 CSV 并进行流式处理。


## 3 Markdown 格式解析库
在进行 Markdown 处理时，应优先掌握源文件提到的“读取与切分”基本功。对于简单的任务，使用标准库配合正则表达式即可；而对于需要将 Markdown 转换为 HTML 或进行复杂语法解析的任务，则需要引入上述第三方库，并配合 Pydantic 进行数据结构化建模。

### 3.1 解析 Markdown 的通用流程（基于标准库）
在没有第三方库的情况下，源文件通过“文件读写”和“核心容器”模块展示了基础的解析逻辑：
- **路径管理**：使用 pathlib 模块定位 Markdown 文件，利用其对象化接口确保在不同操作系统（Windows/Linux）下的路径兼容性。
- **安全读取**：使用 with 语句（上下文管理器）打开文件，确保即使在解析大型文档出错时，文件句柄也能被正确释放。
- **段落切分与封装**：利用 列表推导式 对读取的原始文本进行处理。如，通过识别连续的换行符（\n\n）来切分段落，并将每一段内容封装进字典中。

### 3.2 常见的 Markdown 解析库
- ``Python-Markdown``：最基础的解析库，遵循标准的 Python 实现，支持多种插件扩展（如表格、目录等）。
- ``Mistune``：号称是 Python 中最快的纯 Python 实现的 Markdown 解析库，适合需要高性能解析的场景。
- ``Markdown-it-py``：功能极其强大且完全兼容 CommonMark 规范的解析库，常用于生成复杂的文档系统。


[markdown_to_api](../codes/python_base/app/fp/markdown_to_api.py)



