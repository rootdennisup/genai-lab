from app.llm_runtime.models import LLMMessage


class PromptBuilder:
    """负责把业务输入组装成大模型 messages。"""
    
    def build_chat_messages(
        self,
        user_message: str,
        persona: str | None = None,
    ) -> list[LLMMessage]:
        system_prompt = self._build_system_prompt(persona)
        
        return [
            LLMMessage(role="system", content=system_prompt),
            LLMMessage(role="user", content=user_message),
        ]
    
    def _build_system_prompt(self, persona: str | None = None) -> str:
        """构建 AI-Buddy 的基础系统提示词。"""
        base_prompt = """    
你是 AI-Buddy，一个面向长期陪伴场景的 AI 伙伴。

你的目标不是只回答问题，而是在安全、真诚、克制的前提下，帮助用户：
1. 梳理想法
2. 获得情绪支持
3. 进行学习和项目练习
4. 在长期对话中逐渐形成稳定的陪伴体验

回复要求：
- 使用自然、温和、清晰的中文
- 不要假装拥有真实经历
- 不要编造用户没有说过的个人信息
- 如果用户的问题适合拆解，请分步骤说明
- 如果用户表达情绪，先共情，再给建议
- 如果用户在学习编程，请像耐心的开发指导老师一样解释
""".strip()     

        if persona:
            return f"{base_prompt}\n\n当前角色补充设定：\n{persona}"
        
        return base_prompt
        
        