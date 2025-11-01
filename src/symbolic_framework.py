import sympy as sp

# Define core cosmological symbols
t = sp.Symbol('t', real=True, positive=True)          # time
a = sp.Function('a')(t)                               # scale factor
H = sp.Function('H')(t)                               # Hubble parameter
ρ = sp.Function('rho')(t)                             # density
p = sp.Function('p')(t)                               # pressure
G, Λ, k, c = sp.symbols('G Λ k c', real=True, positive=True)

# Define core relations
friedmann_eq = sp.Eq(H**2, (8*sp.pi*G/3)*ρ - k/(a**2) + Λ/3)
acceleration_eq = sp.Eq(sp.diff(H, t) + H**2, - (4*sp.pi*G/3)*(ρ + 3*p) + Λ/3)

# Display results
print("\nFriedmann Equation:")
sp.pprint(friedmann_eq)
print("\nAcceleration Equation:")
sp.pprint(acceleration_eq)

# Example: substitute symbolic values
example_sub = friedmann_eq.subs({
    G: 6.674e-11,
    Λ: 1e-52,
    k: 0,
    ρ: 9e-27
})
print("\nExample symbolic evaluation (simplified):")
print(sp.simplify(example_sub.rhs))
