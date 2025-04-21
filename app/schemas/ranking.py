from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RankRequest(BaseModel):
    resume_text: str
    job_description: str
    photo_base64: Optional[str] = None

class RankResponse(BaseModel):
    id: int
    score: int
    feedback: str
    photo_check: Optional[str]
    created_at: datetime

class RankingOut(RankResponse):
    resume_text: str
    job_description: str

class RankingFilter(BaseModel):
    min_score: Optional[int] = None
    search: Optional[str] = None
    page: int = 1
    per_page: int = 10
