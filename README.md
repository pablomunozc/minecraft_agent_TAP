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
in development
```

## Code coverage

The code has been tested using 'pytest'.

The file test_MinecraftAgent.py makes tests for MinecraftAgent.py, while test_example.py makes tests for example.py
