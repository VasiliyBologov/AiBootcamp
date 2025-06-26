from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os
import pathlib
import uvicorn
import asyncio

from db import MongoDBClient
from get_env import load_env, get_env_value

from ai.api_agent import ConsultantAgent
from ai.support_agent import SupportAgent
from ai.main_agent import MainAgent

load_env()

# Initialize MongoDB AI Agent
consultant_agent = ConsultantAgent()
support_agent = SupportAgent()
main_agent = MainAgent()


# async def async_run():
#
#     await consultant_agent.run()
#     # ... run other agents
#
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(async_run())


# Initialize MongoDB client
db = MongoDBClient(connection_string=get_env_value('MDB_MCP_CONNECTION_STRING'))
db.connect()

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Mount the client directory as a static files directory
app.mount("/static", StaticFiles(directory="client"), name="static")

# Pydantic models for request/response
class MessageCreate(BaseModel):
    message: str
    role: str = "user"
    sessionId: Optional[str]

class MessageResponse(BaseModel):
    id: str
    role: str
    text: str
    date: str



@app.get("/", response_class=FileResponse)
async def root():
    """Serve the client/index.html file"""

    await consultant_agent.run()

    return FileResponse("client/index.html")

@app.get("/ask")
async def ask():
    return {"status": "ok"}

@app.get("/api/chat/{sessionId}")
async def get_chat(sessionId: str = None):
    """Get the most recent chat messages"""
    await consultant_agent.run()
    try:
        messages = db.get_recent_messages(session_id=sessionId, limit=10)
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/message")
async def add_message(message_data: MessageCreate):
    """Add a new message to the chat"""
    await consultant_agent.run()
    try:
        message_id = db.add_message(role=message_data.role, text=message_data.message, session_id=message_data.sessionId)


        await consultant_agent.run()
        await support_agent.run()
        await main_agent.run(consultant_agent.agent, support_agent.agent)
        r = await main_agent.ask(message_data.message)

        # Return a support reply (this could be enhanced with AI response generation)
        reply_text = f"Support: {r}"
        reply_id = db.add_message(role="support", text=reply_text, session_id=message_data.sessionId)
        return {"status": "success", "message_id": message_id, "reply": reply_text}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    try:
        uvicorn.run(app, reload=False, host="localhost", port=8000)
    finally:
        print("Done")
