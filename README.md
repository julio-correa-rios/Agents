# 🧠 AI Agent Playground (LangGraph + FastAPI)

This repo is a simple, evolving playground for building AI agents using LangGraph, FastAPI, and external tools like Tavily.

The goal is to learn by doing — starting small, then gradually turning this into a more robust, production-style system.

---

## 🚀 What this is (for now)

At the moment, this project includes:

- A basic **LangGraph agent** with multiple steps (planner → executor → responder)
- **Web search integration** (Tavily) for real-time information
- A **structured state** using Pydantic (no more messy string blobs)
- A simple **FastAPI endpoint** to interact with the agent
- **LangSmith tracing** for observability and debugging
- Early steps toward a **ReAct-style loop** (think → search → refine → answer)

It’s intentionally simple, but set up in a way that can grow.

---

## 🧩 How it works

High level flow:
# 🧠 AI Agent Playground (LangGraph + FastAPI)

This repo is a simple, evolving playground for building AI agents using LangGraph, FastAPI, and external tools like Tavily.

The goal is to learn by doing — starting small, then gradually turning this into a more robust, production-style system.

---

## 🚀 What this is (for now)

At the moment, this project includes:

- A basic **LangGraph agent** with multiple steps (planner → executor → responder)
- **Web search integration** (Tavily) for real-time information
- A **structured state** using Pydantic (no more messy string blobs)
- A simple **FastAPI endpoint** to interact with the agent
- **LangSmith tracing** for observability and debugging
- Early steps toward a **ReAct-style loop** (think → search → refine → answer)

It’s intentionally simple, but set up in a way that can grow.

---

## 🧩 How it works

High level flow:

User input
↓
Planner (decides what to do)
↓
Executor (calls tools like search)
↓
Filter (cleans up noisy results)
↓
Responder (generates final answer)


Everything runs through a shared **state object**, which gets updated at each step.

---

## 🛠️ Tech stack

- Python 3.12
- LangGraph
- LangChain (LLM interface)
- FastAPI
- Tavily (search)
- Pydantic (state modelling)
- LangSmith (tracing / debugging)

---

## ▶️ Running locally

1. Create a virtual environment and install dependencies:

```bash
pip install -r requirements.txt

2. Set environment variables (e.g. in .env):
OPENAI_API_KEY=...
TAVILY_API_KEY=...
LANGCHAIN_API_KEY=...
LANGCHAIN_TRACING_V2=true

3. Start the API
uvicorn app.main:app --reload

4. Open docs:
http://127.0.0.1:8000/docs

🧪 LangGraph Studio (optional). 

To visualise the graph, you can write in command line the following:
langgraph dev

And then open:
http://localhost:2024