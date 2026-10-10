"""Data models for NAGRO 4.1."""

from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional, Any
from enum import Enum
from datetime import datetime
import uuid


class TaskType(str, Enum):
    CHAT = "chat"
    CODE = "code"
    IMAGE = "image"
    RESEARCH = "research"
    MATH = "math"
    CREATIVE = "creative"
    REASONING = "reasoning"


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class Message(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    task_type: Optional[TaskType] = None
    stream: bool = False
    context: Optional[dict[str, Any]] = None


class ChatResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    model: str = "NAGRO 4.1"
    message: str
    task_type: TaskType
    conversation_id: str
    tokens_used: int = 0
    processing_time: float = 0.0
    metadata: dict[str, Any] = Field(default_factory=dict)


class ImageRequest(BaseModel):
    prompt: str
    style: Optional[str] = None
    size: str = "1024x1024"
    n: int = 1
    quality: str = "standard"


class ImageResponse(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    model: str = "NAGRO 4.1"
    images: list[dict[str, str]]
    revised_prompt: Optional[str] = None


class CodeRequest(BaseModel):
    prompt: str
    language: Optional[str] = None
    context: Optional[str] = None
    action: str = "generate"  # generate, review, debug, explain, optimize


class ResearchRequest(BaseModel):
    query: str
    depth: str = "standard"  # quick, standard, deep
    sources: int = 5


class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    messages: list[Message] = Field(default_factory=list)
    task_type: Optional[TaskType] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
