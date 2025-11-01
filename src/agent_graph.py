from langgraph.graph import StateGraph, START, END
from agentic_core import SymbolicAgent, KnowledgeAgent, ReasoningAgent
from memory_manager import MemoryManager

memory = MemoryManager()

# =====================================================
# 🧩 Step 1: Define Shared State
# =====================================================
class GraphState(dict):
    pass


# =====================================================
# 🧠 Step 2: Initialize Agents
# =====================================================
symbolic_agent = SymbolicAgent()
knowledge_agent = KnowledgeAgent()
reasoning_agent = ReasoningAgent()


# =====================================================
# 🧩 Step 3: Node Functions
# =====================================================
def retrieve_knowledge(state: GraphState):
    query = state.get("query", "")
    facts = knowledge_agent.search(query)
    state["facts"] = facts
    print("\n📚 Retrieved Facts:")
    for f in facts:
        print(" -", f)
    return state


def compute_equation(state: GraphState):
    result = symbolic_agent.evaluate(6.674e-11, 1e-52, 9e-27)
    state["equation_result"] = result
    print("\n🧮 Computed symbolic result:", result)
    return state


def reason_result(state: GraphState):
    facts = state.get("facts", [])
    eq_result = state.get("equation_result", None)
    explanation = reasoning_agent.interpret(eq_result, facts)

    # Save memory here
    memory.add_entry(
        state.get("query", ""),
        state.get("facts", []),
        state.get("equation_result", ""),
        explanation
    )

    state["explanation"] = explanation
    print("\n💡 Generated Explanation:")
    print(explanation)
    return state


def output_final_state(state: GraphState):
    """Return final structured result"""
    return {
        "query": state.get("query"),
        "facts": state.get("facts"),
        "equation_result": state.get("equation_result"),
        "explanation": state.get("explanation")
    }


# =====================================================
# 🧠 Step 4: Build Graph
# =====================================================
workflow = StateGraph(GraphState)

workflow.add_node("retriever", retrieve_knowledge)
workflow.add_node("symbolic_math", compute_equation)
workflow.add_node("reasoner", reason_result)
workflow.add_node("output", output_final_state)

workflow.add_edge(START, "retriever")
workflow.add_edge("retriever", "symbolic_math")
workflow.add_edge("symbolic_math", "reasoner")
workflow.add_edge("reasoner", "output")
workflow.add_edge("output", END)

graph = workflow.compile()


# =====================================================
# 🚀 Step 5: Execute
# =====================================================
if __name__ == "__main__":
    query = "relationship between dark energy and universe expansion"
    print(f"\n🧠 Running agent graph for query: {query}\n")

    result = graph.invoke({"query": query})

    print("\n✅ Agent Graph Completed.\n")

    if isinstance(result, dict):
        print("🪐 Final Structured Output:")
        print(result)
        print("\n🌌 Final Explanation:\n", result.get("explanation", "No explanation found."))
    else:
        print("⚠️ Graph returned unexpected output type:", type(result))
        print(result)
