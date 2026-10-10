"""
NAGRO 4.1 — Agentic Loop System.

Multi-step autonomous agent that can plan, use tools, reflect,
and iterate until the task is complete.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

from nagro.reasoning.chain_of_thought import ChainOfThought
from nagro.reasoning.self_reflection import SelfReflection
from nagro.reasoning.planner import TaskPlanner, TaskStatus


@dataclass
class AgentStep:
    """A single step in the agentic loop."""
    step_number: int
    thought: str
    action: str
    action_input: str
    observation: str = ""
    is_final: bool = False


@dataclass
class AgentTrace:
    """Complete trace of an agentic execution."""
    task: str
    steps: list[AgentStep] = field(default_factory=list)
    final_answer: str = ""
    total_steps: int = 0

    def add_step(self, step: AgentStep):
        self.steps.append(step)
        self.total_steps = len(self.steps)


class AgenticLoop:
    """
    NAGRO 4.1's autonomous agent system.

    Implements ReAct (Reasoning + Acting) pattern:
    1. Think about what to do
    2. Choose an action (tool)
    3. Execute the action
    4. Observe the result
    5. Decide if done or need more steps
    """

    REACT_PROMPT = """You are NAGRO 4.1, an autonomous AI agent. You solve complex tasks step by step.

You have access to these tools:
{tools_description}

Use this exact format for each step:

THOUGHT: [What you're thinking about, what you need to do next]
ACTION: [tool name]
ACTION_INPUT: [input for the tool]

When you have the final answer:
THOUGHT: [I now have enough information to answer]
FINAL_ANSWER: [Your complete, well-formatted answer]

Rules:
- Always think before acting
- Use tools when you need real information
- Don't guess when you can look it up
- Verify important claims
- Maximum {max_steps} steps

TASK: {task}

Previous steps:
{history}

Continue from here:"""

    AVAILABLE_TOOLS = {
        "search": "Search the web for information. Input: search query.",
        "calculate": "Perform mathematical calculations. Input: math expression.",
        "code_run": "Execute Python code safely. Input: Python code.",
        "analyze": "Analyze text or data deeply. Input: text to analyze.",
        "summarize": "Summarize long text. Input: text to summarize.",
    }

    def __init__(self, max_steps: int = 10):
        self.max_steps = max_steps
        self.cot = ChainOfThought()
        self.reflection = SelfReflection()
        self.planner = TaskPlanner()

    def build_react_prompt(
        self,
        task: str,
        history: list[AgentStep] | None = None,
    ) -> str:
        """Build the ReAct prompt with history."""
        tools_desc = "\n".join(
            f"- {name}: {desc}" for name, desc in self.AVAILABLE_TOOLS.items()
        )

        history_text = ""
        if history:
            for step in history:
                history_text += f"\nTHOUGHT: {step.thought}\n"
                if step.is_final:
                    history_text += f"FINAL_ANSWER: {step.action_input}\n"
                else:
                    history_text += f"ACTION: {step.action}\n"
                    history_text += f"ACTION_INPUT: {step.action_input}\n"
                    history_text += f"OBSERVATION: {step.observation}\n"

        return self.REACT_PROMPT.format(
            tools_description=tools_desc,
            max_steps=self.max_steps,
            task=task,
            history=history_text or "None yet.",
        )

    def parse_step(self, llm_output: str) -> AgentStep:
        """Parse the LLM's output into a structured AgentStep."""
        lines = llm_output.strip().split("\n")

        thought = ""
        action = ""
        action_input = ""
        is_final = False

        for line in lines:
            line = line.strip()
            if line.upper().startswith("THOUGHT:"):
                thought = line[8:].strip()
            elif line.upper().startswith("ACTION:"):
                action = line[7:].strip()
            elif line.upper().startswith("ACTION_INPUT:"):
                action_input = line[13:].strip()
            elif line.upper().startswith("FINAL_ANSWER:"):
                action_input = line[13:].strip()
                is_final = True

        return AgentStep(
            step_number=0,
            thought=thought,
            action=action,
            action_input=action_input,
            is_final=is_final,
        )

    async def execute_tool(self, tool_name: str, tool_input: str) -> str:
        """Execute a tool and return the observation."""
        tool_name = tool_name.lower().strip()

        if tool_name == "search":
            from nagro.tools.web_search import search_web
            results = await search_web(tool_input, num_results=3)
            if not results:
                return "No results found."
            return "\n".join(
                f"- {r['title']}: {r['snippet']}" for r in results
            )

        elif tool_name == "calculate":
            from nagro.tools.calculator import safe_calculate
            return safe_calculate(tool_input)

        elif tool_name == "code_run":
            from nagro.tools.code_executor import execute_python
            result = execute_python(tool_input)
            if result["success"]:
                return result["output"] or "Code executed successfully (no output)."
            return f"Error: {result['error']}"

        elif tool_name == "analyze":
            return f"[Analysis of input — handled by LLM reasoning in next step]"

        elif tool_name == "summarize":
            return f"[Summary task — handled by LLM in next step]"

        return f"Unknown tool: {tool_name}"
