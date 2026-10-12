from pydantic import BaseModel, Field
class ChatRequest(BaseModel):
    question: str = Field(min_length=1)
    model: str = "gpt-4o"
    max_tokens: int = Field(default=500, gt=0, le=4000)

class ChatResponse(BaseModel):
    model: str
    answer: str
    tokens_used: int