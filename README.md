# 🛍️ SpecSense AI: Generative AI-Powered Hybrid Recommender

![Python](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-orange?logo=google&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?logo=pandas&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-Schema%20Validation-E92063?logo=pydantic&logoColor=white)

## 📌 Overview
Traditional recommender systems rely on rigid filters and struggle with vague, natural language queries. **SpecSense AI** bridges this gap by functioning as an intelligent routing and reasoning engine. It leverages Generative AI to process free-form user preferences, strictly extracting constraints, and mapping them against structured product catalogs. 

Instead of overwhelming users with irrelevant choices or dead-end "0 results found" pages, it provides **context-aware, explainable recommendations** backed by deterministic data filtering and LLM reasoning.

## ✨ Core Features & AI Architecture

* **🧠 Natural Language Intent Extraction:** Uses **Pydantic** schema validation to force the LLM to parse messy human queries into strict JSON structures (separating hard constraints like budget from soft preferences like "good for coding").
* **⚙️ Hybrid Matching Engine:** * *Deterministic (Pandas):* Instantly filters out products that violate hard constraints (saving tokens and preventing hallucinations).
  * *Probabilistic (Gemini 2.5 Flash):* Scores remaining products out of 10 based on subjective needs and real-world review snippets.
* **🔄 Gap Detection & Fallback Logic:** If strict constraints (like an impossibly low budget) yield 0 results, the system automatically relaxes the parameters and negotiates with the user by offering the closest alternatives with explicit price trade-offs.
* **🪟 Granular Transparency Layer:** Replaces the "black box" of AI with clear explainability. Every recommendation explicitly breaks down: `Hard Matches`, `Soft Matches`, `Trade-offs`, and `Unmet Needs`.
* **📊 Evaluation & HITL Layer:** Includes a Human-in-the-Loop (HITL) feedback mechanism that tracks match quality and user satisfaction, logging results to a `.jsonl` file for continuous prompt engineering and model fine-tuning.

## 🛠️ Tech Stack
* **LLM / AI:** Google GenAI SDK (`gemini-2.5-flash`)
* **Data Processing:** Pandas (for structured catalog manipulation)
* **Validation:** Pydantic (for reliable structured outputs)
* **Frontend:** Streamlit (for a responsive, premium interactive UI)

## 🚀 Installation & Local Setup

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR_USERNAME/specsense-ai.git](https://github.com/YOUR_USERNAME/specsense-ai.git)
cd specsense-ai
```
**2. Set up the virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```
**3. Install dependencies**
```bash
pip install -r requirements.txt
```
**4. Configure API keys**
Create a `.env` file in the root directory and add your Gemini API Key:
```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```
**5. Generate the Mock Database**
```bash
python generate_mock_data.py
```
**6. Launch the Application**
```bash
streamlit run app.py
```
## 📂 Project Structure

```text
specsense_ai/
├── data/
│   ├── product_catalog.csv         # Generated structured inventory (Specs, Price, Stock)
│   ├── user_profile.json           # Mock user context for personalized grounding
│   └── evaluation_tracking.jsonl   # Auto-generated HITL feedback logs
├── src/
│   ├── intent_extractor.py         # LLM pipeline for Pydantic schema extraction
│   └── matching_engine.py          # Hybrid Pandas/LLM filtering & fallback logic
├── app.py                          # Premium Streamlit user interface
├── generate_mock_data.py           # Script to build catalog and inject real-world variables
├── requirements.txt                # Project dependencies
└── .env                            # API keys (Git ignored)
```
## 🎯 Example Queries to Test

Ready to see the AI in action? Copy and paste these directly into the Streamlit search bar to test the different "muscles" of the architecture:

> **✨ The Perfect Match** > *"I have a budget of ₹80,000 and I need a laptop that is incredibly light for traveling, with a battery that lasts all day."*

> **🛡️ The Gap Detection (Testing Guardrails)** > *"I really want an ultra-light laptop with amazing battery life, and my maximum budget is ₹15,000."* > 💡 *Notice how it triggers the fallback logic, explaining why the budget is too low and suggesting the closest alternatives instead of failing.*

> **🔮 The Vague Vibe (Testing Soft Reasoning)** > *"I want something that looks good, is super easy to carry to cafes, and won't die on me quickly. Money is not an issue."*

---

## 👨‍💻 Author & Contributing

**Developed by Anuj Dhiman** This project was built to demonstrate practical, enterprise-grade Generative AI engineering, focusing on LLM pipelines, prompt design, and hybrid recommender systems. 

**Want to contribute?** Contributions, issues, and feature requests are warmly welcome! Whether you want to optimize the Pydantic schemas, add a vector database for semantic search, or enhance the Streamlit UI:
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request