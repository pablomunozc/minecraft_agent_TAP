import pytest
from unittest.mock import MagicMock, patch
from MinecraftAgent import AgentManager
from example import CommandAgent, GlassAgent, TNTAgent, DiamondAgent, ChatAgent
from mcpi import block as Block
from mcpi import vec3 as Vec3


@pytest.fixture
def mock_manager():
    return AgentManager()


@pytest.fixture
def mock_minecraft():
    with patch("MinecraftAgent.Minecraft.Minecraft.create") as mock_mc:
        yield mock_mc.return_value


class TestCommandAgent:
    def test_register_agent_command(self, mock_manager, mock_minecraft):
        mock_minecraft.events.pollChatPosts.return_value = [
            MagicMock(message="!agent register GlassAgent TestGlass")
        ]
        command_agent = CommandAgent("CommandAgent", mock_manager, [GlassAgent])
        command_agent.execute()

        assert len(mock_manager.agents) == 1
        assert mock_manager.agents[0].name == "TestGlass"

    def test_list_agents_command(self, mock_manager, mock_minecraft):
        mock_manager.register(GlassAgent("Glass1"))
        mock_minecraft.events.pollChatPosts.return_value = [
            MagicMock(message="!agent list")
        ]
        command_agent = CommandAgent("CommandAgent", mock_manager, [GlassAgent])
        command_agent.postToChat = MagicMock()
        command_agent.execute()

        command_agent.postToChat.assert_any_call("   -> Glass1 (GlassAgent)")

    def test_kill_agent_command(self, mock_manager, mock_minecraft):
        mock_agent = MagicMock(name="MockAgent", spec=GlassAgent)
        mock_agent.name = "Glass1"
        mock_manager.kill_all()
        mock_manager.register(mock_agent)
        mock_minecraft.events.pollChatPosts.return_value = [
            MagicMock(message="!agent kill Glass1")
        ]
        command_agent = CommandAgent("CommandAgent", mock_manager, [GlassAgent])
        command_agent.execute()

        assert len(mock_manager.agents) == 0
        mock_agent.stop.assert_called_once()

    def test_help_command(self, mock_manager, mock_minecraft):
        mock_minecraft.events.pollChatPosts.return_value = [
            MagicMock(message="!agent help")
        ]
        command_agent = CommandAgent("CommandAgent", mock_manager, [GlassAgent])
        command_agent.postToChat = MagicMock()
        command_agent.execute()

        command_agent.postToChat.assert_any_call("Manager commands:")
        command_agent.postToChat.assert_any_call("   -> register: registers a new Agent from a set list")
        command_agent.postToChat.assert_any_call("   -> list: returns the list of current agents")
        command_agent.postToChat.assert_any_call("   -> kill: stops an active agent")


class TestGlassAgent:
    def test_glass_platform(self, mock_minecraft):
        mock_minecraft.player.getTilePos.return_value = MagicMock(x=0, y=10, z=0)
        glass_agent = GlassAgent("GlassAgent")
        glass_agent.mc = mock_minecraft

        glass_agent.execute()

        mock_minecraft.setBlocks.assert_called_once_with(
            -1, 9, -1, 1, 9, 1, Block.GLASS
        )


class TestTNTAgent:
    def test_tnt_spawn(self, mock_minecraft):
        mock_minecraft.events.pollChatPosts.return_value = [
            MagicMock(message="TNT", entityId=1)
        ]
        mock_minecraft.entity.getTilePos.return_value = MagicMock(x=0, y=10, z=0)
        tnt_agent = TNTAgent("TNTAgent")
        tnt_agent.mc = mock_minecraft

        tnt_agent.execute()

        mock_minecraft.setBlock.assert_any_call(0, 13, 0, Block.TNT)


class TestDiamondAgent:
    def test_detect_diamond_blocks(self, mock_minecraft):
        mock_minecraft.player.getTilePos.return_value = MagicMock(x=0, y=10, z=0)
        mock_minecraft.getBlocks.return_value = [Block.DIAMOND_ORE.id]
        diamond_agent = DiamondAgent("DiamondAgent")
        diamond_agent.mc = mock_minecraft
        diamond_agent.last_time = diamond_agent.last_time - 5
        diamond_agent.postToChat = MagicMock()

        diamond_agent.execute()

        diamond_agent.postToChat.assert_called_once_with("beep")


class TestChatAgent:
    @patch("example.pipeline")
    def test_chat_reply(self, mock_pipeline, mock_minecraft):
        mock_pipeline.return_value.return_value = [
            {"generated_text": "Hello, how can I help you?"}
        ]
        mock_minecraft.events.pollChatPosts.return_value = [
            MagicMock(message="Hey ChatAgent help", entityId=1)
        ]
        chat_agent = ChatAgent("ChatAgent")
        chat_agent.mc = mock_minecraft
        chat_agent.postToChat = MagicMock()

        chat_agent.execute()

        chat_agent.postToChat.assert_called_once_with("Hello, how can I help you?")
