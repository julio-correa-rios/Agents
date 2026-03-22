# 🧠 AI Agent Playground (LangGraph + FastAPI)

This repo is a simple, evolving playground for building AI agents using LangGraph, FastAPI, and external tools like Tavily.

The goal is to go through a complete AI agentic workflow by starting small, and then gradually turning this into a more robust, production-style system.

---

## 🚀 What this is (for now)

At the moment, this project includes:

- A basic **LangGraph agent** with multiple steps (planner → executor → responder)
- **Web search integration** (Tavily) for real-time information
- A **structured state** using Pydantic (no more messy strings or json objects)
- A simple **FastAPI endpoint** to interact with the agent
- **LangSmith tracing** for observability and debugging
- Early steps toward a **ReAct-style loop** (think → search → refine → answer)

It’s intentionally simple, but set up in a way that can grow.

---

## 🧩 How it works

High level flow:

User input -> Planner (decides what to do) -> Executor (calls tools like search)
-> Filter (cleans up noisy results) -> Responder (generates final answer)


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
```

2. Set environment variables (e.g. in .env):
- OPENAI_API_KEY=...
- TAVILY_API_KEY=...
- LANGCHAIN_API_KEY=...
- LANGCHAIN_TRACING_V2=true

3. Start the API
```bash
uvicorn app.main:app --reload
```

4. Open docs:
```bash
http://127.0.0.1:8000/docs
```

## 🧪 LangGraph Studio (optional). 

To visualise the graph, you can write in command line the following:
langgraph dev

And then open:
```bash
http://localhost:2024
```

## 📊 Observability

Runs are tracked with LangSmith, which lets you:

See each node execution
Inspect inputs and outputs
Debug agent behaviour
⚠️ Important note

This project is very much a work in progress.

Things will change, break, and get refactored as new ideas are tested:

- Better filtering and ranking of search results
- More robust ReAct loops
- Additional tools (e.g. Neo4j or MongoDB or even Postgres)
- CI/CD and deployment setup

## 🎯 Direction

The aim is to evolve this into a:

More reliable agent system
With proper evaluation and testing
And eventually a deployable AI service

## Final note

This is not meant to be perfect — it’s meant to improve over time.
If something looks rough, that’s probably intentional (or at least accepted for now). Again, my intention is to build something meaningful but not following a pre-defined approach, but a totally experimental one. 