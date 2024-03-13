from typing import List
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Depends, HTTPException, Request, status
from llama_index.core.chat_engine.types import BaseChatEngine
from llama_index.core.llms import ChatMessage, MessageRole
from app.engine import get_chat_engine

from llama_index.core.schema import MetadataMode

chat_router = r = APIRouter()


class _Message(BaseModel):
    role: MessageRole
    content: str


class _ChatData(BaseModel):
    messages: List[_Message]

START_OF_SOURCES_TOKEN="\n<START_OF_SOURCES>"
START_OF_SOURCE_TOKEN="\n<START_OF_SOURCE>"
END_OF_SOURCE_TOKEN="\n<END_OF_SOURCE>"
@r.post("")
async def chat(
    request: Request,
    data: _ChatData,
    chat_engine: BaseChatEngine = Depends(get_chat_engine),
):
    # check preconditions and get last message
    if len(data.messages) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages provided",
        )
    lastMessage = data.messages.pop()
    if lastMessage.role != MessageRole.USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Last message must be from user",
        )
    # convert messages coming from the request to type ChatMessage
    messages = [
        ChatMessage(
            role=m.role,
            content=m.content.split(START_OF_SOURCES_TOKEN)[0],
        )
        for m in data.messages
    ]
    # query chat engine
    response = await chat_engine.astream_chat(lastMessage.content, messages)

    # stream response
    async def event_generator():
        async for token in response.async_response_gen():
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break
            yield token
        
        sources = response.source_nodes
        yield f"\n\n{START_OF_SOURCES_TOKEN}\n"
        for i, node in enumerate(response.source_nodes):
            # If client closes connection, stop sending events
            if await request.is_disconnected():
                break
            content= node.get_text()
            yield f"\n\n{START_OF_SOURCE_TOKEN}\n"
            yield f"\n\n**[{i+1}]**:\n"
            metadata = node.metadata
            if "file_name" in metadata.keys():
                yield f"\n\nFile: {metadata['file_name']}"
            if "file_path" in metadata.keys():
                yield f"\n\nPath: {metadata['file_path']}"
            yield f"\n{content[:100]}...{content[-100:]}\n"
            yield f"\n\n{END_OF_SOURCE_TOKEN}\n"

    return StreamingResponse(event_generator(), media_type="text/plain")
