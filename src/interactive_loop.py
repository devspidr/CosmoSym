import os
import json
import subprocess
from datetime import datetime
from insight_agent import InsightAgent


def run_stage(command, title):
    print(f"\n⚙️  Running {title}...")
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("⚠️", result.stderr)
    print(f"✅ {title} done.\n")

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def main():
    print("🌌 Welcome to COSMOSYM Interactive Mode 🌌")
    print("Ask any cosmic or physics-based question below.\n")

    while True:
        query = input("🔭 Enter your research question (or type 'exit' to quit): ").strip()
        if query.lower() == "exit":
            print("\n🪐 Exiting COSMOSYM. See you in the next universe!")
            break

        # Step 1️⃣ Run agent_graph
        run_stage("python src/agent_graph.py", "Knowledge Graph Builder")

        # Step 2️⃣ Run symbolic_engine
        run_stage("python src/symbolic_engine.py", "Symbolic Regression Engine")

        # Step 3️⃣ Run symbolic_simplifier
        run_stage("python src/symbolic_simplifier.py", "Symbolic Simplifier")

        # Step 4️⃣ Run insight generation
        simplified_data = load_json("data/simplified_expression.json")
        simplified_expr = simplified_data.get("simplified_expression") if simplified_data else None

        insight_agent = InsightAgent()
        insight = insight_agent.generate_insight(query, simplified_expr or "unknown_equation", [], "")

        # Save results
        output = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "equation": simplified_expr,
            "insight": insight
        }

        with open("data/insight_log.json", "a", encoding="utf-8") as f:
            json.dump(output, f, indent=2)
            f.write(",\n")

        print("\n🧠 Insight Generated:")
        print(insight)
        print("\n✅ Insight saved to data/insight_log.json\n")
        print("─────────────────────────────────────────────")

if __name__ == "__main__":
    main()
