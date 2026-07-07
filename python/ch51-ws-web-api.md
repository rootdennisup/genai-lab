# 模块五：并发与 Web 服务 (Web & Service)--Web API 开发
本模块解决大模型应用的服务化，使之成为可调用的后端接口或集成工具。

- [模块五：并发与 Web 服务 (Web \& Service)--Web API 开发](#模块五并发与-web-服务-web--service--web-api-开发)
  - [1 HTTP 基础](#1-http-基础)
    - [1.1 网络工程视角下的工作流程](#11-网络工程视角下的工作流程)
    - [1.2 web api 视角下的工作流程](#12-web-api-视角下的工作流程)
    - [1.3 工作原理](#13-工作原理)
    - [1.4 HTTP 四要素](#14-http-四要素)
  - [2 requests \& httpx](#2-requests--httpx)
    - [2.1 核心定位：经典标准 vs. 现代进化](#21-核心定位经典标准-vs-现代进化)
    - [2.2 关键技术细节对比](#22-关键技术细节对比)
    - [2.3 工作原理](#23-工作原理)
    - [2.4 requests vs. httpx](#24-requests-vs-httpx)
    - [2.5 什么时候该选谁](#25-什么时候该选谁)

## 1 HTTP 基础

- HTTP 是用于分布式、协作式和超媒体信息系统的应用层协议。在 Web API 领域，它被视为客户端（如浏览器、手机 App）与服务器（如 FastAPI 应用）之间交换数据的“语言”。
- 它定义了数据如何被请求、传输和响应。通过 HTTP，开发者可以实现资源的定位（URL/路径）、动作定义（方法）数据载入（请求体/响应体）。

### 1.1 网络工程视角下的工作流程
- 在网络工程的宏观视角下，HTTP 处于应用层，是用户交互的最前端。
- 当你在浏览器输入地址或在代码中使用 httpx 发送请求时，就触发了 HTTP 流程。

具体流程：
- **客户端发起请求**：通过特定的主机地址和端口（如 127.0.0.1:8000）触达服务器。
- **Web 服务器中转**：服务器（如 Uvicorn）接收原始的网络包并将其传递给 Web 框架。
- **框架处理**：Starlette（FastAPI 的底层依赖）负责解析 HTTP 细节。
- **响应返回**：处理完成后，数据以 HTTP 响应的形式原路返回。


### 1.2 web api 视角下的工作流程
- 在 Web API 开发视角中，HTTP 是定义接口契约的核心，它定义了 API 的入口（Endpoints）。
- 每一行 FastAPI 代码几乎都在处理 HTTP 的某个组成部分（如 @app.get("/") 定义了方法和路径）

具体流程：
- **路由匹配**：服务器根据 HTTP 请求的路径（Path）和方法（Method）寻找对应的处理函数。
- **数据提取**：从 JSON 请求体、路径参数、查询参数、Headers 或 Cookies 中读取输入。
- **校验与转换**：利用 Pydantic 验证 HTTP 输入是否符合声明的 Python 类型。
- **响应生成**：将执行结果转换为 JSON 格式，并附带合适的 HTTP 状态码 返回给客户端。

### 1.3 工作原理
HTTP 遵循典型的**请求-响应（Request-Response）模型**：

- **无状态性**：每个请求通常是独立的，服务器不保留之前请求的上下文（除非使用 Cookies 或 Sessions）。
- **结构化交换**：
    - **请求（Request）**：包含方法（GET/POST 等）、资源定位符（URL）、头部（Headers）和正文（Body）。
    - **响应（Response）**：包含状态码（如 200 OK, 404 Not Found）、头部和正文（通常是 JSON 格式）。
- **标准化支持**：FastAPI 完全兼容 OpenAPI 标准，意味着它能根据 HTTP 逻辑自动生成 Swagger UI 等交互式文档。

### 1.4 HTTP 四要素
HTTP 四要素为：路径 (Path)、方法 (Method)、参数 (Parameters)、状态码 (Status Codes)。

[http_demo](../codes/python_base/app/ws/http_demo.py)

**1> 请求路径**：

是 API 用于接收请求的具体地址，用于定位资源。
- 固定路径：如 /
- 动态路径：如 /items/{item_id}，其中 {item_id} 占位符，表示客户端可以根据需要请求不同的资源。

**2> HTTP 方法**：

定义了客户端想要对资源执行的操作。
- ``GET`` ：用于从服务器获取数据，参数通常放在路径或查询字符串中。
- ``PUT/POST/PATCH``：用于向服务器发送数据以更新现有资源，数据通常承载于 JSON 请求体中。

3> **请求参数**：

FastAPI 允许从不同的位置接收参数，并通过类型提示（Type Hints）自动进行校验和转换。
- **路径参数**（Path Parameters）：直接嵌入在 URL 路径中，用于标识特定资源，如 /items/{item_id}。
- **查询参数**（Query Parameters）：位于 URL 问号之后的部分，用于过滤或可选设置。如 ?q=somequery 中的 q 是一个字符串参数。如果参数被声明为 = None，则在 HTTP 请求中是可选的。
- **请求体** (Request Body)：主要用于 POST 或 PUT 请求。它通常是以 JSON 格式传输的复杂对象。

4> **响应状态码**：

状态码由服务器返回，告知客户端请求的结果。
- 成功 (如 200 OK)：默认情况下，当一切正常时，FastAPI 会返回状态码 200。
- 当数据无效、未授权或服务器出错时，应当通过合适的 HTTP 状态码告知客户端。
- 自定义状态码：FastAPI 允许在路径操作中根据业务逻辑更改或添加额外的状态码。


**其他**：

- **头部与安全（Headers & Security）**：关键的认证信息（如 JWT 令牌、OAuth2）通常存放在 HTTP Headers 中，而非请求体中。
- **数据格式（Content-Type）**：现代 Web API 绝大多数使用 application/json。FastAPI 会自动完成 JSON 的读取与输出转换，极大减少了人为错误。

## 2 requests & httpx
- 在 Web API 开发中（尤其是 FastAPI），requests 和 httpx 是最常用的两个 HTTP 客户端库。
- 用于模拟客户端向服务器发起 HTTP 请求（如 GET、POST 等），获取响应数据，处理 Headers、Cookies 和 JSON 等。


### 2.1 核心定位：经典标准 vs. 现代进化

- ``requests``：是 Python 同步 HTTP 通信的事实标准。它的设计理念是 **“为人而写”**，极大地简化了早期 urllib 繁琐的操作。
- ``httpx``：是专为 Python 3 设计的下一代 HTTP 客户端。它在继承 requests 优雅 API 的基础上，增加了对异步 (Async) 和 HTTP/2 的原生支持，是 FastAPI 官方指定的测试与通信伙伴

### 2.2 关键技术细节对比

**1> 执行模式与性能 (Sync vs. Async)**

这是两者最本质的区别。
- **requests (同步阻塞)**：每发起一个请求，程序必须等待服务器返回响应后才能继续执行下一行代码。在高并发场景（如 FastAPI 异步路由中调用外部 API）下，这会导致性能瓶颈。
- **httpx (异步非阻塞)**：支持 async/await 语法，它允许程序在等待网络响应的同时去处理其他任务。在 FastAPI 这种基于 Starlette 的高性能框架中，使用 httpx 可以充分发挥异步并发的优势。

**2> 资源管理与连接池 (Context Management)**
- ``requests.Session()``：通过 Session 对象实现连接复用（Connection Pooling），避免频繁创建 TCP 连接的开销。
- ``httpx.Client() / AsyncClient()``：提供了类似的连接池管理，但其上下文管理器（with 或 async with）使用更为严格。这种设计符合 Python 的“预定义清理操作”原则，确保连接在操作完成后被自动且安全地释放。

**3> FastAPI 工程集成深度**
- **内置依赖**：当安装 fastapi[standard] 时，系统会自动安装 httpx。因为 FastAPI 的接口测试工具 TestClient 在底层依赖 httpx 来模拟 HTTP 请求。
- **测试体验**：FastAPI 推荐结合 pytest 和 httpx 进行极其简单的测试。通过 httpx 的 AsyncClient，你可以像在生产环境中一样测试异步接口。


### 2.3 工作原理
- ``requests``：基于底层的 urllib3 库。它在发起请求时会阻塞当前线程，直到服务器返回响应或超时。这种模式在处理高并发或需要非阻塞 IO 的 Web 服务器（如 FastAPI）中可能会成为性能瓶颈。
- ``httpx``：基于异步 I/O 驱动（如 anyio）。它允许在等待服务器响应时释放 CPU 去处理其他任务（即协程切换），这使得它在执行大量并发网络请求时效率显著高于 requests。

### 2.4 requests vs. httpx


|   关键特性   |       requests      | httpx                   | 备注                    | 
| ------------|---------------------|-------------------------|-------------------------|
| 异步支持     | 不支持               | 完美支持 (async/await)  | httpx 适合异步框架       |
| HTTP/2 支持  | 100% (行业标准)      | 95% (兼容 requests)     | 迁移成本极低             |
| FastAPI 集成 | 外部库，无直接依赖    | 核心依赖                | TestClient 必须使用 httpx|
| 核心底层     | urllib3              | httpcore               | httpx 底层更现代         |
| 安装方式     | pip install requests | pip install httpx      |                         |
| 数据校验     | 需手动配合            | 常配合 Pydantic        | 自动完成 JSON 与模型转换  |


### 2.5 什么时候该选谁

- 选择 ``requests`` 的场景：
    - 编写简单的自动化脚本。
    - 维护传统的同步 Web 框架项目（如旧版 Flask）。
    - 对 asyncio 概念不熟悉且对并发要求不高的初学者。

- 选择 ``httpx`` 的场景：
    - 开发 FastAPI 应用：无论是调用外部 API 还是编写接口测试用例。
    - 高性能爬虫：需要利用异步特性提升抓取速度。
    - 追求标准化：希望代码能支持现代协议（HTTP/2）并获得更好的编辑器自动补全支持。


