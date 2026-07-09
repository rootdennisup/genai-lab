from pydantic import BaseModel,Field

class ChatRequest(BaseModel):
    user_id: str = Field(default="user_id_001",description="用户ID")
    chat_id: str | None = Field(default=None,description="对话ID") 
    message: str = Field(...,min_length=1, description="用户输入对话")
    persona: str |None = Field(default=None,description="可选角色设定")


class ChatResponse(BaseModel):
    chat_id: str
    reply:str
    model:str
