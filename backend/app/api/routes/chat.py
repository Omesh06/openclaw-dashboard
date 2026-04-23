from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime
from app.core.database import get_db_connection
from app.services.command_dispatcher import CommandDispatcher

router = APIRouter()
dispatcher = CommandDispatcher()

class ChatMessage(BaseModel):
    text: str

@router.post("/send")
async def send_message(msg: ChatMessage):
    """
    The primary interface for chatting with OpenClaw.
    It handles both general conversation and command execution.
    """
    # 1. Save User Message to History
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO chat_history (role, message, timestamp) VALUES (?, ?, ?)",
        ("user", msg.text, datetime.now().isoformat())
    )
    conn.commit()
    
    # 2. Process command via Dispatcher
    result = dispatcher.process_command(msg.text)
    
    # 3. Determine Response
    if result["status"] == "executing":
        response_text = f"✅ {result['message']}"
    elif result["status"] == "unknown":
        response_text = result["message"]
    else:
        response_text = result.get("message", "I'm processing that for you.")

    # 4. Save Bot Response to History
    cursor.execute(
        "INSERT INTO chat_history (role, message, timestamp) VALUES (?, ?, ?)",
        ("bot", response_text, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()

    return {
        "role": "bot",
        "text": response_text,
        "intent": result.get("intent")
    }

@router.get("/history")
async def get_chat_history(limit: int = 50):
    """Fetch recent chat history."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT role, message, timestamp FROM chat_history ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    # Reverse to show in chronological order
    history = [{"role": row["role"], "text": row["message"], "timestamp": row["timestamp"]} for row in rows]
    return {"status": "success", "data": history[::-1]}
