"""
NAGRO 4.1 — Self-Reflection Engine.

Evaluates and improves the model's own outputs through iterative refinement.
"""

from __future__ import annotations


class SelfReflection:
    """
    Self-reflection system that evaluates responses and iteratively
    improves them until they meet quality thresholds.
    """

    REFLECT_PROMPT = """You are NAGRO 4.1's quality control system. Review this response critically.

ORIGINAL QUESTION: {question}

RESPONSE TO REVIEW:
{response}

Evaluate honestly:

1. **Accuracy:** Are there any factual errors or misleading statements?
2. **Completeness:** Did it miss anything important?
3. **Code Quality (if code):** Any bugs, security issues, or bad practices?
4. **Clarity:** Could it be explained better?
5. **Actionability:** Can the user actually use this?

If you find issues, provide a CORRECTED and IMPROVED response.
If the response is already excellent, respond with "QUALITY_APPROVED" followed by the response."""

    IMPROVE_CODE_PROMPT = """You are NAGRO 4.1's code quality engine. Review and improve this code.

ORIGINAL REQUEST: {question}

CODE TO REVIEW:
{code}

Check for:
1. **Bugs** — Logic errors, off-by-one, null/undefined handling
2. **Security** — Injection, XSS, path traversal, secrets exposure
3. **Performance** — Unnecessary loops, memory leaks, N+1 queries
4. **Best Practices** — Naming, structure, error handling, typing
5. **Edge Cases** — Empty input, large input, concurrent access

Provide the improved code with brief explanations of what you fixed."""

    FACT_CHECK_PROMPT = """You are NAGRO 4.1's fact-checking system.

CLAIM TO VERIFY:
{claim}

CONTEXT:
{context}

Evaluate:
1. Is this factually accurate based on your training data?
2. Could this be outdated?
3. Are there important nuances being missed?
4. What's the confidence level (high/medium/low)?

Provide your assessment with corrections if needed."""

    def build_reflection_prompt(self, question: str, response: str) -> str:
        return self.REFLECT_PROMPT.format(question=question, response=response)

    def build_code_review_prompt(self, question: str, code: str) -> str:
        return self.IMPROVE_CODE_PROMPT.format(question=question, code=code)

    def build_fact_check_prompt(self, claim: str, context: str = "") -> str:
        return self.FACT_CHECK_PROMPT.format(claim=claim, context=context)
