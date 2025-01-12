import MinecraftAgent
from mcpi import block as Block
from transformers import pipeline
import time
import re

class MainAgent(MinecraftAgent.BaseAgent):
    def __init__(self, name, manager, list):
        super().__init__(name)
        self.manager = manager
        self.agent_list = list

    def execute(self):
        chat = self.mc.events.pollChatPosts()
        for message in chat:
                words = message.message.split()
                if (words[0] == "!agent"):
                    match (words[1]):
                        case "register":
                            if (len(words) < 3):
                                self.postToChat("Usage: !agent register <agent_class> <agent_name>")
                                self.postToChat("For a list of possible agent classes, check '!agent register list'")
                            elif (words[2] == "list"):
                                self.postToChat("List of possible agent classes:")
                                for a in self.agent_list:
                                    self.postToChat("   -> " + a.__name__)
                            elif (len(words) < 4):
                                self.postToChat("Usage: !agent register <agent_class> <agent_name>")
                                self.postToChat("For a list of possible agent classes, check '!agent register list'")
                            else:
                                for a in self.agent_list:
                                    if (a.__name__ == words[2]):
                                        new = a(words[3])
                                        manager.register(new)
                                        new.start()
                                        self.postToChat("Started new " + a.__name__ + ": " + words[3])
                                        
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
                                i = 0
                                for agent in agents:
                                    if (agent.name == words[2]):
                                        manager.kill(manager.agents.index(agent))
                                        self.postToChat("Killed " + agent.name + " agent")
                                        i = i + 1
                                if (i == 0):
                                    self.postToChat("Agent named " + words[2] + " not found")
                        case "help":
                            self.postToChat("Manager commands:")
                            self.postToChat("   -> register: registers a new Agent from a set list")
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

class ChatAgent(MinecraftAgent.BaseAgent):
    def __init__(self, name):
        super().__init__(name)
        self.chatbot=pipeline(task="text2text-generation", model="facebook/blenderbot-400M-distill")
    def execute(self):
        chat = self.mc.events.pollChatPosts()
        for message in chat:
            palabras=message.message.split()
            if palabras[0]=="Hey" and palabras[1]==self.name:
                user_message="".join(palabras[2:])
                for text in self.chatbot(user_message, max_new_tokens=100):
                    self.postToChat(text["generated_text"])



manager = MinecraftAgent.AgentManager()
manager.register(MainAgent("Manager", manager, [DiamondAgent, TestAgent, ChatAgent]))
manager.start_all()