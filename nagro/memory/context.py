"""Context management for NAGRO 4.1 conversations."""

from __future__ import annotations
from nagro.core.models import Conversation, MessageRole


class ContextManager:
    """Manages conversation context and history for the NAGRO engine."""

    MAX_HISTORY_MESSAGES = 50
    MAX_CONTEXT_TOKENS = 100_000

    def build_context(self, conversation: Conversation) -> list[dict[str, str]]:
        """Build a context window from conversation history."""
        messages = conversation.messages[-self.MAX_HISTORY_MESSAGES:]
        return [
            {"role": msg.role.value, "content": msg.content}
            for msg in messages
            if msg.role in (MessageRole.USER, MessageRole.ASSISTANT)
        ]

    def summarize_if_needed(self, conversation: Conversation) -> str | None:
        """Generate a summary if conversation is getting too long."""
        if len(conversation.messages) > self.MAX_HISTORY_MESSAGES:
            early_messages = conversation.messages[:-self.MAX_HISTORY_MESSAGES]
            summary_parts = []
            for msg in early_messages[-10:]:
                role = "User" if msg.role == MessageRole.USER else "NAGRO"
                summary_parts.append(f"{role}: {msg.content[:200]}")
            return "Previous conversation summary:\n" + "\n".join(summary_parts)
        return None
