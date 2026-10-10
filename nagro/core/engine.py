"""NAGRO 4.1 Core Engine - The brain of the system."""

from __future__ import annotations
import time
import uuid
from typing import AsyncIterator

from nagro.core.config import settings
from nagro.core.models import (
    ChatRequest, ChatResponse, TaskType, Message, MessageRole, Conversation
)
from nagro.core.prompts import NAGRO_SYSTEM_PROMPT, ROUTING_PROMPT
from nagro.agents import AgentRouter
from nagro.memory.context import ContextManager


class NAGROEngine:
    """Main engine that orchestrates all NAGRO 4.1 operations."""

    def __init__(self):
        self.model_name = "NAGRO 4.1"
        self.version = "4.1.0"
        self.router = AgentRouter()
        self.context = ContextManager()
        self.conversations: dict[str, Conversation] = {}
        self._llm_client = None
        self._init_llm()

    def _init_llm(self):
        provider = settings.nagro_llm_provider
        if provider == "anthropic" and settings.anthropic_api_key:
            import anthropic
            self._llm_client = anthropic.AsyncAnthropic(
                api_key=settings.anthropic_api_key
            )
            self._llm_type = "anthropic"
        elif provider == "openai" and settings.openai_api_key:
            import openai
            self._llm_client = openai.AsyncOpenAI(
                api_key=settings.openai_api_key
            )
            self._llm_type = "openai"
        elif provider == "groq" and settings.groq_api_key:
            import groq
            self._llm_client = groq.AsyncGroq(
                api_key=settings.groq_api_key
            )
            self._llm_type = "groq"
        else:
            self._llm_client = None
            self._llm_type = "none"

    def _get_or_create_conversation(self, conversation_id: str | None) -> Conversation:
        if conversation_id and conversation_id in self.conversations:
            return self.conversations[conversation_id]
        conv = Conversation()
        self.conversations[conv.id] = conv
        return conv

    async def classify_task(self, message: str) -> TaskType:
        """Intelligently classify the user's intent."""
        msg_lower = message.lower()

        image_keywords = [
            "generate image", "create image", "draw", "picture of",
            "illustration", "generate a photo", "make an image",
            "design", "visual", "artwork", "generate art",
            "image of", "photo of", "painting of",
        ]
        if any(kw in msg_lower for kw in image_keywords):
            return TaskType.IMAGE

        code_keywords = [
            "code", "function", "class", "program", "debug", "error",
            "compile", "syntax", "algorithm", "api", "database",
            "python", "javascript", "java", "html", "css", "react",
            "django", "flask", "node", "sql", "git", "docker",
            "fix this", "write a script", "implement", "refactor",
            "def ", "import ", "const ", "let ", "var ",
        ]
        if any(kw in msg_lower for kw in code_keywords):
            return TaskType.CODE

        research_keywords = [
            "research", "find out", "search", "latest news",
            "what is happening", "current", "trend", "statistics",
            "study", "report", "analyze data", "compare",
            "pros and cons", "review of", "source",
        ]
        if any(kw in msg_lower for kw in research_keywords):
            return TaskType.RESEARCH

        math_keywords = [
            "calculate", "solve", "equation", "integral", "derivative",
            "matrix", "probability", "statistics", "theorem",
            "proof", "formula", "math", "algebra", "calculus",
            "geometry", "trigonometry", "+", "=", "×",
        ]
        if any(kw in msg_lower for kw in math_keywords):
            return TaskType.MATH

        creative_keywords = [
            "write a story", "poem", "creative", "fiction",
            "narrative", "script", "dialogue", "blog post",
            "article", "essay", "content", "slogan",
            "tagline", "lyrics", "haiku",
        ]
        if any(kw in msg_lower for kw in creative_keywords):
            return TaskType.CREATIVE

        reasoning_keywords = [
            "why", "how does", "explain", "analyze", "reason",
            "logic", "think", "evaluate", "assess", "strategy",
            "decision", "plan", "approach", "consider",
        ]
        if any(kw in msg_lower for kw in reasoning_keywords):
            return TaskType.REASONING

        return TaskType.CHAT

    async def process(self, request: ChatRequest) -> ChatResponse:
        """Process a user request through the NAGRO pipeline."""
        start_time = time.time()

        conv = self._get_or_create_conversation(request.conversation_id)
        conv.messages.append(Message(role=MessageRole.USER, content=request.message))

        task_type = request.task_type or await self.classify_task(request.message)
        conv.task_type = task_type

        agent = self.router.get_agent(task_type)
        history = self.context.build_context(conv)

        response_text = await agent.execute(
            message=request.message,
            history=history,
            llm_client=self._llm_client,
            llm_type=self._llm_type,
        )

        conv.messages.append(Message(
            role=MessageRole.ASSISTANT,
            content=response_text,
            metadata={"task_type": task_type.value},
        ))

        processing_time = time.time() - start_time
        return ChatResponse(
            message=response_text,
            task_type=task_type,
            conversation_id=conv.id,
            processing_time=round(processing_time, 3),
        )

    async def process_stream(
        self, request: ChatRequest
    ) -> AsyncIterator[str]:
        """Process a request with streaming output."""
        conv = self._get_or_create_conversation(request.conversation_id)
        conv.messages.append(Message(role=MessageRole.USER, content=request.message))

        task_type = request.task_type or await self.classify_task(request.message)
        agent = self.router.get_agent(task_type)
        history = self.context.build_context(conv)

        full_response = []
        async for chunk in agent.execute_stream(
            message=request.message,
            history=history,
            llm_client=self._llm_client,
            llm_type=self._llm_type,
        ):
            full_response.append(chunk)
            yield chunk

        conv.messages.append(Message(
            role=MessageRole.ASSISTANT,
            content="".join(full_response),
            metadata={"task_type": task_type.value},
        ))

    def get_conversation(self, conversation_id: str) -> Conversation | None:
        return self.conversations.get(conversation_id)

    def clear_conversation(self, conversation_id: str) -> bool:
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False

    @property
    def info(self) -> dict:
        return {
            "model": self.model_name,
            "version": self.version,
            "provider": settings.nagro_llm_provider,
            "capabilities": [
                "chat", "coding", "image_generation",
                "research", "mathematics", "creative_writing",
                "reasoning", "code_review", "debugging",
            ],
            "status": "operational",
        }
