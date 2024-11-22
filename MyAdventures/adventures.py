from mcpi import minecraft as Minecraft
from mcpi import block as Block
import time

mc = Minecraft.Minecraft.create()

mc.postToChat("Hello Minecraft World")
 
pos = mc.player.getTilePos() 
mc.setBlock(pos.x+3, pos.y, pos.z, Block.BOOKSHELF.id) 
while True:
    pos = mc.player.getTilePos() 
    blocks = mc.getBlocks(pos.x-5, pos.y -5, pos.z-5, pos.x+5, pos.y+5,pos.z+5)
    for block in blocks:
        if block == Block.DIAMOND_ORE.id:
            mc.postToChat("DIAMANTEEEEE")
    time.sleep(0.5)