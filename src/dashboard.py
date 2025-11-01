import json
from pathlib import Path

def show_latest_insight():
    file_path = Path("data/insight_log.json")

    if not file_path.exists():
        print("⚠️ No insights found yet. Run interactive_loop.py first.")
        return

    try:
        text = file_path.read_text(encoding="utf-8").strip()

        if not text:
            print("⚠️ The insight log is empty.")
            return

        # Detect JSON array vs newline-separated JSON
        if text.startswith("["):
            data = json.loads(text)
            latest = data[-1]
        else:
            lines = [l.strip() for l in text.splitlines() if l.strip()]
            latest = json.loads(lines[-1])

        print("\n🧠 === LATEST COSMIC INSIGHT === 🧠\n")
        print(f"🕒 Timestamp: {latest.get('timestamp', 'unknown')}")
        if 'query' in latest:
            print(f"🔭 Query: {latest['query']}")
        print(f"📈 Equation: {latest.get('equation', 'unknown')}\n")
        print(latest.get('insight', 'No insight text found.'))

    except json.JSONDecodeError as e:
        print(f"❌ JSON decoding failed: {e}")
        print("Please check that data/insight_log.json is properly formatted.")

if __name__ == "__main__":
    show_latest_insight()
