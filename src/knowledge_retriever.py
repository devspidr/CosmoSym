from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document
import pandas as pd

# Load processed data
constants = pd.read_csv("data/processed/constants.csv").to_dict(orient="records")[0]

# Example cosmological text corpus
texts = [
    "The Friedmann equations describe the expansion of the universe in general relativity.",
    "The Hubble constant defines the rate of expansion of the universe.",
    "The cosmological constant (Λ) represents dark energy density in Einstein's field equations.",
    f"The current value of the Hubble constant is approximately {constants['H0_current']} km/s/Mpc.",
    "Dark matter constitutes approximately 27% of the total mass-energy of the universe.",
    "The speed of light is constant at approximately 3 × 10^8 m/s.",
]

# Create Document objects for each text
docs = [Document(page_content=t) for t in texts]

# Create embeddings & vector store
embedding = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(docs, embedding)

# Save vector index
vectorstore.save_local("data/processed/vector_index")

print("\n✅ Knowledge base created and saved to data/processed/vector_index")

# Test retrieval
query = "What defines the rate of expansion of the universe?"
retriever = FAISS.load_local("data/processed/vector_index", embedding, allow_dangerous_deserialization=True)
results = retriever.similarity_search(query, k=2)

print("\n🔎 Query:", query)
for i, r in enumerate(results, 1):
    print(f"Result {i}: {r.page_content}")
