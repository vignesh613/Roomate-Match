from fastapi import APIRouter, HTTPException
from backend.models.models import Listing, MatchRequest
from backend.db.database import db
from backend.ai_agents.matching_agent import matching_agent
from backend.ai_agents.trust_agent import trust_agent
from typing import List
import os

router = APIRouter()

@router.get("/listings")
async def get_listings():
    return db.get_all_listings()

@router.post("/listings")
async def add_listing(listing: Listing):
    db.add_listing(listing)
    return {"message": "Listing added successfully"}

@router.post("/match")
async def find_matches(request: MatchRequest):
    result = matching_agent.invoke({"request": request, "candidates": [], "matches": []})
    return result["matches"]

@router.post("/check-trust")
async def check_trust(listings: List[Listing]):
    result = trust_agent.invoke({"listings": listings, "flagged": []})
    return result["flagged"]