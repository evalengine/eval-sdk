from pydantic import BaseModel, Field
from typing import Optional

class TweetPair(BaseModel):
    input_tweet: str
    output_tweet: str

class ScoreDetail(BaseModel):
    score: float = Field(..., ge=0, le=100)
    rationale: str

class EvalResponse(BaseModel):
    original_tweet: str
    responded_tweet: str
    truth: ScoreDetail
    accuracy: ScoreDetail
    creativity: ScoreDetail
    engagement: ScoreDetail
    final_score: float
    recommended_response: Optional[str] = None