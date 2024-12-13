from mcpi import block as Block
from mcpi import minecraft as Minecraft
from mcpi.vec3 import Vec3
import threading
import time

class BlockPos:
    """Clase que guarda la informacion del bloque, incluyendo posicion"""
    def __init__(self, id, data, pos):
        self.id=id
        self.data=data
        pos=pos
    
class API:
    def __init__(self):
        self.mcpi = Minecraft.Minecraft.create()
    
    def getBlock(self, x, y, z):
        """Get block (x,y,z) => block:BlockPos"""
        block = self.mcpi.getBlockWithData(x,y,z)
        return BlockPos(block.id, block.data, Vec3(x,y,z))
    
    def getBlocks(self, x0, y0, z0, x1, y1, z1):
        """Get a cuboid of blocks (x0,y0,z0,x1,y1,z1) => [block:BlockPos]"""
        blockPoss = []
        for y in range(y1-y0+1):
            for z in range(z1-z0+1):
                for x in range(x1-x0+1):
                    blockPoss.append(self.getBlock(x0+x, y0+y, z0+z))
        return blockPoss
    
    def replaceBlocks(self, x0, y0, z0, x1, y1, z1, inBlockId, outBlockId):
        blocks = self.getBlocks(x0, y0, z0, x1, y1, z1)
        for block in blocks:
            if block.id == inBlockId:
                self.setBlock(block.pos.x, block.pos.y, block.pos.z, outBlockId)

    def setBlock(self, *args):
        """Set block (x,y,z,id,[data])"""
        self.mcpi.setBlock(args)

    def getPlayer(self):
        return self.mcpi.player
    
    def postToChat(self, msg):
        """Post a message to the game chat"""
        self.mcpi.postToChat(msg)

    def setting(self, setting, status):
        """Set a world setting (setting, status). keys: world_immutable, nametags_visible"""
        self.mcpi.setting(setting, status)

    def getHeight(self, *args):
        """Get the height of the world (x,z) => int"""
        return self.mcpi.getHeight(args)

    def getPlayerEntityIds(self):
        """Get the entity ids of the connected players => [id:int]"""
        return self.mcpi.getPlayerEntityIds()

    def getPlayerEntityId(self, name):
        """Get the entity id of the named player => [id:int]"""
        return self.mcpi.getPlayerEntityId()

    def saveCheckpoint(self):
        """Save a checkpoint that can be used for restoring the world"""
        self.mcpi.saveCheckpoint()

    def restoreCheckpoint(self):
        """Restore the world state to the checkpoint"""
        self.mcpi.restoreCheckpoint()

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
        self.running = False



