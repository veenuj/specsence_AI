import pandas as pd
import json
import os

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

def generate_catalog():
    # Mocking a structured laptop catalog WITH availability and offers
    data = {
        "product_id": ["L1", "L2", "L3", "L4", "L5"],
        "name": [
            "Acer Aspire Lite", 
            "MacBook Air M1", 
            "Lenovo IdeaPad Slim 3", 
            "ASUS ROG Strix", 
            "HP Pavilion Aero"
        ],
        "category": ["Laptop", "Laptop", "Laptop", "Laptop", "Laptop"],
        "price_inr": [28000, 75000, 32000, 110000, 65000],
        "weight_kg": [1.7, 1.29, 1.6, 2.5, 0.97],
        "battery_life_hours": [6, 15, 8, 4, 10],
        "ram_gb": [8, 8, 8, 16, 16],
        "processor": ["Intel i3", "Apple M1", "Intel i3", "AMD Ryzen 9", "AMD Ryzen 7"],
        "description": [
            "A budget-friendly laptop for basic everyday tasks.",
            "Incredibly thin and light with unmatched battery life.",
            "Reliable everyday performer with a decent screen.",
            "Heavy-duty gaming beast with RGB and top-tier cooling.",
            "Ultra-lightweight champion, perfect for frequent travelers."
        ],
        "review_snippets": [
            "Keyboard is a bit mushy. Good for the price.",
            "Best battery ever. Screen is gorgeous.",
            "Gets the job done, but battery drains fast if watching videos.",
            "Runs every game perfectly, but it's very heavy to carry.",
            "So light I forget it's in my bag! Fast performance."
        ],
        # --- NEW COLUMNS FOR STEP 6 ENRICHMENT ---
        "availability_status": [
            "In Stock", 
            "Only 2 left in stock!", 
            "In Stock", 
            "Out of Stock soon", 
            "In Stock"
        ],
        "current_offers": [
            "5% Cashback on ICICI Credit Cards",
            "No Cost EMI starting at ₹3,500/mo",
            "Free laptop bag included",
            "₹5,000 instant discount on HDFC cards",
            "10% off for Students"
        ]
    }
    
    df = pd.DataFrame(data)
    df.to_csv("data/product_catalog.csv", index=False)
    print("✅ product_catalog.csv generated with Enrichment Data (Availability & Offers)")

def generate_user_profile():
    # Mocking a user profile with context tags
    profile = {
        "user_id": "U001",
        "age": 28,
        "base_budget": 40000,
        "context_tags": ["student", "frequent traveler", "loves movies"],
        "product_history": ["purchased wireless mouse", "purchased laptop sleeve"]
    }
    
    with open("data/user_profile.json", "w") as f:
        json.dump(profile, f, indent=4)
    print("✅ user_profile.json generated in /data")

if __name__ == "__main__":
    generate_catalog()
    generate_user_profile()