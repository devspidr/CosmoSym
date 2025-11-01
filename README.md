# 🌌 COSMOSYM: AI-Powered Symbolic Cosmology

> _"Where cosmic curiosity meets artificial intelligence."_

---

## 🧠 About the Project

I’ve always been deeply fascinated by the mysteries of the universe — how it expands, evolves, and the hidden mathematics behind it.  
To combine this passion for **cosmology** with my interests in **AI**, **symbolic computation**, and **data science**, I built **COSMOSYM** —  
a project that uses **symbolic regression** and **knowledge graphs** to uncover mathematical insights about the **universe’s expansion**.

COSMOSYM blends scientific reasoning with modern AI techniques to simulate how an intelligent agent might “rediscover” relationships between  
cosmic variables like **Λ (cosmological constant)**, **ρ (matter density)**, and **H² (expansion rate)** — just as a physicist would, but computationally.

---

## 🚀 Features

- 🧩 **Symbolic Regression Engine** – discovers mathematical laws hidden in data  
- 🔬 **Symbolic Simplifier** – simplifies and differentiates discovered equations  
- 🧠 **Insight Agent** – generates natural-language insights from symbolic results  
- 🌐 **Interactive Loop** – lets users ask physics-based questions dynamically  
- 📊 **Streamlit Dashboard** – visualize latest cosmic insights with an elegant UI  

---

## 🧰 Tech Stack

| Category | Tools Used |
|-----------|-------------|
| Core Language | Python |
| AI / ML | SymPy, DEAP (Genetic Programming) |
| Data | NumPy, Pandas |
| Visualization | Streamlit, Matplotlib |
| Knowledge & Reasoning | LangGraph-style workflow |
| Environment | Virtualenv (`venv`) |

---

## 🧩 Architecture Overview

COSMOSYM/
│
├── data/ # Generated data, insights, and logs
├── src/
│ ├── symbolic_engine.py # Symbolic regression pipeline
│ ├── symbolic_simplifier.py # Equation simplification
│ ├── insight_agent.py # Insight generation and logging
│ ├── interactive_loop.py # User question + reasoning interface
│ ├── dashboard.py # CLI dashboard for insights
│ └── streamlit_dashboard.py # Streamlit-based visualization
│
└── README.md


---

## 🧠 How It Works (in short)

1. **User asks** a question like _“What happens if dark energy doubles?”_  
2. **Symbolic regression** discovers mathematical relationships between Λ, ρ, and H².  
3. **Simplifier** cleans and derives symbolic relationships.  
4. **Insight agent** generates readable explanations and stores them in JSON.  
5. **Dashboard** displays the insight interactively using Streamlit.

---

## 💬 Example Insight

> **Query:** What happens to cosmic expansion if dark energy doubles?  
> **Equation:** `8231.516619736072 * Λ * ρ`  
> **Insight:**  
> “The equation shows that the universe’s expansion rate (H²) increases linearly with both Λ and ρ — supporting the theory that dark energy accelerates cosmic expansion.”

---

## 🖥️ Running Locally

```bash
# Clone the repository
git clone https://github.com/<your-username>/cosmosym.git
cd cosmosym

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the interactive mode
python src/interactive_loop.py

# (Optional) Launch the dashboard
streamlit run src/streamlit_dashboard.py
```
# 📚 Future Enhancements

Integrate external astrophysical datasets (Planck, JWST, etc.)

Add GPT-based insight summarization

Introduce a dynamic 3D cosmic model visualization

Deploy Streamlit dashboard publicly

# 💖 Inspiration

This project was born from my curiosity about the universe and my desire to combine AI with physics.
I wanted to create a system that doesn’t just compute — but thinks symbolically about how our cosmos works.

J Soundar Balaji
AI & Physics Enthusiast | Developer 
