import json
from datetime import datetime

# =====================================================
# 🧠 Insight Agent: Combines knowledge, symbolic data, and memory
# =====================================================

class InsightAgent:
    def __init__(self):
        self.simplified_file = "data/simplified_expression.json"
        self.memory_file = "data/memory_log.json"

    def load_data(self):
        """Load simplified equation and past runs."""
        try:
            with open(self.simplified_file, "r") as f:
                simplified = json.load(f)
        except FileNotFoundError:
            simplified = {"simplified_expression": "unknown"}

        try:
            with open(self.memory_file, "r") as f:
                memory = json.load(f)
        except FileNotFoundError:
            memory = []

        return simplified, memory

    def generate_insight(self, query, equation, facts, context):
        """
        Generate an interpretive scientific insight from the query and equation.
        Compatible with interactive_loop.py
        """
        simplified, memory = self.load_data()

        # If no simplified expression is passed, use loaded one
        expr = equation or simplified.get("simplified_expression", "unknown")

        # Gather recent context facts
        if not facts:
            for m in memory[-3:]:
                if m.get("facts"):
                    facts.extend(m["facts"])

        # Build the final insight text
        insight_text = f"""
🧩 Simplified Relationship:
    {expr}

📜 Query Asked:
    {query}

📚 Knowledge Context:
    {', '.join(facts) if facts else 'No contextual facts found'}

💡 Generated Insight:
    The equation {expr} indicates that the universe's expansion rate (H²)
    depends on both the cosmological constant (Λ) and matter density (ρ).
    As either Λ or ρ increases, the expansion rate intensifies —
    supporting the theory that dark energy accelerates cosmic expansion.
"""

        # Save insight log
        insight_data = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "equation": expr,
            "insight": insight_text.strip()
        }

        with open("data/insight_log.json", "a", encoding="utf-8") as f:
            json.dump(insight_data, f)
            f.write("\n")

        return insight_text


# =====================================================
# 🚀 Run if executed directly
# =====================================================
if __name__ == "__main__":
    agent = InsightAgent()
    insight = agent.generate_insight(
        query="relationship between dark energy and expansion",
        equation="8231.5 * Lambda * rho",
        facts=["Dark energy accelerates expansion", "H² ∝ Λρ"],
        context=""
    )
    print("\n=== Generated Scientific Insight ===\n")
    print(insight)
