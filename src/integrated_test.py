import sympy as sp
import pandas as pd
from astropy.cosmology import FlatLambdaCDM
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS

# ----------------------------
# 1️⃣ Symbolic setup
# ----------------------------
t = sp.Symbol('t', real=True)
a = sp.Function('a')(t)
H = sp.Function('H')(t)
ρ = sp.Function('rho')(t)
p = sp.Function('p')(t)
G, Λ, k = sp.symbols('G Λ k', real=True, positive=True)

friedmann_eq = sp.Eq(H**2, (8*sp.pi*G/3)*ρ - k/(a**2) + Λ/3)
acc_eq = sp.Eq(sp.diff(H, t) + H**2, - (4*sp.pi*G/3)*(ρ + 3*p) + Λ/3)

print("\n🧮 Symbolic equations loaded:")
sp.pprint(friedmann_eq)
sp.pprint(acc_eq)

# ----------------------------
# 2️⃣ Load processed data
# ----------------------------
df = pd.read_csv("data/processed/cosmology_data.csv")
consts = pd.read_csv("data/processed/constants.csv").to_dict(orient="records")[0]

cosmo = FlatLambdaCDM(H0=consts["H0_current"], Om0=consts["Omega_matter"])
z_sample = 1.0
dist = cosmo.comoving_distance(z_sample).value
print(f"\n🌌 Example: Comoving distance at z={z_sample}: {dist:.2f} Mpc")

# ----------------------------
# 3️⃣ Retrieve cosmological context (RAG)
# ----------------------------
embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
retriever = FAISS.load_local("data/processed/vector_index", embedding, allow_dangerous_deserialization=True)

query = "What is the cosmological constant and its role in the Friedmann equation?"
results = retriever.similarity_search(query, k=2)

print("\n🔎 Knowledge Retrieval Results:")
for i, r in enumerate(results, 1):
    print(f"{i}. {r.page_content}")

# ----------------------------
# 4️⃣ Combine symbolic + numeric context
# ----------------------------
example_sub = friedmann_eq.subs({
    G: consts["G_gravitational"],
    Λ: 1e-52,
    k: 0,
    ρ: 9e-27
})
evaluated = sp.simplify(example_sub.rhs)
print(f"\n🧠 Example symbolic evaluation result: {evaluated:.3e}")

# ----------------------------
# 5️⃣ Summary
# ----------------------------
print("\n✅ Integration test complete — CosmoSym core modules working together.")
