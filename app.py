import streamlit as st
import sys
import os
import json

# Add src folder to the system path
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

# --- Ultra-Premium CSS (Glassmorphism & Animations) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global Typography & Background */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Subtle ambient background */
    .stApp {
        background: radial-gradient(circle at 15% 50%, rgba(99, 102, 241, 0.04), transparent 25%),
                    radial-gradient(circle at 85% 30%, rgba(236, 72, 153, 0.04), transparent 25%);
    }

    /* Hero Section */
    .hero-title {
        font-size: 4.5rem !important;
        font-weight: 800;
        background: linear-gradient(135deg, #4f46e5 0%, #c026d3 50%, #e11d48 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
        letter-spacing: -2px;
        animation: fadeInDown 0.8s ease-out;
    }

    .hero-subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #64748b;
        margin-bottom: 3.5rem;
        font-weight: 500;
        letter-spacing: -0.5px;
        animation: fadeIn 1.2s ease-out;
    }

    /* Search Input Styling */
    .stTextInput > div > div > input {
        border-radius: 16px;
        border: 2px solid rgba(226, 232, 240, 0.8);
        padding: 22px 20px;
        font-size: 1.15rem;
        box-shadow: 0 4px 20px -5px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        background: rgba(255, 255, 255, 0.9);
    }
    .stTextInput > div > div > input:focus {
        border-color: #6366f1;
        box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
    }

    /* Button Styling */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border: none;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -10px rgba(99, 102, 241, 0.5);
    }

    /* Glassmorphism Product Cards with Animation */
    .glass-card {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.4);
        border-radius: 24px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.05);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        animation: slideUp 0.6s ease-out forwards;
        opacity: 0;
        transform: translateY(20px);
    }

    .glass-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px -10px rgba(99, 102, 241, 0.15);
        border-color: rgba(99, 102, 241, 0.3);
        background: rgba(255, 255, 255, 0.85);
    }

    /* Stagger animations for cards (pseudo-selectors don't work well via injected CSS in st.container, so handled generally) */
    @keyframes slideUp {
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    /* Modern Typography inside cards */
    .product-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }
    .price-text {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #10b981, #059669);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 16px;
    }

    /* Premium Spec Pills */
    .spec-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin-bottom: 16px;
    }
    .premium-pill {
        display: inline-flex;
        align-items: center;
        padding: 6px 14px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.3px;
        box-shadow: inset 0 0 0 1px rgba(0,0,0,0.05);
    }
    .pill-weight { background: #f0f9ff; color: #0284c7; }
    .pill-battery { background: #fffbeb; color: #b45309; }
    .pill-ram { background: #f0fdf4; color: #16a34a; }
    .pill-cpu { background: #faf5ff; color: #9333ea; }

    /* Rationale & Info */
    .rationale-header {
        font-size: 0.85rem;
        font-weight: 800;
        color: #64748b;
        margin-top: 20px;
        margin-bottom: 10px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }
    .info-text {
        font-size: 0.9rem;
        color: #475569;
        display: flex;
        align-items: center;
        gap: 6px;
    }

    /* Score Styling */
    .score-container {
        text-align: center;
        padding-top: 10px;
        border-left: 1px dashed #e2e8f0;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .score-label {
        font-size: 0.8rem;
        font-weight: 800;
        color: #94a3b8;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: -5px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown('<div class="hero-title">SpecSense AI</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">The next generation of AI-driven product discovery</div>', unsafe_allow_html=True)

# --- Search Section ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    user_query = st.text_input(
        "Search Intent", 
        placeholder="Try: 'A lightweight laptop for video editing under 1 Lakh'...",
        label_visibility="collapsed"
    )
    
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
    with btn_col2:
        submit_btn = st.button("✨ Discover Matches", type="primary", use_container_width=True)

    with st.expander("💡 Power User Examples"):
        st.markdown("**Perfect Match:** `I need an ultra-light laptop under ₹80k for travel.`")
        st.markdown("**Gap Detection:** `I want a 32GB RAM laptop for ₹10,000.`")

st.divider()

# --- Logic with Session State ---
if submit_btn and user_query:
    with st.spinner("🚀 Architecting your recommendations..."):
        try:
            intent = extract_intent(user_query)
            st.session_state['intent'] = intent
            st.session_state['match_results'] = match_products(intent)
            st.session_state['current_query'] = user_query
        except Exception as e:
            st.error(f"Intelligence Error: {e}")

# --- Display Results ---
if 'match_results' in st.session_state:
    match_results = st.session_state['match_results']
    intent = st.session_state['intent']
    saved_query = st.session_state['current_query']

    with st.expander("🔍 System Trace (Pipeline Transparency)", expanded=False):
        st.json(intent)

    if match_results["status"] in ["success", "alternatives_found"] and match_results["matches"]:
        
        if match_results["status"] == "alternatives_found":
            st.warning("💡 **Gap Detection Active:** Strict constraints unmet. Showing closest technical alternatives.", icon="⚙️")
        else:
            st.success(f"🎯 Synthesized {len(match_results['matches'])} optimized matches for your profile.", icon="✨")

        for idx, product in enumerate(match_results["matches"]):
            # UI Card Implementation - Injecting animation delay inline
            st.markdown(f'<div class="glass-card" style="animation-delay: {idx * 0.15}s;">', unsafe_allow_html=True)
            
            c1, c2, c3 = st.columns([1, 5, 2])
            
            with c1:
                st.markdown("<div style='text-align: center; font-size: 5rem; margin-top: 10px; text-shadow: 0 10px 20px rgba(0,0,0,0.1);'>💻</div>", unsafe_allow_html=True)
            
            with c2:
                badge = " <span style='background: #eef2ff; color: #4f46e5; padding: 4px 10px; border-radius: 20px; font-size: 0.75rem; font-weight: 800; vertical-align: middle; margin-left: 10px;'>⚡ ALTERNATIVE</span>" if product.get('is_alternative') else ""
                st.markdown(f"<div class='product-title'>{product['name']}{badge}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='price-text'>₹{product['price_inr']:,}</div>", unsafe_allow_html=True)
                
                # Styled Spec Pills
                st.markdown(f"""
                    <div class='spec-container'>
                        <span class='premium-pill pill-weight'>⚖️ {product['weight_kg']}kg</span>
                        <span class='premium-pill pill-battery'>🔋 {product['battery_life_hours']}h Battery</span>
                        <span class='premium-pill pill-ram'>🧠 {product['ram_gb']}GB RAM</span>
                        <span class='premium-pill pill-cpu'>⚙️ {product['processor']}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                # Enrichment
                st.markdown(f"<div class='info-text'>📦 <b>Stock:</b> {product.get('availability_status', 'Available')} &nbsp;•&nbsp; 🎁 <b>Offer:</b> {product.get('current_offers', 'Standard Pricing')}</div>", unsafe_allow_html=True)
                
                # Rationale Section
                st.markdown('<div class="rationale-header">AI Rationale</div>', unsafe_allow_html=True)
                st.success(f"**Hard Matches:** {product.get('hard_matches', 'N/A')}")
                st.info(f"**Soft Matches:** {product.get('soft_matches', 'N/A')}")
                
                with st.expander("View Trade-offs & Needs"):
                    st.warning(f"**Trade-offs:** {product.get('trade_offs', 'None detected')}")
                    if product.get('unmet_needs') and product.get('unmet_needs').lower() not in ["none", "n/a", "null", ""]:
                        st.error(f"**Unmet Needs:** {product['unmet_needs']}")
                
                st.caption(f"💬 \"{product.get('review_snippets', 'No reviews available.')}\"")

            with c3:
                score = product.get('match_score', 0)
                score_color = "#10b981" if score >= 8 else "#f59e0b" if score >= 5 else "#ef4444"
                
                st.markdown(f"<div class='score-container'>", unsafe_allow_html=True)
                st.markdown(f"<div class='score-label'>Match Score</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='color: {score_color}; font-size: 4rem; font-weight: 800; line-height: 1; margin: 10px 0;'>{score}<span style='font-size: 1.8rem; color: #cbd5e1;'>/10</span></div>", unsafe_allow_html=True)
                st.progress(score / 10.0)
                
                # Feedback Tracking
                st.write("")
                st.markdown("<div style='font-size: 0.75rem; color: #94a3b8; font-weight: 600; text-transform: uppercase;'>Rate Accuracy</div>", unsafe_allow_html=True)
                feedback = st.feedback("thumbs", key=f"eval_{product.get('product_id', idx)}_{idx}")
                if feedback is not None:
                    # Log to JSONL (Evaluation Layer)
                    feedback_log = {"query": saved_query, "product": product['name'], "score": score, "rating": feedback}
                    os.makedirs("data", exist_ok=True)
                    with open("data/evaluation_tracking.jsonl", "a") as f:
                        f.write(json.dumps(feedback_log) + "\n")
                    st.toast("Evaluation data captured! 📈")
                st.markdown("</div>", unsafe_allow_html=True) # End score container

            st.markdown('</div>', unsafe_allow_html=True) # End Product Card