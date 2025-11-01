import json
from datetime import datetime
from src.insight_agent import InsightAgent

# Load previous data files
def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def main():
    print("🚀 Running Cosmosym Integrated Pipeline...\n")

    # 1️⃣ Load simplified expression
    simplified_data = load_json("data/simplified_expression.json")
    simplified_expr = simplified_data.get("simplified_expression") if simplified_data else None

    # 2️⃣ Load previous memory
    memory_data = load_json("data/memory_log.json") or []
    last_entry = memory_data[-1] if memory_data else {}

    # 3️⃣ Combine context
    query = last_entry.get("query", "cosmology expansion")
    facts = last_entry.get("facts", [])
    explanation = last_entry.get("explanation", "")
    equation = simplified_expr or "Unknown"

    # 4️⃣ Run the Insight Agent
    insight_agent = InsightAgent()
    insight = insight_agent.generate_insight(query, equation, facts, explanation)

    # 5️⃣ Save output with timestamp
    output = {
        "timestamp": datetime.now().isoformat(),
        "query": query,
        "equation": equation,
        "facts": facts,
        "explanation": explanation,
        "insight": insight
    }

    with open("data/insight_log.json", "a", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
        f.write(",\n")

    print("\n🧠 New Insight Generated:")
    print(insight)
    print("\n✅ Insight saved to data/insight_log.json")

if __name__ == "__main__":
    main()
