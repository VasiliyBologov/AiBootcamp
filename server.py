from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os

from db import MongoDBClient
from get_env import load_env, get_env_value

load_env()

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

# Pydantic models for request/response
class MessageCreate(BaseModel):
    message: str
    role: str = "user"

class MessageResponse(BaseModel):
    id: str
    role: str
    text: str
    date: str

# # Dependency to get MongoDB client
# async def get_db():
#     if not mongodb_client.is_connected:
#         try:
#             mongodb_client.connect()
#         except Exception as e:
#             raise HTTPException(status_code=500, detail=f"Failed to connect to MongoDB: {str(e)}")
#     return mongodb_client

# @app.on_event("startup")
# async def startup_db_client():
#     try:
#         mongodb_client.connect()
#         print("Connected to MongoDB")
#     except Exception as e:
#         print(f"Failed to connect to MongoDB: {str(e)}")
#
# @app.on_event("shutdown")
# async def shutdown_db_client():
#     mongodb_client.close()
#     print("Disconnected from MongoDB")

@app.get("/", response_class=HTMLResponse)
async def root():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Simple FastAPI Server</title>
        </head>
        <body>
            <h1>Welcome to the Simple FastAPI Server</h1>
            <p>This is a simple HTML page served by FastAPI.</p>
            <p>MongoDB integration is available at /api/chat endpoint.</p>
        </body>
    </html>
    """
    return html_content

@app.get("/ask")
async def ask():
    return {"status": "ok"}

@app.get("/api/chat")
async def get_chat():
    """Get the most recent chat messages"""
    try:
        messages = db.get_recent_messages(limit=10)
        return {"messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat/message")
async def add_message(message_data: MessageCreate):
    """Add a new message to the chat"""
    try:
        message_id = db.add_message(role=message_data.role, text=message_data.message)
        # Return a system reply (this could be enhanced with AI response generation)
        # reply_id = db.add_message(role="system", text=f"Received your message: {message_data.message}")
        return {"status": "success", "message_id": message_id, "reply": f"Received your message: {message_data.message}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
