import logging
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from app.graph import create_graph
from app.db.checkpointing import get_checkpoint_saver
from app.config.logging import setup_logging

setup_logging()
logger = logging.getLogger(__name__)
load_dotenv()

# Create app with checkpointer for FastAPI
saver = get_checkpoint_saver()
graph = create_graph(checkpointer=saver)

app = FastAPI()


class AgentRequest(BaseModel):
    user_input: str
    thread_id: str = None


class AgentResponse(BaseModel):
    thread_id: str
    result: dict


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/agent", response_model=AgentResponse)
async def run_agent(request: AgentRequest):
    thread_id = request.thread_id or str(uuid.uuid4())
    logger.info(f"[API] Thread: {thread_id}")

    try:
        result = graph.invoke(
            {
                "user_input": request.user_input,
                "iteration": 0,
                "max_iterations": 3,
                "intermediate_steps": [],
                "search_results": []
            },
            config={"configurable": {"thread_id": thread_id}}
        )
        return AgentResponse(thread_id=thread_id, result=result)
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agent/resume")
async def resume_agent(thread_id: str):
    return {"status": "resumed", "thread_id": thread_id}


@app.get("/agent/sessions")
async def list_sessions():
    return {"status": "ok"}
