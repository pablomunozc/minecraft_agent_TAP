import MinecraftAgent
from mcpi import block as Block
from transformers import pipeline
import time
import re

class MainAgent(MinecraftAgent.BaseAgent):
    def __init__(self, name, manager):
        super().__init__(name)
        self.manager = manager

    def execute(self):
        chat = self.mc.events.pollChatPosts()
        for message in chat:
                words = message.message.split()
                if (words[0] == "!agent"):
                    match (words[1]):
                        case "create":
                            self.postToChat("not implemented yet")
                        case "list":
                            self.postToChat("There are currently " + str(len(manager.agents)) + " agents:")
                            for agent in manager.agents:
                                self.postToChat("   -> " + agent.name + " (" + type(agent).__name__ + ")")
                        case "kill":
                            if (len(words) < 3):
                                self.postToChat("Usage: !agent kill <agent name>")
                            elif (words[2] == self.name):
                                self.postToChat("You can't kill me!")
                            else:
                                agents = manager.agents.copy()
                                for agent in agents:
                                    if (agent.name == words[2]):
                                        manager.kill(manager.agents.index(agent))
                                        self.postToChat("Killed " + agent.name + " agent")
                        case "help":
                            self.postToChat("Manager commands:")
                            self.postToChat("   -> create: creates a new Agent")
                            self.postToChat("   -> list: returns the list of current agents")
                            self.postToChat("   -> kill: stops an active agent")
                        case _:
                            self.postToChat("Unknown command, write '!agent help' for more information")



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

class ChatBot(MinecraftAgent.BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        self.chatbot=pipeline(task="text2text-generation", model="facebook/blenderbot-400M-distill")
    def execute(self):
        chat = self.mc.events.pollChatPosts()
        for message in chat:
            if message.message[0]!='!':
                user_message=message.message
                for text in self.chatbot(user_message, max_new_tokens=100):
                    self.postToChat(text["generated_text"])



manager = MinecraftAgent.AgentManager()
manager.register(MainAgent("Manager", manager))
manager.register(DiamondAgent("Carlota"))
manager.register(ChatBot("Jesus"))
manager.start_all()