"""NAGRO 4.1 Core Engine — fully self-built, with advanced reasoning."""

from __future__ import annotations
import time
from typing import AsyncIterator

from nagro.core.config import settings
from nagro.core.models import (
    ChatRequest, ChatResponse, TaskType, Message, MessageRole, Conversation
)
from nagro.agents import AgentRouter
from nagro.memory.context import ContextManager
from nagro.reasoning.chain_of_thought import ChainOfThought
from nagro.reasoning.self_reflection import SelfReflection
from nagro.reasoning.planner import TaskPlanner


class NAGROEngine:
    """Main engine that orchestrates all NAGRO 4.1 operations."""

    def __init__(self):
        self.model_name = "NAGRO 4.1"
        self.version = "4.1.0"
        self.router = AgentRouter()
        self.context = ContextManager()
        self.conversations: dict[str, Conversation] = {}
        self.cot = ChainOfThought()
        self.reflection = SelfReflection()
        self.planner = TaskPlanner()
        self._rag = None

    def _get_rag(self):
        """Lazy-load RAG retriever."""
        if self._rag is None:
            from nagro.rag.retriever import Retriever
            self._rag = Retriever()
        return self._rag

    async def classify_task(self, message: str) -> TaskType:
        """Intelligently classify the user's intent."""
        msg_lower = message.lower()

        image_keywords = [
            "generate image", "create image", "draw", "picture of",
            "illustration", "generate a photo", "make an image",
            "design a logo", "artwork", "generate art",
            "image of", "photo of", "painting of", "image banao",
            "tasveer", "image bana", "sketch",
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
            "code likho", "program banao", "bug fix", "runtime",
        ]
        if any(kw in msg_lower for kw in code_keywords):
            return TaskType.CODE

        research_keywords = [
            "research", "find out", "search", "latest news",
            "what is happening", "current", "trend", "statistics",
            "study", "report", "analyze data", "compare",
            "pros and cons", "review of", "source",
            "khojo", "search karo", "pata karo",
        ]
        if any(kw in msg_lower for kw in research_keywords):
            return TaskType.RESEARCH

        math_keywords = [
            "calculate", "solve", "equation", "integral", "derivative",
            "matrix", "probability", "statistics", "theorem",
            "proof", "formula", "math", "algebra", "calculus",
            "geometry", "trigonometry",
        ]
        if any(kw in msg_lower for kw in math_keywords):
            return TaskType.MATH

        creative_keywords = [
            "write a story", "poem", "creative", "fiction",
            "narrative", "script", "dialogue", "blog post",
            "article", "essay", "content", "slogan",
            "tagline", "lyrics", "haiku", "kahani",
        ]
        if any(kw in msg_lower for kw in creative_keywords):
            return TaskType.CREATIVE

        reasoning_keywords = [
            "why", "how does", "explain", "analyze", "reason",
            "logic", "think", "evaluate", "assess", "strategy",
            "decision", "plan", "approach", "consider",
            "samjhao", "kaise", "kyun",
        ]
        if any(kw in msg_lower for kw in reasoning_keywords):
            return TaskType.REASONING

        return TaskType.CHAT

    def _should_use_deep_reasoning(self, message: str) -> bool:
        """Determine if a query needs deep reasoning vs simple response."""
        complex_signals = [
            "step by step", "explain in detail", "compare", "analyze",
            "pros and cons", "trade-off", "design", "architect",
            "optimize", "complex", "detailed", "thoroughly",
            "plan", "strategy", "evaluate", "deep dive",
        ]
        msg_lower = message.lower()
        return any(s in msg_lower for s in complex_signals) or len(message) > 200

    async def process(self, request: ChatRequest) -> ChatResponse:
        """Process a user request through the full NAGRO pipeline."""
        start_time = time.time()

        conv = self._get_or_create_conversation(request.conversation_id)
        conv.messages.append(Message(role=MessageRole.USER, content=request.message))

        task_type = request.task_type or await self.classify_task(request.message)
        conv.task_type = task_type

        # Get RAG context if available
        rag_context = ""
        try:
            rag = self._get_rag()
            if rag.store.count > 0:
                rag_context = rag.build_context(request.message)
        except Exception:
            pass

        agent = self.router.get_agent(task_type)
        history = self.context.build_context(conv)

        # Inject RAG context into the message if available
        effective_message = request.message
        if rag_context:
            effective_message = (
                f"{request.message}\n\n"
                f"[Relevant context from knowledge base:]\n{rag_context}"
            )

        # Use deep reasoning for complex queries
        if self._should_use_deep_reasoning(request.message):
            effective_message = self.cot.build_cot_prompt(effective_message)

        response_text = await agent.execute(
            message=effective_message,
            history=history,
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
        ):
            full_response.append(chunk)
            yield chunk

        conv.messages.append(Message(
            role=MessageRole.ASSISTANT,
            content="".join(full_response),
            metadata={"task_type": task_type.value},
        ))

    async def process_agentic(self, task: str, max_steps: int = 10) -> dict:
        """Run a multi-step agentic task with tool use."""
        from nagro.agents.agentic import AgenticLoop, AgentTrace, AgentStep

        loop = AgenticLoop(max_steps=max_steps)
        trace = AgentTrace(task=task)

        for step_num in range(max_steps):
            prompt = loop.build_react_prompt(task, trace.steps)

            try:
                from nagro.core.inference import generate
                llm_output = generate(prompt, max_tokens=1024)
            except FileNotFoundError:
                trace.final_answer = (
                    "Model not loaded. Run `python download_model.py` to set up."
                )
                break

            step = loop.parse_step(llm_output)
            step.step_number = step_num + 1

            if step.is_final:
                trace.final_answer = step.action_input
                trace.add_step(step)
                break

            if step.action:
                observation = await loop.execute_tool(step.action, step.action_input)
                step.observation = observation

            trace.add_step(step)

        return {
            "task": trace.task,
            "answer": trace.final_answer,
            "steps": [
                {
                    "step": s.step_number,
                    "thought": s.thought,
                    "action": s.action,
                    "result": s.observation,
                }
                for s in trace.steps
            ],
            "total_steps": trace.total_steps,
        }

    def ingest_document(self, doc_id: str, text: str, metadata: dict | None = None):
        """Add a document to the RAG knowledge base."""
        rag = self._get_rag()
        rag.ingest(doc_id, text, metadata)

    def _get_or_create_conversation(self, conversation_id: str | None) -> Conversation:
        if conversation_id and conversation_id in self.conversations:
            return self.conversations[conversation_id]
        conv = Conversation()
        self.conversations[conv.id] = conv
        return conv

    def get_conversation(self, conversation_id: str) -> Conversation | None:
        return self.conversations.get(conversation_id)

    def clear_conversation(self, conversation_id: str) -> bool:
        if conversation_id in self.conversations:
            del self.conversations[conversation_id]
            return True
        return False

    @property
    def info(self) -> dict:
        from nagro.core.inference import is_model_loaded
        from nagro.core.model_manager import is_model_downloaded

        return {
            "model": self.model_name,
            "version": self.version,
            "architecture": "Neural Adaptive Generative Reasoning Operator",
            "inference": "100% local",
            "llm_model": settings.nagro_llm_model,
            "model_downloaded": is_model_downloaded(),
            "model_loaded": is_model_loaded(),
            "capabilities": [
                "chat", "coding", "image_generation",
                "research", "mathematics", "creative_writing",
                "reasoning", "code_review", "debugging",
                "agentic_tasks", "rag", "document_analysis",
                "chain_of_thought", "self_reflection",
                "task_planning", "tool_use", "web_search",
                "calculator", "code_execution",
            ],
            "reasoning_systems": [
                "chain_of_thought",
                "tree_of_thought",
                "self_reflection",
                "multi_perspective_analysis",
                "internal_debate",
                "task_decomposition",
            ],
            "external_apis": "none — fully self-built",
            "status": "operational",
        }
