import os
import json
from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# 1. Define the Pydantic Schema
class UserIntent(BaseModel):
    max_budget_inr: Optional[int] = Field(None, description="The maximum budget in INR mentioned by the user.")
    hard_constraints: List[str] = Field(default_factory=list, description="Strict technical requirements, e.g., '16GB RAM', 'Intel i5'.")
    soft_preferences: List[str] = Field(default_factory=list, description="Subjective or vague needs, e.g., 'lightweight', 'good for coding', 'battery backup'.")

def extract_intent(user_query: str) -> dict:
    """
    Passes the user query to Gemini and forces it to return a JSON 
    matching the UserIntent Pydantic schema using the new SDK.
    """
    # Initialize the new GenAI client
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    
    prompt = f"""
    You are an expert product recommendation assistant.
    Analyze the following user query and extract the constraints.
    Separate them into a maximum budget (in INR), strict hard constraints (like RAM, processor), 
    and soft subjective preferences (like weight, use cases).
    
    User Query: "{user_query}"
    """
    
    # Generate content using the new syntax
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=UserIntent,
            temperature=0.1
        )
    )
    
    # Parse the returned JSON string into a Python dictionary
    return json.loads(response.text)

# --- Testing the Module ---
if __name__ == "__main__":
    sample_query = "Looking for a lightweight laptop under ₹30k, good for coding and battery backup"
    print(f"User Query: {sample_query}\n")
    
    try:
        extracted_data = extract_intent(sample_query)
        print("✅ Extracted Intent (JSON):")
        print(json.dumps(extracted_data, indent=4))
    except Exception as e:
        print(f"❌ Error: {e}")