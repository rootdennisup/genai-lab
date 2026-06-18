# Python 工程基础

## 0 环境基础

- Python 安装：https://www.python.org/downloads/
- vscode 安装 python 扩展。
- 两个工具：pip、uv

### pip

Python 官方默认的包管理工具，用于 安装/卸载/导出 依赖。

- 练习：
    ```bash
    # 安装 FastAPI
    pip install fastapi
    # 查看
    pip list 
    # 卸载
    pip uninstall fastapi
    ```

当 Python 项目越来越复杂，pip 暴露出很多问题：

- **安装速度慢**，需要下载包、解析依赖、安装
- **虚拟环境独立管理**，pip 不负责环境管理
    ```bash
        python -m venv .venv

        # mac 激活
        source .venv/bin/activate
        # windows 激活
        .venv\Scripts\activate
    ```
- **依赖锁定不完善**
    ```bash
        # 今天安装
        openai==1.70
        # 明天安装
        openai==1.75
    ```
- **工具太多**，一个项目可能需要：
    ```text
        pip
        venv
        pip-tools
        virtualenv
        poetry
        pyenv
    ```

### uv
[uv](https://docs.astral.sh/uv/) 是 Astral 团队开发的新一代 Python 工具链，集成了 pip、venv、依赖管理和项目管理能力，速度更快、体验更统一。

- 高性能：Rust 编写，极快，相比 pip 提升 10~100 倍
- 依赖管理
- 虚拟环境管理
- Python 版本管理

> 可替代 pip、virtualenv、pip-tools 等工具的一体化方案


uv 能干什么：

- 创建项目
    ```bash
    uv init rag-learning
    ```
- 创建虚拟环境
    ```bash
    uv venv

    # 等价于
    python -m venv .venv
    ```
- 安装依赖
    ```bash
    uv add langchain

    # 等价于
    pip install langchain
    ```
- 删除依赖
    ```bash
    uv remove langchain
    ```
- 同步依赖
    ```bash
    # 自动安装项目全部依赖。
    uv sync
    ```
- 运行脚本
    ```bash
    uv run main.py
    ```

## 1 虚拟环境

虚拟环境（Virtual Environment）是 Python 工程化中实现**确定性运行时**和**依赖管理**的基础设施。

### 核心机制和作用

- **环境隔离** ：它是 Python 解释器的一个私有副本。通过隔离，开发者可以在不影响系统全局 Python 环境的情况下，为每个项目配置独立的依赖项。
- **依赖版本控制**：复杂工程中，不同项目可能依赖同一工具库的不同版本。虚拟环境允许在同一台机器上并存多个相互冲突的库版本，解决了版本碎片化和依赖地狱的问题。
- **标准库工具 venv**：从 Python 3.3 开始，标准库引入了 venv 模块作为创建虚拟环境的官方工具。它通过在项目目录下生成一个包含 Python 二进制文件拷贝（或符号链接）的文件夹，来构建运行时的上下文环境。
- **Shell 上下文切换（Activation）**：当用户执行“激活”脚本时，系统会修改当前终端会话的 PATH 环境变量，使得 python 和 pip 命令优先指向虚拟环境内部的路径，而非系统的全局路径。
- **无污染开发**：在构建 Web 框架（如 FastAPI）或进行自动化测试（如 pytest）时，建议在虚拟环境中进行操作，以确保开发环境的纯净和项目的可移植性。

### 怎么使用

- 1.**创建项目目录**，如：a_python_base
- 2.**创建虚拟环境**，使用 Python 自带的 venv 模块，习惯把环境文件夹命名为 .venv
    ```bash
    python -m venv .venv
    ```
    执行完，项目目录下会多了个 .venv 目录。
- 3.**激活虚拟环境**，需要运行环境内部的激活脚本
    ```bash
    # Windows
    .venv\Scripts\activate
    ```
    成功标志：你的命令行提示符前面会出现 (.venv) 字样
- 4.**在环境内安装包**(实践)：在当前的 .venv 文件夹里安装 FastAPI，不会影响其他项目
    ```bash
    pip install "fastapi[standard]"
    ```
- 5.**退出环境** ：输入 ``deactivate`` 回到全局环境


## 2 依赖管理

依赖管理（Dependency Management）是在软件开发过程中，对项目所依赖的外部软件包（Packages/Libraries）进行识别、安装、版本约束及更新的系统化过程。

### 解决了什么问题

- **防止“环境腐烂”与版本冲突**：若项目 A 依赖某个库的 1.0 版本，而项目 B 偷偷将其升级到了 2.0 导致代码报错，依赖管理能通过锁定版本号来确保环境的稳定性。
- **解决传递依赖**：当你安装 FastAPI 时，它本身也依赖 Pydantic 和 Starlette。依赖管理工具会自动识别并安装这些“库所依赖的库”，无需你手动一个个查找安装。
- **实现“一键复现”**：当你把代码发给同事或部署到服务器时，对方不需要询问你装了什么，只需运行一行命令，系统就会根据清单还原出和你电脑上一模一样的运行环境。


### 在系统中的位置

- 逻辑位置：项目根目录下的配置文件中，常用文件名 requirements.txt。
- 物理位置：当执行安装命令后，这些库会被下载并存放在当前 Python 环境（.venv）的 Lib\site-packages 文件夹内。

### 怎么使用（示例）

- **安装需要的库**，安装 FastAPI 及其标准依赖
    ```bash
    pip install "fastapi[standard]"
    ```
- **导出依赖**，使用以下命令将当前环境的所有依赖及其精确版本号保存到文件中
    ```bash
    pip freeze > requirements.txt
    ```
    项目根目录下会生成 requirements.txt 文件，其中记录了依赖的库和版本号。
- **分发与还原**：如果你把代码发给同事，他只需拿到代码和这个 requirements.txt 文件，在自己的虚拟环境中运行
    ```bash
    pip install -r requirements.txt
    ```
    系统会自动读取文件，把里面记录的所有库及其指定版本全部安装好，确保他的环境和你的一致。


## 3 环境变量
环境变量 (Environment Variables) 是操作系统提供的一种动态命名值，存储在系统的内存或配置文件中。它们以“键=值”的形式存在（例如 PATH=C:\Python314），供运行中的进程及其子进程访问，用以获取系统路径、配置参数或安全凭证。是实现程序 **“代码与配置分离”** 的关键。


### 解决了什么问题

- **硬编码带来的安全隐患**：不应该把数据库密码、API 密钥直接写在 .py 代码里。通过环境变量，敏感信息可以安全地存储在代码之外。
- **多环境切换的复杂性**：开发环境（Dev）和生产环境（Prod）需要不同的配置（如数据库地址）。通过环境变量，可以让同一套代码在不修改任何字符的情况下，根据环境自动切换。
- **程序发现与路径引导**：python3 利用环境变量动态查找解释器的路径，增加了脚本的通用性。

### 系统中的位置

环境变量主要存在 3 个地方：

- 系统/用户环境变量：Windows环境 在“系统属性”->“环境变量”中设置，永久生效。
- 进程级别（临时）：仅在当前的 PowerShell 或 CMD 窗口中有效，关闭窗口即消失。
- **项目配置（.env 文件）**：在项目根目录创建 .env 文件，结合 Pydantic-settings 等库自动将其加载为环境变量。


### 怎么使用
- 在 FastAPI 等框架中，使用 pydantic-settings 库来管理环境变量。
- 可以定义一个配置类，它会自动从系统环境变量或项目中的 .env 文件里读取对应的值，并进行类型检查。


## 4 项目结构

### 创建 Python 项目
使用 vs code 创建 python 项目示例。

- **新建文件夹**：a_python_base ，用 vs code 打开 a_python_base
- **配置解释器**：按 Ctrl+Shift+P 搜索 Python: Select Interpreter，选择虚拟环境（.venv）下的 Python 解释器。
- **工作区设置**：VS Code 会在项目根目录生成 .vscode/ 文件夹，记录你的格式化工具、代码检查器等配置。

### 命名规范
遵循 Python 官方（PEP 8）和现代框架的惯例：

- **包与模块（文件夹与 .py 文件）**：使用 全小写+下划线（snake_case），例如 user_service.py 或 auth_utils/。
- **类名**：使用 大驼峰（PascalCase），例如 UserModel。
- **函数与变量**：使用 全小写+下划线（snake_case），例如 get_current_user()。
- **常量**：使用 全大写+下划线，例如 MAX_RETRY_COUNT。

### 项目结构示例

```text
a_python_base/                  # 项目根目录
    ├── .venv/                  # 虚拟环境（禁止提交到 Git）
    ├── .env                    # 环境变量配置
    ├── .gitignore              # 忽略文件配置
    ├── requirements.txt        # 依赖清单
    ├── app/                    # 核心代码包
    │   ├── __init__.py         # 使 app 成为一个包
    │   ├── main.py             # 程序入口
    │   ├── models.py           # 数据模型（如 Pydantic 模型）
    │   └── database.py         # 数据库逻辑
    ├── tests/                  # 测试包
    │   ├── __init__.py
    │   └── test_main.py        # 针对 main.py 的测试用例
    └── README.md               # 项目使用说明
```

- Python 通过文件夹中的 ``__init__.py`` 文件来识别包结构：
    - **根包模式**：将核心代码放在一个主文件夹内（如 app/ 或 src/），避免项目根目录过于混乱。
    - **相对导入**：在包内部，使用 from . import models 显式的相对导入，增加代码的可移植性。
    - **路径发现**：pytest 等工具会自动将当前目录加入 sys.path，以便在测试时能够正确找到包路径。

- 操作建议：
    - **代码分离**：不要把所有代码都写在 main.py。随着项目增大，应利用 APIRouter 等工具将逻辑拆分到不同模块。
    - **配置分离**：使用 pydantic-settings 库将环境变量自动加载到 Python 对象中，实现“配置即代码”。
    - **测试先行**：在 tests/ 下为每个功能模块编写测试脚本，通过在终端输入 pytest 一键运行所有测试。






