from pydantic import BaseModel
from typing import List, Optional, Any

class ChatRequest(BaseModel):
    user_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    type: str   # "FAQ" | "RECOMMENDATION" | "COMPARISON"
    answer: str
    plans: Optional[List[dict]] = None

class CompareRequest(BaseModel):
    user_id: Optional[str] = None
    message: str
    plan_ids: List[int]

class RecommendRequest(BaseModel):
    user_id: Optional[str] = None
    message: str
    max_results: int = 5

class FAQRequest(BaseModel):
    user_id: Optional[str] = None
    message: str