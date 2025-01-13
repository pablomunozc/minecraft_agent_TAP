[![Coverage Status](https://coveralls.io/repos/github/pablomunozc/minecraft_agent_TAP/badge.svg?branch=main)](https://coveralls.io/github/pablomunozc/minecraft_agent_TAP?branch=main)
# Minecraft Agent Framework

Pablo Muñoz Castro
Adrià Montagut Serres

Based on book: "Adventures in Minecraft" written by David Whale and Martin O'Hanlon, Wiley, 2017
 [http://eu.wiley.com/WileyCDA/WileyTitle/productCd-1119439582.html](http://eu.wiley.com/WileyCDA/WileyTitle/productCd-1119439582.html)

## Description

This repository implements a Python framework enabling the development and execution of Python coded agents in a Shared Minecraft server.

The structure of the project is as follows:

* minecraft_agent_TAP
  * Server : contains the pre-configured minecraft server and raspberry juice plugin
  * MyAdventures : folder to save the minecraft programs to
    * mcpi : python api library distributed with Minecraft: Pi Edition and minecraftstuff libraries
    * MinecraftAgent.py : python file that works as the agent framework
    * example.py : python file that has examples of different agents and includes everything to execute them
    * test_MinecraftAgent.py : python test file for MinecraftAgent.py
    * test_example.py : python test file for example.py
  * StartServer.bat : a batch file used to start the minecraft server

## The Framework

```
## AgentManager
The AgentManager class manages all the agents in the Minecraft server. This class is Singleton, so it is the only one which can exist to manage all the other agents.

register(agent):  Registers a new agent with the manager.  
start_all():  Activates and runs all registered agents.
stop_all():  Stops all registered agents.
start(): Starts the execution of a specific agent. It is called from BaseAgent.
stop(): Stops the execution of a specific agent. It is called from BaseAgent.
kill(): Stops and removes a specific agent registered at the position `agent_number`.
kill_all(): Stops and removes all registered agents.

---

## BaseAgent
The BaseAgent class is the class which all the agents inherits, and makes him interact with the Minecraft server.

start(): Activates the agent and starts its execution.
run(): The agent's main loop. While the agent is active, it repeatedly calls the `execute` method.
execute(): Abstract method that must be implemented by derived classes. Defines the actions the agent must do.  
stop(): Stops the agent's execution.
postToChat(message):  Sends a message to the Minecraft server's chat with the Agent name.
```

```

## Code coverage

The code has been tested using 'pytest'.

The file test_MinecraftAgent.py makes tests for MinecraftAgent.py, while test_example.py makes tests for example.py
