import logging
import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from app.graph import create_graph
from app.db.checkpointing import get_checkpoint_saver, list_sessions, clear_session
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
    """Resume an existing agent session."""
    logger.info(f"[API] Resuming thread: {thread_id}")
    
    try:
        # Get last checkpoint for this thread
        result = graph.invoke(
            {
                "user_input": "",  # Continue from last state
                "iteration": 0,
                "max_iterations": 3,
                "intermediate_steps": [],
                "search_results": []
            },
            config={"configurable": {"thread_id": thread_id}}
        )
        return AgentResponse(thread_id=thread_id, result=result)
    except Exception as e:
        logger.error(f"Error resuming: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/agent/sessions")
async def list_agent_sessions():
    """List all saved sessions with checkpoint metadata."""
    try:
        sessions = list_sessions()
        return {"status": "ok", "sessions": sessions}
    except Exception as e:
        logger.error(f"Error listing sessions: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/agent/sessions/{thread_id}")
async def delete_session(thread_id: str):
    """Delete a specific session and all its checkpoints."""
    try:
        success = clear_session(thread_id)
        if success:
            return {"status": "ok", "message": f"Session {thread_id} deleted"}
        else:
            raise HTTPException(status_code=500, detail="Failed to delete session")
    except Exception as e:
        logger.error(f"Error deleting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))
