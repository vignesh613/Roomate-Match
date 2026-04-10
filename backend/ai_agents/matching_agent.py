from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
import os
from backend.db.database import db
from backend.models.models import MatchRequest, MatchResult, Listing

class MatchingState(TypedDict):
    request: MatchRequest
    candidates: List[Listing]
    matches: List[MatchResult]

def retrieve_candidates(state: MatchingState):
    if db.chroma_available:
        try:
            # Use ChromaDB for semantic search
            query = f"Looking for accommodation in {state['request'].location or 'Siruseri area'} with budget {state['request'].budget}, lifestyle {state['request'].lifestyle}, urgency {state['request'].urgency}"
            results = db.collection.query(query_texts=[query], n_results=20)
            
            candidates = []
            for metadata in results['metadatas'][0]:
                listing = Listing(
                    id=metadata['id'],
                    location=metadata['location'],
                    rent=metadata['rent'],
                    deposit=metadata['deposit'],
                    num_roommates=metadata['num_roommates'],
                    vacancy_count=metadata['vacancy_count'],
                    lifestyle_tags=metadata['lifestyle_tags'],
                    contact_info=metadata['contact_info'],
                    urgency=metadata['urgency'],
                    trust_score=metadata['trust_score'],
                    description=""  # Will be filled from Chroma
                )
                candidates.append(listing)
        except Exception as e:
            print(f"ChromaDB search failed: {e}, using all listings")
            # Fallback to all listings
            candidates = db.get_all_listings()
    else:
        # No ChromaDB, use all listings
        candidates = db.get_all_listings()
    
    return {"candidates": candidates}

def filter_candidates(state: MatchingState):
    filtered = []
    for listing in state['candidates']:
        if listing.rent <= state['request'].budget:
            if state['request'].urgency == "Immediate" and listing.urgency == "Immediate Move-in (48 hrs)":
                filtered.append(listing)
            elif state['request'].urgency == "Flexible":
                filtered.append(listing)
    return {"candidates": filtered}

def score_matches(state: MatchingState):
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
        prompt = ChatPromptTemplate.from_template("""
        Score this listing for the user request on a scale of 0-100.
        Higher scores for better matches.
        
        User request: Budget {budget}, Lifestyle {lifestyle}, Urgency {urgency}
        
        Listing: Location {location}, Rent {rent}, Lifestyle tags {tags}, Urgency {listing_urgency}, Trust score {trust}
        
        Provide only the score number.
        """)
        
        chain = prompt | llm | StrOutputParser()
        
        matches = []
        for listing in state['candidates'][:10]:  # Top 10
            score = float(chain.invoke({
                "budget": state['request'].budget,
                "lifestyle": state['request'].lifestyle,
                "urgency": state['request'].urgency,
                "location": listing.location,
                "rent": listing.rent,
                "tags": listing.lifestyle_tags,
                "listing_urgency": listing.urgency,
                "trust": listing.trust_score
            }))
            explanation = f"Score {score} based on budget fit, lifestyle match, and urgency."
            matches.append(MatchResult(listing=listing, score=score, explanation=explanation))
        
        matches.sort(key=lambda x: x.score, reverse=True)
        return {"matches": matches[:5]}  # Top 5
    except Exception as e:
        print(f"LLM scoring failed: {e}. Using simple scoring.")
        # Fallback: simple scoring based on budget and urgency
        matches = []
        for listing in state['candidates'][:10]:
            score = 50  # Base score
            if listing.rent <= state['request'].budget:
                score += 30
            if state['request'].urgency == "Immediate" and listing.urgency == "Immediate Move-in (48 hrs)":
                score += 20
            elif state['request'].urgency == "Flexible":
                score += 10
            explanation = f"Simple score {score} based on budget and urgency."
            matches.append(MatchResult(listing=listing, score=score, explanation=explanation))
        matches.sort(key=lambda x: x.score, reverse=True)
        return {"matches": matches[:5]}

def create_matching_graph():
    workflow = StateGraph(MatchingState)
    workflow.add_node("retrieve", retrieve_candidates)
    workflow.add_node("filter", filter_candidates)
    workflow.add_node("score", score_matches)
    
    workflow.add_edge("retrieve", "filter")
    workflow.add_edge("filter", "score")
    workflow.add_edge("score", END)
    
    workflow.set_entry_point("retrieve")
    return workflow.compile()

matching_agent = create_matching_graph()