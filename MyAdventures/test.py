import MinecraftAgent
from mcpi import block as Block
import time
import re

class MainAgent(MinecraftAgent.BaseAgent):
    def execute(self):
        chat = self.mc.events.pollChatPosts()
        for message in chat:
            if (message.message.startsWith("!")):
                m = re.match(r"!(\w+)", message.message).group(1)
                if (m.startsWith("create")):
                    self.mc.postToChat("Que grande loquete")

class TestAgent(MinecraftAgent.BaseAgent):
    def execute(self):
        pos = self.mc.player.getTilePos()
        self.mc.setBlocks(pos.x-1,pos.y-1,pos.z-1,pos.x+1,pos.y-1,pos.z+1,Block.GLASS)

class DiamondAgent(MinecraftAgent.BaseAgent):
    def execute(self):
        chat = self.mc.events.pollChatPosts()
        for message in chat:
            if (message.message == "Hola"):
                self.mc.postToChat("<"+self.name+"> Tus muertos")
                pos = self.mc.entity.getTilePos(message.entityId)
                self.mc.setBlock(pos.x, pos.y+3, pos.z, Block.TNT)
                self.mc.setBlock(pos.x,pos.y+4,pos.z, 152)
                self.mc.setBlock(pos.x,pos.y+4,pos.z, Block.AIR)
            elif (message.message == "Adios"):
                pos = self.mc.entity.getPos(message.entityId)
                self.mc.entity.setPos(message.entityId, pos.x, pos.y+30, pos.z)
            else:
                self.mc.postToChat(message.message)


manager = MinecraftAgent.AgentManager()
manager.register(MainAgent("Servidor"))
manager.register(TestAgent("Carlitos"))
manager.register(DiamondAgent("Carlota"))
manager.start_all()