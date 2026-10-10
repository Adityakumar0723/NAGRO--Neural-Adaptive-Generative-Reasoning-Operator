"""Agent router for NAGRO 4.1 - Routes tasks to specialized agents."""

from __future__ import annotations

from nagro.core.models import TaskType
from nagro.agents.base import BaseAgent
from nagro.agents.reasoning import ReasoningAgent
from nagro.agents.coding import CodingAgent
from nagro.agents.research import ResearchAgent
from nagro.agents.image import ImageAgent
from nagro.agents.math_agent import MathAgent
from nagro.agents.creative import CreativeAgent


class AgentRouter:
    """Routes incoming requests to the appropriate specialized agent."""

    def __init__(self):
        self._agents: dict[TaskType, BaseAgent] = {
            TaskType.CHAT: ReasoningAgent(),
            TaskType.REASONING: ReasoningAgent(),
            TaskType.CODE: CodingAgent(),
            TaskType.RESEARCH: ResearchAgent(),
            TaskType.IMAGE: ImageAgent(),
            TaskType.MATH: MathAgent(),
            TaskType.CREATIVE: CreativeAgent(),
        }

    def get_agent(self, task_type: TaskType) -> BaseAgent:
        return self._agents.get(task_type, self._agents[TaskType.CHAT])

    @property
    def available_agents(self) -> list[str]:
        return [agent.name for agent in self._agents.values()]
