print("🚀 MAIN STARTING")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .models import ChatRequest, ChatResponse, RecommendRequest, CompareRequest, FAQRequest
from .services.intent_service import classify_intent
from .services.recommend_service import handle_recommendation
from .services.generic_handler import handle_generic
from .services.compare_service import handle_comparison
from .services.faq_service import handle_faq
from .services.plan_service import get_all_plans_categorized

print("🚀 app created")

app = FastAPI(title="Telco AI Recommender",debug=True)

# Allow Open-WebUI (and others) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "Telco AI Recommender API is running."
    }
    
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    intent = classify_intent(req.message)
    if intent == "RECOMMENDATION":
        result = handle_recommendation(req.message)
    else:
        result = handle_generic(req.message)
    # elif intent == "COMPARISON":
    #     # naive: extract ids from text later; for now just FAQ fallback
    #     result = handle_faq(req.message)
    #     result["type"] = "FAQ"
    # else:
    #     result = handle_faq(req.message)

    return ChatResponse(**result)

@app.get("/plans")
def get_plans():
    """
    Get all active telco plans grouped by market categories
    """
    return get_all_plans_categorized()


# @app.post("/recommend", response_model=ChatResponse)
# def recommend(req: RecommendRequest):
#     result = handle_recommendation(req.message, max_results=req.max_results)
#     return ChatResponse(**result)

# @app.post("/compare", response_model=ChatResponse)
# def compare(req: CompareRequest):
#     result = handle_comparison(req.message, req.plan_ids)
#     return ChatResponse(**result)

# @app.post("/faq", response_model=ChatResponse)
# def faq(req: FAQRequest):
#     result = handle_faq(req.message)
#     return ChatResponse(**result)