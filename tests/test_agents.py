"""Tests for NAGRO 4.1 agents."""

import pytest
from nagro.agents.router import AgentRouter
from nagro.agents.reasoning import ReasoningAgent
from nagro.agents.coding import CodingAgent
from nagro.agents.research import ResearchAgent
from nagro.agents.image import ImageAgent
from nagro.agents.math_agent import MathAgent
from nagro.agents.creative import CreativeAgent
from nagro.core.models import TaskType


class TestAgentRouter:
    def test_router_initialization(self):
        router = AgentRouter()
        assert len(router.available_agents) > 0

    def test_get_coding_agent(self):
        router = AgentRouter()
        agent = router.get_agent(TaskType.CODE)
        assert isinstance(agent, CodingAgent)

    def test_get_research_agent(self):
        router = AgentRouter()
        agent = router.get_agent(TaskType.RESEARCH)
        assert isinstance(agent, ResearchAgent)

    def test_get_image_agent(self):
        router = AgentRouter()
        agent = router.get_agent(TaskType.IMAGE)
        assert isinstance(agent, ImageAgent)

    def test_get_math_agent(self):
        router = AgentRouter()
        agent = router.get_agent(TaskType.MATH)
        assert isinstance(agent, MathAgent)

    def test_get_creative_agent(self):
        router = AgentRouter()
        agent = router.get_agent(TaskType.CREATIVE)
        assert isinstance(agent, CreativeAgent)

    def test_fallback_to_chat(self):
        router = AgentRouter()
        agent = router.get_agent(TaskType.CHAT)
        assert isinstance(agent, ReasoningAgent)


class TestCodingAgent:
    def test_enhance_debug_prompt(self):
        agent = CodingAgent()
        enhanced = agent._enhance_coding_prompt("debug this error in my code")
        assert "root cause" in enhanced.lower()

    def test_enhance_review_prompt(self):
        agent = CodingAgent()
        enhanced = agent._enhance_coding_prompt("review this code for issues")
        assert "performance" in enhanced.lower() or "bugs" in enhanced.lower()

    def test_enhance_general_prompt(self):
        agent = CodingAgent()
        enhanced = agent._enhance_coding_prompt("write a hello world program")
        assert "production-ready" in enhanced.lower()
