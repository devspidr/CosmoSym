# src/symbolic_simplifier.py
import sympy as sp
import json
from pathlib import Path

def simplify_expression(expr_str: str):
    """Simplify and analyze the symbolic expression found by the regression engine."""
    # Define variables
    rho, Lambda = sp.symbols("rho Lambda")

    # Convert string expression to SymPy object
    expr = sp.sympify(expr_str, locals={"rho": rho, "Lambda": Lambda, "exp": sp.exp, "mul": sp.Mul})

    # Simplify algebraically
    simplified = sp.simplify(expr)

    # Try to expand and factor for clarity
    expanded = sp.expand(simplified)
    factored = sp.factor(expanded)

    # Compute partial derivatives to see influence of rho and Lambda
    d_rho = sp.diff(factored, rho)
    d_Lambda = sp.diff(factored, Lambda)

    result = {
        "original_expression": expr_str,
        "simplified_expression": str(simplified),
        "factored_expression": str(factored),
        "derivative_wrt_rho": str(d_rho),
        "derivative_wrt_Lambda": str(d_Lambda)
    }

    # Save output for the agent to use later
    output_file = Path("data/simplified_expression.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(result, f, indent=4)

    print("\n=== Simplification Results ===")
    for k, v in result.items():
        print(f"{k}:\n {v}\n")

    print(f"✅ Simplified expression saved to {output_file}")
    return result


if __name__ == "__main__":
    # Use the top expression from your symbolic_engine output
    best_expr = "mul(mul(Lambda, rho), exp(9.015725556127048))"
    simplify_expression(best_expr)
