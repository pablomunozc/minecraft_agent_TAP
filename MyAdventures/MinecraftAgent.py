from mcpi import minecraft as Minecraft
import threading

class AgentManager:
    _instance = None  # Variable de clase para almacenar la unica instancia

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'agents'):  # Evitar re-inicializacion
            self.agents = []

    def register(self, agent):
        self.agents.append(agent)

    def start_all(self):
        for agent in self.agents:
            agent.start()

    def stop_all(self):
        for agent in self.agents:
            agent.stop()

    def start(self, agent_number):
        self.agents[agent_number].start()
    
    def stop(self, agent_number):
        self.agents[agent_number].stop()
    
    def kill(self, agent_number):
        self.stop(agent_number)
        self.agents.remove(self.agents[agent_number])
    
    def kill_all(self):
        self.stop_all()
        self.agents.clear()

class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.active = False
        self.mc = Minecraft.Minecraft.create()

    def start(self):
        self.active = True
        threading.Thread(target=self.run).start()

    def run(self):
        while self.active:
            self.execute()

    def execute(self):
        raise NotImplementedError("This method should be overridden.")

    def stop(self):
        self.active = False

    def postToChat(self, message):
        self.mc.postToChat("["+self.name+"] " + message)



