import pytest
from unittest.mock import MagicMock, patch
from MinecraftAgent import AgentManager, BaseAgent


class TestBaseAgent:
    def test_start_sets_active_to_true(self):
        with patch("MinecraftAgent.Minecraft.Minecraft.create") as mock_mc:
            agent = BaseAgent("TestAgent")
            agent.run = MagicMock()  # Evitamos ejecutar el bucle run
            agent.start()
            assert agent.active is True

    def test_stop_sets_active_to_false(self):
        with patch("MinecraftAgent.Minecraft.Minecraft.create") as mock_mc:
            agent = BaseAgent("TestAgent")
            agent.active = True
            agent.stop()
            assert agent.active is False

    def test_post_to_chat_calls_mc_method(self):
        with patch("MinecraftAgent.Minecraft.Minecraft.create") as mock_mc:
            mock_instance = mock_mc.return_value
            agent = BaseAgent("TestAgent")
            agent.postToChat("Hello")
            mock_instance.postToChat.assert_called_with("[TestAgent] Hello")


class TestAgentManager:
    def test_singleton_behavior(self):
        manager1 = AgentManager()
        manager2 = AgentManager()
        assert manager1 is manager2

    def test_register_adds_agents(self):
        manager = AgentManager()
        manager.kill_all()
        agent = MagicMock()
        manager.register(agent)
        assert agent in manager.agents

    def test_start_all_starts_all_agents(self):
        manager = AgentManager()
        manager.kill_all()
        agent1 = MagicMock()
        agent2 = MagicMock()
        manager.register(agent1)
        manager.register(agent2)

        manager.start_all()
        agent1.start.assert_called_once()
        agent2.start.assert_called_once()

    def test_stop_all_stops_all_agents(self):
        manager = AgentManager()
        manager.kill_all()
        agent1 = MagicMock()
        agent2 = MagicMock()
        manager.register(agent1)
        manager.register(agent2)

        manager.stop_all()
        agent1.stop.assert_called_once()
        agent2.stop.assert_called_once()

    def test_start_starts_specific_agent(self):
        manager = AgentManager()
        manager.kill_all()
        agent1 = MagicMock()
        manager.register(agent1)

        manager.start(0)
        agent1.start.assert_called_once()

    def test_stop_stops_specific_agent(self):
        manager = AgentManager()
        manager.kill_all()
        agent1 = MagicMock()
        manager.register(agent1)

        manager.stop(0)
        agent1.stop.assert_called_once()

    def test_kill_removes_and_stops_agent(self):
        manager = AgentManager()
        manager.kill_all()
        agent1 = MagicMock()
        manager.register(agent1)

        manager.kill(0)
        agent1.stop.assert_called_once()
        assert agent1 not in manager.agents

    def test_kill_all_removes_all(self):
        manager = AgentManager()
        agent1 = MagicMock()
        agent2 = MagicMock()
        manager.register(agent1)
        manager.register(agent2)
        assert len(manager.agents) > 0
        manager.kill_all()
        assert len(manager.agents) == 0
