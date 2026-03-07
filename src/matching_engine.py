import os
import json
import pandas as pd
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv

load_dotenv()

# --- 1. UPDATED PYDANTIC SCHEMA (Screenshot 4: Recommendation + Transparency Layer) ---
class ProductMatch(BaseModel):
    product_id: str = Field(description="The ID of the product.")
    score: int = Field(description="Match score out of 10.")
    hard_matches_summary: str = Field(description="Summary of how it meets strict specs (e.g., budget, RAM).")
    soft_matches_summary: str = Field(description="Summary of how it meets subjective needs based on reviews/specs.")
    trade_offs: str = Field(description="Explicit trade-offs the user is making by choosing this product.")
    unmet_needs: str = Field(description="What requested features are missing from this product.")
    is_alternative: bool = Field(default=False, description="True if it exceeds the original budget constraint.")

class MatchResponse(BaseModel):
    matches: List[ProductMatch] = Field(description="List of evaluated products.")

def match_products(extracted_intent: dict, catalog_path: str = "data/product_catalog.csv", profile_path: str = "data/user_profile.json") -> dict:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    # Load Catalog
    try:
        df = pd.read_csv(catalog_path)
    except FileNotFoundError:
        return {"status": "error", "message": "Catalog not found."}

    # --- NEW: LOAD USER PROFILE (Screenshot 3: Data) ---
    user_context = ""
    try:
        with open(profile_path, "r") as f:
            profile = json.load(f)
            user_context = f"User Profile Context: Age {profile.get('age')}, Tags: {', '.join(profile.get('context_tags', []))}, Past Purchases: {', '.join(profile.get('product_history', []))}."
    except FileNotFoundError:
        user_context = "No historical user context available."

    # --- HARD FILTERING ---
    budget = extracted_intent.get("max_budget_inr")
    if budget:
        df_filtered = df[df['price_inr'] <= budget]
    else:
        df_filtered = df.copy()

    # --- GAP DETECTION & FALLBACK ---
    fallback_mode = False
    if df_filtered.empty:
        fallback_mode = True
        df_filtered = df.copy() 
        
    # --- SOFT MATCHING (LLM Reasoning) ---
    products_json = df_filtered.to_dict(orient="records")
    products_str = json.dumps(products_json, indent=2)
    soft_prefs = extracted_intent.get("soft_preferences", [])

    # Inject the user_context into the prompt
    prompt = f"""
    You are an expert AI matching engine. 
    {user_context}
    
    The user's specific soft preferences for this search are: {soft_prefs}.
    Available Products:
    {products_str}
    
    Evaluate the catalog. Break down the hard matches, soft matches, explicit trade-offs, and unmet needs for each product. 
    """
    
    if fallback_mode:
        prompt += f"\nCRITICAL: The user wanted a budget of ₹{budget}, but no products exist. Set 'is_alternative' to true, and explain the price trade-off."

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=MatchResponse,
            temperature=0.2 
        )
    )

    llm_result = json.loads(response.text)
    
    # --- COMBINE RESULTS ---
    final_matches = []
    for match in llm_result.get("matches", []):
        prod_row = df_filtered[df_filtered['product_id'] == match['product_id']]
        if not prod_row.empty:
            prod_info = prod_row.iloc[0].to_dict()
            prod_info['match_score'] = match['score']
            prod_info['hard_matches'] = match['hard_matches_summary']
            prod_info['soft_matches'] = match['soft_matches_summary']
            prod_info['trade_offs'] = match['trade_offs']
            prod_info['unmet_needs'] = match['unmet_needs']
            prod_info['is_alternative'] = match['is_alternative']
            final_matches.append(prod_info)
            
    final_matches = sorted(final_matches, key=lambda x: x['match_score'], reverse=True)
    status = "alternatives_found" if fallback_mode else "success"
    return {"status": status, "matches": final_matches}