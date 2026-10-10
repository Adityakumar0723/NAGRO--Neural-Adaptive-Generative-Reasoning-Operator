"""
NAGRO 4.1 — Context Window Optimizer.

Intelligently manages context window to maximize quality within token limits.
Compresses old messages, prioritizes relevant context, and manages token budget.
"""

from __future__ import annotations


class ContextOptimizer:
    """Optimizes context window for maximum output quality."""

    def __init__(self, max_context_tokens: int = 4096):
        self.max_tokens = max_context_tokens
        self.reserved_for_response = 1024

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation (1 token ~ 4 chars for English)."""
        return len(text) // 4 + 1

    def optimize_context(
        self,
        system_prompt: str,
        messages: list[dict[str, str]],
        rag_context: str = "",
    ) -> list[dict[str, str]]:
        """Build an optimized context that fits within token limits."""
        available = self.max_tokens - self.reserved_for_response
        available -= self.estimate_tokens(system_prompt)

        if rag_context:
            rag_tokens = self.estimate_tokens(rag_context)
            if rag_tokens > available // 3:
                rag_context = self._truncate(rag_context, available // 3)
            available -= self.estimate_tokens(rag_context)

        if not messages:
            return []

        # Always keep the latest message
        latest = messages[-1]
        available -= self.estimate_tokens(latest["content"])

        # Fill remaining budget with recent messages (newest first)
        kept = [latest]
        for msg in reversed(messages[:-1]):
            msg_tokens = self.estimate_tokens(msg["content"])
            if msg_tokens > available:
                compressed = self._compress_message(msg, available)
                if compressed:
                    kept.insert(0, compressed)
                break
            available -= msg_tokens
            kept.insert(0, msg)

        return kept

    def _compress_message(self, message: dict[str, str], max_tokens: int) -> dict[str, str] | None:
        """Compress a message to fit within token budget."""
        content = message["content"]
        target_chars = max_tokens * 4

        if len(content) <= target_chars:
            return message

        # Keep first and last parts
        half = target_chars // 2
        compressed = content[:half] + "\n...[compressed]...\n" + content[-half:]
        return {"role": message["role"], "content": compressed}

    def _truncate(self, text: str, max_tokens: int) -> str:
        target_chars = max_tokens * 4
        if len(text) <= target_chars:
            return text
        return text[:target_chars] + "\n...[truncated]"

    def build_enhanced_context(
        self,
        user_message: str,
        history: list[dict[str, str]],
        rag_context: str = "",
        memories: list[str] | None = None,
        facts: list[str] | None = None,
    ) -> str:
        """Build a rich context string with all available information."""
        parts = []

        if memories:
            parts.append("**Relevant Memories:**\n" + "\n".join(f"- {m}" for m in memories[:5]))

        if facts:
            parts.append("**Known Facts:**\n" + "\n".join(f"- {f}" for f in facts[:5]))

        if rag_context:
            parts.append(f"**Knowledge Base Context:**\n{rag_context}")

        if parts:
            return "\n\n".join(parts) + f"\n\n**User Query:** {user_message}"

        return user_message
