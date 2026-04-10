from pydantic import BaseModel
from typing import List, Optional

class Listing(BaseModel):
    id: int
    location: str
    rent: int
    deposit: int
    num_roommates: int
    vacancy_count: int
    lifestyle_tags: str
    contact_info: str
    urgency: str
    trust_score: int
    description: str

class UserProfile(BaseModel):
    id: int
    name: str
    email: str
    linkedin: Optional[str] = None
    work_email: Optional[str] = None
    id_verified: bool = False
    trust_score: int = 0
    preferences: dict = {}

class MatchRequest(BaseModel):
    budget: int
    lifestyle: str
    urgency: str
    location: Optional[str] = None

class MatchResult(BaseModel):
    listing: Listing
    score: float
    explanation: str