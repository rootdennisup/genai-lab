from pydantic import BaseModel

class LLMMessage(BaseModel):
    role: str
    content: str
    
    
class LLMRequest(BaseModel):
    messages: list[LLMMessage]
    model: str
    temperature: float = 0.7
    
    
class LLMResponse(BaseModel):
    content: str
    model: str