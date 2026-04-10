from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from backend.models.models import Listing
import os

class TrustState(TypedDict):
    listings: List[Listing]
    flagged: List[dict]

def analyze_listing(state: TrustState):
    try:
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, api_key=os.getenv("OPENAI_API_KEY"))
        prompt = ChatPromptTemplate.from_template("""
        Analyze this listing for potential scams or trust issues.
        
        Listing details:
        - Rent: {rent}
        - Deposit: {deposit}
        - Location: {location}
        - Description: {description}
        - Trust score: {trust_score}
        
        Flag as "High Risk" if:
        - Rent is unrealistically low for the area
        - Deposit is unusually high
        - Description is vague or suspicious
        
        Otherwise, mark as "Verified Safe".
        
        Provide only: "High Risk" or "Verified Safe"
        """)
        
        chain = prompt | llm | StrOutputParser()
        
        flagged = []
        for listing in state['listings']:
            result = chain.invoke({
                "rent": listing.rent,
                "deposit": listing.deposit,
                "location": listing.location,
                "description": listing.description,
                "trust_score": listing.trust_score
            })
            flagged.append({"listing_id": listing.id, "flag": result})
        
        return {"flagged": flagged}
    except Exception as e:
        print(f"Trust analysis failed: {e}. Using simple rules.")
        # Fallback: simple rules
        flagged = []
        for listing in state['listings']:
            flag = "Verified Safe"
            if listing.rent < 4000 or listing.deposit > 50000:
                flag = "High Risk"
            flagged.append({"listing_id": listing.id, "flag": flag})
        return {"flagged": flagged}

def create_trust_graph():
    workflow = StateGraph(TrustState)
    workflow.add_node("analyze", analyze_listing)
    workflow.add_edge("analyze", END)
    workflow.set_entry_point("analyze")
    return workflow.compile()

trust_agent = create_trust_graph()