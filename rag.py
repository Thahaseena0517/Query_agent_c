# rag.py
# RAG = Retrieval Augmented Generation
# This loads our knowledge base so the agent can answer product questions

import json
import os

def load_knowledge_base() -> str:
    """Load knowledge base from JSON and convert to readable text."""
    
    kb_path = os.path.join("data", "knowledge_base.json")
    
    with open(kb_path, "r") as f:
        kb = json.load(f)
    
    # Convert JSON to a readable text format for the LLM
    text = """
=== AUTOSTREAM PRODUCT KNOWLEDGE BASE ===

PRODUCT:
- Name: AutoStream
- Description: {description}
- Key Features: {features}

PRICING PLANS:

1. BASIC PLAN
   - Price: {basic_price}
   - Videos: {basic_videos}
   - Resolution: {basic_res}
   - Features: {basic_features}

2. PRO PLAN
   - Price: {pro_price}
   - Videos: {pro_videos}
   - Resolution: {pro_res}
   - Features: {pro_features}

COMPANY POLICIES:
- Refund Policy: {refund}
- Support: {support}
- Free Trial: {trial}
""".format(
        description=kb["product"]["description"],
        features=", ".join(kb["product"]["key_features"]),
        basic_price=kb["pricing"]["basic"]["price"],
        basic_videos=kb["pricing"]["basic"]["videos"],
        basic_res=kb["pricing"]["basic"]["resolution"],
        basic_features=", ".join(kb["pricing"]["basic"]["features"]),
        pro_price=kb["pricing"]["pro"]["price"],
        pro_videos=kb["pricing"]["pro"]["videos"],
        pro_res=kb["pricing"]["pro"]["resolution"],
        pro_features=", ".join(kb["pricing"]["pro"]["features"]),
        refund=kb["policies"]["refund"],
        support=kb["policies"]["support"],
        trial=kb["policies"]["trial"]
    )
    
    return text


def get_relevant_info(user_message: str) -> str:
    """
    Simple RAG: return full knowledge base.
    In production, you'd use vector similarity search here.
    """
    return load_knowledge_base()