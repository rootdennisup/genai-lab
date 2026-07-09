# Python 工程基础

目标：快速补齐大模型应用开发所需的 Python 工程能力，能够开发脚本、API 服务和简单 AI 工具。

## Python技能体系

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
  - [Web API 开发*](./ch51-WS-web-api.md)
  - [FastAPI 框架*](./ch52-WS-fastapi.md)
  - [Web 应用*](./ch53-WS-web-applicatiion.md)
  - [pytest 自动化测试框架](./ch54-WS-pytest.md)


## 实战项目：AI Excel Assistant v1 | 4h
- 目标：先不接入大模型，做一个普通 Excel 批处理工具。

- 功能清单：
  - 上传 Excel
  - 读取 Sheet
  - 读取表头
  - 按字段过滤数据
  - 批量清洗空值
  - 生成新列
  - 导出处理后的 Excel
  - 提供 FastAPI 接口

## 最小验收标准
- [☑️] 能读懂 Python 基础代码
- [☑️] 熟悉 list / dict / JSON
- [☑️] 能写函数和简单 class
- [☑️] 能处理文件和路径
- [☑️] 能写 pydantic 数据模型
- [☑️] 能写 FastAPI 接口
- [☑️] 能调用 HTTP API
- [☑️] 能管理虚拟环境和依赖
- [☑️] 能看懂常见报错
- [☑️] 能把代码组织成小项目

## 学习资料

| 资料                   | 用途                                 |
| ---------------------- | ------------------------------------ |
| Python 官方教程        | 系统补语法、数据结构、模块、异常、类 |
| FastAPI 官方文档       | 学 API 开发、请求响应、Pydantic      |
| Pydantic 官方文档      | 学数据模型、参数校验                 |
| Pytest 官方文档        | 学基础测试                           |
| pandas / openpyxl 文档 | 用于 Excel、CSV 和结构化数据处理     |

- [Python 官方教程](https://docs.python.org/zh-cn/3.14/tutorial/index.html)
- [Python3 菜鸟教程](https://www.runoob.com/python3/python3-tutorial.html)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/zh/)
- [Pydantic 官方文档](https://pydantic.com.cn/)
- [Pytest 官方文档](https://pytest.cn/en/stable/)
