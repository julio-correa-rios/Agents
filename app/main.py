from fastapi import FastAPI
from dotenv import load_dotenv
from app.graph import graph

load_dotenv()
app = FastAPI()


@app.post("/agent")
async def run_agent(input: str):

    result = graph.invoke({
        "user_input": input
    })

    return result