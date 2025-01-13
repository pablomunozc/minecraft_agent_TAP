from mcpi import minecraft as Minecraft
import threading

class AgentManager:
    """ Main class for Minecraft Agent Framework
        Contains the agents that will execute from other threads """
    _instance = None  # Variable de clase para almacenar la unica instancia

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'agents'):  # Evitar re-inicializacion
            self.agents = []

    def register(self, agent):
        """ Registers an agent to the list """
        self.agents.append(agent)

    def start_all(self):
        """ Starts all agents on the list """
        for agent in self.agents:
            agent.start()

    def stop_all(self):
        """ Stops all agents on the list """
        for agent in self.agents:
            agent.stop()

    def start(self, agent_number):
        """ Starts an specific agent """
        self.agents[agent_number].start()
    
    def stop(self, agent_number):
        """ Stops an specific agent """
        self.agents[agent_number].stop()
    
    def kill(self, agent_number):
        """ Stops an specific agent and removes them from the list """
        self.stop(agent_number)
        self.agents.remove(self.agents[agent_number])
    
    def kill_all(self):
        """ Stops all agents and removes them from the list """
        self.stop_all()
        self.agents.clear()

class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.active = False
        self.mc = Minecraft.Minecraft.create()

    def start(self):
        """ Starts the agent """
        self.active = True
        threading.Thread(target=self.run).start()

    def run(self):
        """ The method that will execute the agent's work through another Thread """
        while self.active:
            self.execute()

    def execute(self):
        """ The method that needs to be overriden """
        raise NotImplementedError("This method should be overridden.")

    def stop(self):
        """ Stops the agent """
        self.active = False

    def postToChat(self, message):
        """ Shortcut from postToChat that also adds the name of the agent to it """
        self.mc.postToChat("["+self.name+"] " + message)



