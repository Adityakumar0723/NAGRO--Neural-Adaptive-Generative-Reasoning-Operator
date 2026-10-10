"""
NAGRO 4.1 — Chain-of-Thought & Tree-of-Thought Reasoning Engine.

Advanced multi-step reasoning that breaks problems into logical steps,
explores multiple solution paths, and selects the best answer.
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class ThoughtNode:
    """A single node in the reasoning tree."""
    content: str
    confidence: float = 0.0
    children: list[ThoughtNode] = field(default_factory=list)
    evaluation: str = ""
    is_final: bool = False


class ChainOfThought:
    """
    Implements Chain-of-Thought and Tree-of-Thought reasoning.

    Breaks complex problems into sequential reasoning steps,
    evaluates each step, and constructs a logical chain to the answer.
    """

    COT_PROMPT = """You are NAGRO 4.1's deep reasoning engine. Think through this problem step by step.

PROBLEM: {problem}

Follow this exact reasoning framework:

**STEP 1 — UNDERSTAND:**
What exactly is being asked? Identify the core question, constraints, and what a complete answer looks like.

**STEP 2 — DECOMPOSE:**
Break the problem into smaller sub-problems. List each one.

**STEP 3 — ANALYZE:**
For each sub-problem, reason through it carefully. Show your work.

**STEP 4 — SYNTHESIZE:**
Combine your findings into a coherent answer.

**STEP 5 — VERIFY:**
Check your answer. Are there edge cases? Could you be wrong? What assumptions did you make?

**FINAL ANSWER:**
Provide your complete, well-reasoned answer.

Think deeply. Be thorough. Show your reasoning at every step."""

    EVALUATE_PROMPT = """Evaluate the quality of this reasoning and answer.

ORIGINAL PROBLEM: {problem}

PROPOSED ANSWER:
{answer}

Rate on these dimensions (1-10):
1. **Correctness** — Is the answer factually correct?
2. **Completeness** — Does it fully address the question?
3. **Clarity** — Is the explanation clear and well-structured?
4. **Depth** — Does it show genuine understanding?
5. **Practical Value** — Is it actually useful to the person?

If the score is below 7 on any dimension, provide an IMPROVED answer.
If it's good, confirm with "APPROVED" and repeat the answer."""

    def build_cot_prompt(self, problem: str) -> str:
        """Build a chain-of-thought prompt for the given problem."""
        return self.COT_PROMPT.format(problem=problem)

    def build_evaluation_prompt(self, problem: str, answer: str) -> str:
        """Build a self-evaluation prompt."""
        return self.EVALUATE_PROMPT.format(problem=problem, answer=answer)

    def build_multi_perspective_prompt(self, problem: str) -> str:
        """Generate prompt that considers multiple perspectives."""
        return f"""You are NAGRO 4.1. Analyze this from multiple perspectives:

PROBLEM: {problem}

**Perspective 1 — Technical/Analytical:**
What does logic, data, and evidence say?

**Perspective 2 — Practical:**
What actually works in the real world? What are the constraints?

**Perspective 3 — Creative/Alternative:**
What unconventional approaches exist? What are people missing?

**Synthesis:**
Combine the strongest insights from each perspective into a comprehensive answer.

**Confidence Level:** How confident are you? What are the key uncertainties?"""

    def build_debate_prompt(self, problem: str) -> str:
        """Internal debate between different reasoning approaches."""
        return f"""You are NAGRO 4.1. Conduct an internal debate about this problem:

PROBLEM: {problem}

**ADVOCATE (argues FOR the most obvious answer):**
Present the strongest case for the conventional answer.

**CRITIC (challenges the obvious answer):**
What could be wrong? What assumptions are being made? Play devil's advocate.

**JUDGE (evaluates both sides):**
Who made better arguments? Where does the truth lie?

**FINAL VERDICT:**
The most well-reasoned answer, acknowledging nuance and uncertainty."""
