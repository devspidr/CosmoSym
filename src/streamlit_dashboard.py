import streamlit as st
import json
import os
from datetime import datetime
from insight_agent import InsightAgent

# =====================================================
# 🌌 COSMOSYM: Streamlit Dashboard with Interactive Q&A
# =====================================================

st.set_page_config(page_title="COSMOSYM: Cosmic Symbolic AI", page_icon="🌌", layout="centered")

st.title("🌌 COSMOSYM: Cosmic Symbolic AI Dashboard")
st.markdown("A scientific dashboard showing symbolic regression insights about the universe’s expansion.")

insight_file = "data/insight_log.json"
agent = InsightAgent()

# =====================================================
# 🧩 Utility: Load latest valid insight
# =====================================================
def load_latest_insight():
    if not os.path.exists(insight_file):
        return None
    with open(insight_file, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        return None
    for line in reversed(lines):
        try:
            return json.loads(line)
        except json.JSONDecodeError:
            continue
    return None


# =====================================================
# 🧠 Section 1: Show Latest Insight
# =====================================================
st.subheader("🧠 Latest Insight")

latest = load_latest_insight()

if latest:
    st.write(f"**🕒 Timestamp:** {latest.get('timestamp', 'N/A')}")
    if "query" in latest:
        st.write(f"**🔭 Query:** {latest['query']}")
    st.write(f"**📈 Equation:** {latest.get('equation', 'Unknown')}")
    st.markdown("### 💡 Generated Insight")
    st.write(latest.get("insight", "No insight found."))
else:
    st.warning("Dataset not found. Run `symbolic_engine.py` to generate data.")


# =====================================================
# 🧑‍🚀 Section 2: Ask a New Scientific Question
# =====================================================
st.markdown("---")
st.subheader("🧑‍🚀 Ask a New Question to the AI")

user_query = st.text_input("Enter your scientific question (e.g., *What happens if dark energy triples?*)")

if st.button("✨ Generate New Insight"):
    if not user_query.strip():
        st.error("Please enter a question first.")
    else:
        # Generate a new AI insight
        simplified, _ = agent.load_data()
        expr = simplified.get("simplified_expression", "unknown")

        insight_text = f"""
🧩 Simplified Relationship:
    {expr}

🧠 Query Asked:
    {user_query}

💡 Generated Insight:
    The equation {expr} suggests that cosmic expansion depends on both Λ (dark energy) and ρ (matter density).
    If {user_query.lower()}, this implies a proportional change in expansion rate,
    reinforcing the relationship between dark energy and universal acceleration.
"""
        # Save it to log
        new_entry = {
            "timestamp": datetime.now().isoformat(),
            "query": user_query,
            "equation": expr,
            "insight": insight_text.strip(),
        }
        with open(insight_file, "a", encoding="utf-8") as f:
            json.dump(new_entry, f)
            f.write("\n")

        st.success("✅ New insight generated and saved!")
        st.markdown("### 🧩 New Insight Generated:")
        st.write(insight_text)


# =====================================================
# 🚀 Footer
# =====================================================
st.markdown("---")
st.caption("🚀 COSMOSYM — AI-driven symbolic cosmology research framework")
