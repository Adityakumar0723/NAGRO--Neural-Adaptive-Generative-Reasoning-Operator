"""
NAGRO 4.1 — Prompt Optimizer.

Automatically enhances user prompts for better output quality.
Adds structure, clarification, and context to get the best response.
"""

from __future__ import annotations
import re


class PromptOptimizer:
    """Automatically improves prompts for higher quality outputs."""

    def optimize(self, message: str, task_type: str) -> str:
        """Enhance a user's message for better LLM output."""
        message = message.strip()
        if not message:
            return message

        if len(message) < 15:
            message = self._expand_short_prompt(message)

        if task_type == "code":
            return self._optimize_code_prompt(message)
        elif task_type == "math":
            return self._optimize_math_prompt(message)
        elif task_type == "research":
            return self._optimize_research_prompt(message)
        elif task_type == "creative":
            return self._optimize_creative_prompt(message)
        elif task_type == "reasoning":
            return self._optimize_reasoning_prompt(message)
        elif task_type == "image":
            return self._optimize_image_prompt(message)

        return message

    def _expand_short_prompt(self, message: str) -> str:
        """Add context to very short prompts."""
        return f"{message}\n\nProvide a thorough, detailed response."

    def _optimize_code_prompt(self, message: str) -> str:
        msg_lower = message.lower()

        if any(w in msg_lower for w in ["debug", "error", "fix", "bug", "traceback"]):
            return (
                f"{message}\n\n"
                "Instructions:\n"
                "1. Identify the exact root cause of this error\n"
                "2. Explain WHY this happens (not just what)\n"
                "3. Provide the corrected, complete code\n"
                "4. Add error handling for similar edge cases\n"
                "5. Suggest preventive practices"
            )

        if any(w in msg_lower for w in ["review", "improve", "refactor", "optimize"]):
            return (
                f"{message}\n\n"
                "Review for:\n"
                "1. Correctness — bugs, logic errors, edge cases\n"
                "2. Security — injection, XSS, data exposure\n"
                "3. Performance — time/space complexity, unnecessary operations\n"
                "4. Readability — naming, structure, documentation\n"
                "5. Provide improved code with explanations"
            )

        if any(w in msg_lower for w in ["explain", "how", "what does"]):
            return (
                f"{message}\n\n"
                "Explain:\n"
                "1. What this code does (high-level overview)\n"
                "2. How it works (step-by-step walkthrough)\n"
                "3. Key design decisions and patterns used\n"
                "4. Potential improvements or issues"
            )

        return (
            f"{message}\n\n"
            "Requirements:\n"
            "- Complete, runnable, production-ready code\n"
            "- Proper error handling and input validation\n"
            "- Clean structure following best practices\n"
            "- Type hints where applicable\n"
            "- Brief usage example"
        )

    def _optimize_math_prompt(self, message: str) -> str:
        return (
            f"{message}\n\n"
            "Solve step by step:\n"
            "1. State what's given and what we need to find\n"
            "2. Choose the appropriate method/formula\n"
            "3. Show each calculation step with clear working\n"
            "4. Box or highlight the final answer\n"
            "5. Verify the answer using a different method if possible"
        )

    def _optimize_research_prompt(self, message: str) -> str:
        return (
            f"{message}\n\n"
            "Research and present:\n"
            "1. Key findings with source citations\n"
            "2. Multiple perspectives on the topic\n"
            "3. Data points and statistics where available\n"
            "4. Practical implications and takeaways\n"
            "5. Note any limitations or uncertainties"
        )

    def _optimize_creative_prompt(self, message: str) -> str:
        return (
            f"{message}\n\n"
            "Create with:\n"
            "- Vivid, sensory language that engages the reader\n"
            "- Strong opening that hooks attention\n"
            "- Consistent tone and voice throughout\n"
            "- Satisfying structure with a clear arc\n"
            "- Original ideas and unique perspective"
        )

    def _optimize_reasoning_prompt(self, message: str) -> str:
        return (
            f"{message}\n\n"
            "Think through this systematically:\n"
            "1. What exactly is being asked?\n"
            "2. What are the key factors and constraints?\n"
            "3. Analyze from multiple angles\n"
            "4. Consider counter-arguments and edge cases\n"
            "5. Provide a well-reasoned conclusion with confidence level"
        )

    def _optimize_image_prompt(self, message: str) -> str:
        has_style = any(w in message.lower() for w in [
            "realistic", "cartoon", "anime", "oil painting", "watercolor",
            "digital art", "3d", "pixel", "sketch", "photographic",
        ])
        has_detail = len(message.split()) > 15

        additions = []
        if not has_style:
            additions.append("high quality, detailed")
        if not has_detail:
            additions.append("professional lighting, sharp focus")

        if additions:
            return f"{message}, {', '.join(additions)}"
        return message
