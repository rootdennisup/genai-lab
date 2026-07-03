import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError
from fastapi import FastAPI, HTTPException, Depends

## 智能文档处理与检索系统

# ==========================================
# 1. 数据建模 (Pydantic + 类型提示)
# 定义文档块的“形状”，实现声明式驱动 [2, 3]
# ==========================================
class DocChunk(BaseModel):
    id: int
    content: str = Field(..., min_length=5, description="段落内容")
    tag: str = "Uncategorized"

class DocResponse(BaseModel):
    filename: str
    total_chunks: int
    data: List[DocChunk]

# ==========================================
# 2. 核心逻辑 (容器 + 列表推导式)
# 模拟将原始 Markdown/TXT 按段落切分并封装 [1, 4]
# ==========================================
def process_raw_text(raw_text: str) -> List[dict]:
    # 使用列表推导式快速清洗和封装数据
    # 过滤掉空行，并将每一段封装成字典格式 [4, 5]
    lines = [line.strip() for line in raw_text.split("\n") if line.strip()]
    return [{"id": i, "content": text} for i, text in enumerate(lines)]

# ==========================================
# 3. 资源管理 (生成器 + Depends)
# 模拟数据库或文件流的开启与关闭 [6, 7]
# ==========================================
async def get_db_session():
    print(">>> 开启资源：数据库连接已建立")
    try:
        yield "DB_SESSION_ACTIVE"
    finally:
        # 确保即使 API 出错也能安全释放资源 [7, 8]
        print(">>> 释放资源：数据库连接已关闭")

# ==========================================
# 4. Web 接口 (FastAPI + 异常处理)
# 整合所有逻辑，提供健壮的服务 [9-11]
# ==========================================
app = FastAPI(title="智能文档系统")

@app.post("/upload/", response_model=DocResponse)
async def upload_document(filename: str, content: str, db=Depends(get_db_session)):
    try:
        # 执行核心转换逻辑
        raw_chunks = process_raw_text(content)
        
        # 利用 Pydantic 执行批量校验和强制类型转换 [12, 13]
        validated_chunks = [DocChunk(**item) for item in raw_chunks]
        
        if not validated_chunks:
            # 主动触发业务异常 [10, 14]
            raise ValueError("文档内容不能为空")
            
        return {
            "filename": filename,
            "total_chunks": len(validated_chunks),
            "data": validated_chunks
        }
        
    except ValidationError as e:
        # 拦截数据验证错误
        raise HTTPException(status_code=422, detail=f"文档结构非法: {e.errors()}")
    except ValueError as e:
        # 拦截业务逻辑错误
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # 拦截未知的系统崩溃
        raise HTTPException(status_code=500, detail="服务器内部逻辑故障")




