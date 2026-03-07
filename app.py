import streamlit as st
import sys
import os
import json

# Add src folder to the system path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from intent_extractor import extract_intent
from matching_engine import match_products

# --- Page Configuration ---
st.set_page_config(
    page_title="SpecSense AI", 
    page_icon="🛍️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom CSS for Premium Look ---
st.markdown("""
    <style>
    .premium-title {
        font-size: 3.5rem !important;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #4A00E0, #8E2DE2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding-bottom: 5px;
        margin-bottom: 0px;
    }
    .premium-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #6c757d;
        margin-bottom: 40px;
        font-weight: 500;
    }
    .spec-tag {
        display: inline-block;
        background-color: #f1f3f5;
        color: #495057;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 8px;
        border: 1px solid #dee2e6;
    }
    .price-tag {
        color: #2b8a3e;
        font-weight: 800;
        font-size: 1.6rem;
        margin-bottom: 10px;
    }
    .stTextInput input {
        padding: 15px;
        font-size: 1.1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown('<div class="premium-title">SpecSense AI</div>', unsafe_allow_html=True)
st.markdown('<div class="premium-subtitle">Intelligent Product Matching Powered by Generative AI</div>', unsafe_allow_html=True)

# --- Search Bar Section ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    user_query = st.text_input(
        "What exactly are you looking for?", 
        placeholder="e.g., An ultra-light laptop under ₹80k, good for coding and travel...",
        label_visibility="collapsed" 
    )
    
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
    with btn_col2:
        submit_btn = st.button("✨ Find My Match", type="primary", use_container_width=True)

    with st.expander("💡 Need inspiration? Copy & paste these test queries:"):
        st.markdown("**1. The 'Perfect Match' Test**")
        st.code("I have a budget of ₹80,000 and I need a laptop that is incredibly light for traveling, with a battery that lasts all day.", language="text")
        st.markdown("**2. The 'Gap Detection' Test (Impossible Ask)**")
        st.code("I really want an ultra-light laptop with amazing battery life, and my maximum budget is ₹15,000.", language="text")

st.divider()

# --- Core Application Logic with SESSION STATE ---

# 1. When the user clicks the button, save the results into memory (session state)
if submit_btn:
    if user_query:
        with st.spinner("🧠 Analyzing intent and evaluating product specs..."):
            try:
                intent = extract_intent(user_query)
                # Store data in session state so it survives the re-run
                st.session_state['intent'] = intent
                st.session_state['match_results'] = match_products(intent)
                st.session_state['current_query'] = user_query
            except Exception as e:
                st.error(f"Failed to extract intent. Error: {e}")
    else:
        st.warning("Please enter a query to get started.")

# 2. If we have results saved in memory, display them!
if 'match_results' in st.session_state:
    match_results = st.session_state['match_results']
    intent = st.session_state['intent']
    saved_query = st.session_state['current_query']

    # Transparency Layer
    with st.expander("🔍 See AI's Extracted Understanding (Data Pipeline Transparency)", expanded=False):
        st.json(intent)
        
    # Display Recommendations
    if match_results["status"] in ["success", "alternatives_found"] and match_results["matches"]:
        
        if match_results["status"] == "alternatives_found":
            st.warning("⚠️ **Strict Budget Alert:** We couldn't find an exact match for your hard constraints, but we found these highly-rated alternatives!", icon="💡")
        else:
            st.success("🎯 **Perfect Matches Found!** Here are the top recommendations based on your preferences.", icon="✅")
            
        st.write("") 

        for idx, product in enumerate(match_results["matches"]):
            with st.container(border=True):
                img_col, details_col, score_col = st.columns([1, 5, 2])
                
                with img_col:
                    st.markdown("<h1 style='text-align: center; margin-top: 20px;'>💻</h1>", unsafe_allow_html=True)

                with details_col:
                    badge = " 🏷️ *(Suggested Alternative)*" if product.get('is_alternative') else ""
                    st.markdown(f"### {product['name']}{badge}")
                    st.markdown(f"<div class='price-tag'>₹{product['price_inr']:,}</div>", unsafe_allow_html=True)
                    
                    specs_html = f"""
                    <div>
                        <span class='spec-tag'>⚖️ {product['weight_kg']} kg</span>
                        <span class='spec-tag'>🔋 {product['battery_life_hours']} hrs</span>
                        <span class='spec-tag'>🧠 {product['ram_gb']}GB RAM</span>
                        <span class='spec-tag'>⚙️ {product['processor']}</span>
                    </div>
                    """
                    st.markdown(specs_html, unsafe_allow_html=True)
                    
                    st.markdown(f"📦 **Availability:** `{product.get('availability_status', 'Check website')}` | 🎁 **Offer:** `{product.get('current_offers', 'No active offers')}`")
                    st.write("") 
                    
                    st.markdown("**🔍 AI Matching Rationale:**")
                    st.success(f"**✅ Hard Matches:** {product.get('hard_matches', 'N/A')}")
                    st.info(f"**✨ Soft Matches:** {product.get('soft_matches', 'N/A')}")
                    st.warning(f"**⚖️ Trade-offs:** {product.get('trade_offs', 'N/A')}")
                    
                    if product.get('unmet_needs') and product.get('unmet_needs').lower() not in ["none", "n/a", "null", ""]:
                        st.error(f"**❌ Unmet Needs:** {product['unmet_needs']}")
                        
                    st.caption(f"💬 *Real User Review: \"{product.get('review_snippets', '')}\"*")
                    
                with score_col:
                    score = product.get('match_score', 0)
                    if score >= 8:
                        score_color = "#2b8a3e" 
                    elif score >= 5:
                        score_color = "#f59f00" 
                    else:
                        score_color = "#c92a2a" 
                        
                    st.markdown("<div style='text-align: center; font-weight: bold; color: #6c757d; margin-top: 10px;'>Match Score</div>", unsafe_allow_html=True)
                    st.markdown(f"<h1 style='text-align: center; color: {score_color}; margin-top: -15px; font-size: 3rem;'>{score}/10</h1>", unsafe_allow_html=True)
                    st.progress(score / 10.0)
                    
                    # --- FIXED Evaluation Layer ---
                    st.write("")
                    st.markdown("<div style='text-align: center; font-size: 0.8rem; color: #6c757d;'>Rate this recommendation:</div>", unsafe_allow_html=True)
                    
                    feedback = st.feedback("thumbs", key=f"feedback_{product.get('product_id', idx)}_{idx}")
                    if feedback is not None:
                        feedback_data = {
                            "query": saved_query,
                            "product_recommended": product['name'],
                            "ai_score": score,
                            "user_rating": "Thumbs Up" if feedback == 1 else "Thumbs Down"
                        }
                        
                        os.makedirs("data", exist_ok=True)
                        with open("data/evaluation_tracking.jsonl", "a") as f:
                            f.write(json.dumps(feedback_data) + "\n")
                            
                        st.toast("Feedback recorded for continuous improvement! 📈")
                    
    elif match_results["status"] == "no_hard_matches":
        st.error("⚠️ No products perfectly matched your strict constraints, and the fallback logic failed. Try relaxing your requirements!")
    else:
        st.error(match_results.get("message", "An unexpected error occurred."))