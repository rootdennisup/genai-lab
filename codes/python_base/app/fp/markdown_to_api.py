import json
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field, ValidationError
from fastapi import FastAPI, HTTPException

# ==========================================
# 1. 数据建模 (Pydantic + 类型提示)
# 定义 Markdown 块的“契约”，充当运行时的“门卫” 
# ==========================================
class MarkdownChunk(BaseModel):
    chunk_id: int
    content: str = Field(..., min_length=1, description="段落内容")
    char_count: int = Field(..., ge=0)
    tag: str = "paragraph"

class DocumentSchema(BaseModel):
    filename: str
    chunks: List[MarkdownChunk]

# ==========================================
# 2. 核心逻辑 (pathlib + 列表推导式)
# 实现数据的“读取 -> 切分 -> 封装”流程
# ==========================================
def parse_markdown_file(file_path: Path) -> List[dict]:
    # 使用 pathlib 的对象化接口读取内容，确保跨平台兼容性
    if not file_path.exists():
        raise FileNotFoundError(f"未找到文件: {file_path}")
    
    # 推荐使用 utf-8 编码读取文本
    raw_text = file_path.read_text(encoding="utf-8")
    
    # 利用列表推导式高效处理数据
    # 逻辑：按双换行切分段落 -> 清洗空白 -> 转换为字典
    paragraphs = [p.strip() for p in raw_text.split("\n\n") if p.strip()]
    
    return [
        {
            "chunk_id": i,
            "content": text,
            "char_count": len(text)
        }
        for i, text in enumerate(paragraphs)
    ]

# ==========================================
# 3. 数据持久化 (json 模块)
# 将内存中的数据保存到磁盘，实现持久化存储
# ==========================================
def export_to_json(data: dict, output_path: Path):
    with output_path.open("w", encoding="utf-8") as f:
        # 使用标准库 json 模块保存结构化数据 [10]
        json.dump(data, f, ensure_ascii=False, indent=4)

# ==========================================
# 4. Web 接口发布 (FastAPI)
# 声明式驱动：通过一次声明获得校验、转换和文档功能
# ==========================================
app = FastAPI(title="Markdown 解析引擎")

@app.get("/process-doc/", response_model=DocumentSchema)
async def process_document(file_name: str = "sample.md"):
    # 模拟项目根路径定位 [7]
    base_path = Path(__file__).resolve().parent
    input_file = base_path / file_name
    output_file = base_path / "output.json"

    try:
        # 步骤 1: 解析
        raw_data_list = parse_markdown_file(input_file)
        
        # 步骤 2: 校验 (利用 Pydantic 强制转换和验证)
        validated_chunks = [MarkdownChunk(**item) for item in raw_data_list]
        
        full_doc = {
            "filename": file_name,
            "chunks": validated_chunks
        }
        
        # 步骤 3: 持久化
        export_to_json(full_doc, output_file)
        
        # FastAPI 自动完成响应序列化 (Python -> JSON) 
        return full_doc

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"数据校验失败: {e.errors()}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="服务器内部逻辑故障")
