# ============================================================
# agentic_core.py — Core Agents for Cosmosym
# ============================================================

from sympy import symbols, Eq, solve, pi
from sentence_transformers import SentenceTransformer
from memory_manager import MemoryManager

# ============================================================
# 🔢 Symbolic Agent — Handles Cosmology Equations
# ============================================================
class SymbolicAgent:
    def __init__(self):
        self.model_name = "all-MiniLM-L6-v2"
        self.embedding = SentenceTransformer(self.model_name)

    def evaluate(self, G_value, rho_value, Lambda_value):
        """Compute simplified Friedmann-like relation."""
        try:
            G, rho, Lambda = symbols('G rho Lambda')
            H = symbols('H')

            # Simplified Friedmann equation: H² = (8πGρ)/3 + (Λc²)/3
            eq = Eq(H**2, (8 * pi * G * rho) / 3 + (Lambda / 3))

            # Substitute sample constants
            result = eq.rhs.subs({G: G_value, rho: rho_value, Lambda: Lambda_value})
            return result
        except Exception as e:
            return f"Error: {e}"


# ============================================================
# 📚 Knowledge Agent — Retrieves Contextual Facts
# ============================================================
class KnowledgeAgent:
    def __init__(self):
        self.memory = MemoryManager()

    def search(self, query):
        """Retrieve knowledge or context for a query."""
        # Static domain knowledge
        base_facts = [
            "The Friedmann equations describe the expansion of the universe in general relativity.",
            "The Hubble constant defines the rate of expansion of the universe.",
            "Dark energy is associated with the cosmological constant Λ in Einstein’s equations.",
        ]

        # Include previous memory entries if available
        past_entries = self.memory.search_memory(query)
        if past_entries:
            for entry in past_entries:
                if entry["facts"]:
                    base_facts.extend(entry["facts"])

        return list(set(base_facts))


# ============================================================
# 🧠 Reasoning Agent — Interprets and Learns from Memory
# ============================================================
class ReasoningAgent:
    def __init__(self):
        self.memory = MemoryManager()

    def interpret(self, equation_result, facts):
        """Explain symbolic result using current context and memory."""
        # Retrieve related past insights
        related = self.memory.search_memory("cosmology expansion universe")

        past_context = ""
        if related:
            past_context = "\n\n🧠 Past Knowledge:\n"
            for r in related:
                past_context += f"- {r['query'] or 'Unknown'} → {r['explanation'].strip()[:120]}...\n"

        # Current reasoning synthesis
        eq_str = str(equation_result)
        facts_text = "\n".join(f"- {f}" for f in facts) if facts else "No facts available."

        explanation = f"""
🧮 Computed Result: {eq_str}
🔭 Context:
{facts_text}

💡 Interpretation:
This expression represents how the universe's expansion rate (H²) depends on
the energy density (ρ), spatial curvature (k), and cosmological constant (Λ).
When Λ dominates, the expansion accelerates — aligning with observations of dark energy.
{past_context}
"""
        return explanation
