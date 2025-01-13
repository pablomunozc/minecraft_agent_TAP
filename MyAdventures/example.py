import MinecraftAgent
from mcpi import block as Block
from transformers import pipeline
import time

class CommandAgent(MinecraftAgent.BaseAgent):
    """ Agent that works as a connection between the AgentManager and Minecraft Chat
        It allows players to register and kill agents from within the game """
    def __init__(self, name, manager, list):
        """ Needs the manager and a list of agents [Class] that players can invoke """
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
                                        self.manager.register(new)
                                        new.start()
                                        self.postToChat("Started new " + a.__name__ + ": " + words[3])
                                        
                        case "list":
                            self.postToChat("There are currently " + str(len(self.manager.agents)) + " agents:")
                            for agent in self.manager.agents:
                                self.postToChat("   -> " + agent.name + " (" + type(agent).__name__ + ")")
                        case "kill":
                            if (len(words) < 3):
                                self.postToChat("Usage: !agent kill <agent name>")
                            elif (words[2] == self.name):
                                self.postToChat("You can't kill me!")
                            else:
                                agents = self.manager.agents.copy()
                                i = 0
                                for agent in agents:
                                    if (agent.name == words[2]):
                                        self.manager.kill(self.manager.agents.index(agent))
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

class GlassAgent(MinecraftAgent.BaseAgent):
    """ Agent that creates a glass platform at the player's feet """
    def execute(self):
        pos = self.mc.player.getTilePos()
        self.mc.setBlocks(pos.x-1,pos.y-1,pos.z-1,pos.x+1,pos.y-1,pos.z+1,Block.GLASS)

class TNTAgent(MinecraftAgent.BaseAgent):
    """ Agent that does a variety of things when certain messages are post to chat """
    def execute(self):
        chat = self.mc.events.pollChatPosts()
        for message in chat:
            if (message.message == "TNT"):
                """ Spawns a lit TNT on top of the player """
                self.postToChat("Beware of explosions!")
                pos = self.mc.entity.getTilePos(message.entityId)
                self.mc.setBlock(pos.x, pos.y+3, pos.z, Block.TNT)
                self.mc.setBlock(pos.x,pos.y+4,pos.z, 152)
                self.mc.setBlock(pos.x,pos.y+4,pos.z, Block.AIR)
            elif (message.message == "Up"):
                """ Teleports the player 30 blocks up """
                pos = self.mc.entity.getPos(message.entityId)
                self.mc.entity.setPos(message.entityId, pos.x, pos.y+30, pos.z)

class DiamondAgent(MinecraftAgent.BaseAgent):
    """ Agent that detects nearby diamond blocks and tells the player """
    def __init__(self, name):
        super().__init__(name)
        self.last_time = time.time()
        self.beeps = ["beep", "beep", "beeep", "beeeep", "BEEP", "It's there!", "Diamonds!", "Get them!", "Please get them", "You're right there", "So close yet so far"]
        self.index = 0

    def execute(self):
        pos = self.mc.player.getTilePos() 
        blocks = self.mc.getBlocks(pos.x-5, pos.y -5, pos.z-5, pos.x+5, pos.y+5,pos.z+5)
        if any(block == Block.DIAMOND_ORE.id for block in blocks):
            current_time = time.time()
            if (current_time - self.last_time >= 2):
                self.postToChat(self.beeps[self.index])
                self.last_time = current_time
                self.index = (self.index + 1) % len(self.beeps)

class ChatAgent(MinecraftAgent.BaseAgent):
    """ Agent that works as an AI Bot in chat
        The message must start with 'Hey <name>' to get a reply 
        Needs connection to the internet to download the AI model from huggingface, as well as 'transformers' and 'PyTorch'
        The model used can be changed at the programmer's will, but beware of disc space when doing so """
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


if __name__ == "__main__":
    manager = MinecraftAgent.AgentManager()
    manager.register(CommandAgent("Manager", manager, [TNTAgent, GlassAgent, DiamondAgent, ChatAgent]))
    manager.start_all()