[![Coverage Status](https://coveralls.io/repos/github/pablomunozc/minecraft_agent_TAP/badge.svg)](https://coveralls.io/github/pablomunozc/minecraft_agent_TAP?branch=main)
# Minecraft Agent Framework

Pablo Muñoz Castro | Adrià Montagut Serres

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

### AgentManager
The AgentManager class manages all the agents in the Minecraft server. This class is Singleton, so it is the only one which can exist to manage all the other agents.

* register(agent):  Registers a new agent with the manager.  
* start_all():  Activates and runs all registered agents.
* stop_all():  Stops all registered agents.
* start(): Starts the execution of a specific agent. It is called from BaseAgent.
* stop(): Stops the execution of a specific agent. It is called from BaseAgent.
* kill(): Stops and removes a specific agent registered at the position "agent_number".
* kill_all(): Stops and removes all registered agents.


### BaseAgent
The BaseAgent class is the class which all the agents inherits, and makes him interact with the Minecraft server.

* start(): Activates the agent and starts its execution.
* run(): The agent's main loop. While the agent is active, it repeatedly calls the "execute" method.
* execute(): Abstract method that must be implemented by derived classes. Defines the actions the agent must do.  
* stop(): Stops the agent's execution.
* postToChat(message):  Sends a message to the Minecraft server's chat with the Agent name.


## Agent examples

### Command Agent
The Command Agent works as a connection between the AgentManager and Minecraft Chat. It allows players to register and kill agents from within the game. To use the commands ingame, the player must post a message in chat starting with `!agent`, and has commands like `!agent list`, `!agent register` and `!agent kill`.

### Glass Agent
The Glass Agent is a simple bot that creates a glass platform at the player's feet at any moment.

### TNT Agent
The TNT Agent reads messages from ingame chat and activates when certain words are said. Sending `TNT` will spawn a lit TNT on top of the player that wrote the message, while sending `Up` will teleport the same player 30 blocks up.

### Diamond Agent
The Diamond Agent detects nearby diamond ores from the player and writes messages in chat about it, like some sort of metal detector. It also gets pretty nervous when you take time to reach the diamonds.

### Chat Agent
The Chat Agent reads messages from ingame chat and processes them in a IA language model, returning a resulting phrase. All messages directed to him must start with `Hey <name>`.

For this Agent to work some dependencies are required:
* Python 3.9-3.12
* Transformers
* Pytorch

The model is then downloaded locally. The model used as an example is `facebook/blenderbot-400M-distill` from huggingface, but it can be changed to whatever model you like.


## Code coverage

The code has been tested using 'pytest'.

The file test_MinecraftAgent.py makes tests for MinecraftAgent.py, while test_example.py makes tests for example.py

Also, the repository has a Github Action that updates the code coverage percentage every time a push is made, using pytest, pytest-cov and coveralls:
[![Coverage Status](https://coveralls.io/repos/github/pablomunozc/minecraft_agent_TAP/badge.svg)](https://coveralls.io/github/pablomunozc/minecraft_agent_TAP?branch=main)
