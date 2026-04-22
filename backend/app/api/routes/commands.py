from fastapi import APIRouter
from pydantic import BaseModel
from app.services.command_dispatcher import CommandDispatcher

router = APIRouter()
dispatcher = CommandDispatcher()

class CommandRequest(BaseModel):
    text: str

@router.post("/execute")
async def execute_command(request: CommandRequest):
    """
    The 'ChatGPT' style endpoint. Takes natural language and executes the matched tool.
    """
    result = dispatcher.process_command(request.text)
    return result
