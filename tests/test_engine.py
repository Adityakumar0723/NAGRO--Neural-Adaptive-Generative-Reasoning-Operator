"""Tests for NAGRO 4.1 core engine."""

import pytest
from nagro.core.models import TaskType, ChatRequest, MessageRole, Message, Conversation
from nagro.core.engine import NAGROEngine


@pytest.fixture
def engine():
    return NAGROEngine()


class TestTaskClassification:
    @pytest.mark.asyncio
    async def test_code_classification(self, engine):
        result = await engine.classify_task("Write a Python function to sort a list")
        assert result == TaskType.CODE

    @pytest.mark.asyncio
    async def test_image_classification(self, engine):
        result = await engine.classify_task("Generate image of a sunset")
        assert result == TaskType.IMAGE

    @pytest.mark.asyncio
    async def test_research_classification(self, engine):
        result = await engine.classify_task("Research the latest AI trends")
        assert result == TaskType.RESEARCH

    @pytest.mark.asyncio
    async def test_math_classification(self, engine):
        result = await engine.classify_task("Calculate the integral of x^2")
        assert result == TaskType.MATH

    @pytest.mark.asyncio
    async def test_creative_classification(self, engine):
        result = await engine.classify_task("Write a short story about space")
        assert result == TaskType.CREATIVE

    @pytest.mark.asyncio
    async def test_reasoning_classification(self, engine):
        result = await engine.classify_task("Why does the sky appear blue?")
        assert result == TaskType.REASONING

    @pytest.mark.asyncio
    async def test_default_chat(self, engine):
        result = await engine.classify_task("Hello there")
        assert result == TaskType.CHAT

    @pytest.mark.asyncio
    async def test_hindi_code_classification(self, engine):
        result = await engine.classify_task("code likho sorting ke liye")
        assert result == TaskType.CODE


class TestConversation:
    def test_conversation_creation(self, engine):
        conv = engine._get_or_create_conversation(None)
        assert conv.id is not None
        assert len(conv.messages) == 0

    def test_conversation_retrieval(self, engine):
        conv1 = engine._get_or_create_conversation(None)
        conv2 = engine._get_or_create_conversation(conv1.id)
        assert conv1.id == conv2.id


class TestEngineInfo:
    def test_info(self, engine):
        info = engine.info
        assert info["model"] == "NAGRO 4.1"
        assert info["version"] == "4.1.0"
        assert info["inference"] == "local"
        assert info["external_apis"] == "none"
        assert "capabilities" in info
        assert len(info["capabilities"]) > 0


class TestModels:
    def test_message_creation(self):
        msg = Message(role=MessageRole.USER, content="Hello")
        assert msg.role == MessageRole.USER
        assert msg.content == "Hello"

    def test_chat_request(self):
        req = ChatRequest(message="Test message")
        assert req.message == "Test message"
        assert req.stream is False

    def test_conversation_model(self):
        conv = Conversation()
        assert conv.id is not None
        assert len(conv.messages) == 0
