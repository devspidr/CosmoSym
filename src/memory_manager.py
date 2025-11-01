# ============================================================
# memory_manager.py — Handles short-term and long-term storage
# ============================================================

import json
import os
from datetime import datetime


class MemoryManager:
    def __init__(self, path="memory.json"):
        self.path = path
        self.memory = self.load_memory()

    # -----------------------------------------
    def load_memory(self):
        """Load memory from disk."""
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    # -----------------------------------------
    def save_memory(self):
        """Persist memory to disk."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self.memory, f, indent=2, ensure_ascii=False)

    # -----------------------------------------
    def add_entry(self, query, facts, equation_result, explanation):
        """Add a new entry to memory."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "query": query or "",
            "facts": facts or [],
            "equation_result": str(equation_result) if equation_result else "None",
            "explanation": explanation or "",
        }
        self.memory.append(entry)
        self.save_memory()

    # -----------------------------------------
    def search_memory(self, query):
        """Search memory for entries related to a query."""
        if not query:
            return []

        query_lower = query.lower()
        results = []
        for m in self.memory:
            text = f"{m.get('query', '')} {m.get('explanation', '')}".lower()
            if any(q in text for q in query_lower.split()):
                results.append(m)
        return results
