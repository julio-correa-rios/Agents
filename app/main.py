from fastapi import FastAPI
from dotenv import load_dotenv
from app.graph import graph
from app.config.logging import setup_logging

# Setup logging
setup_logging()

load_dotenv()
app = FastAPI()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.post("/agent")
async def run_agent(input: str):

    result = graph.invoke({
        "user_input": input,
        "iteration": 0,
        "max_iterations": 3,
        "intermediate_steps": [],
        "search_results": []
    })

    return result