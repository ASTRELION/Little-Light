import discord
from discord.ext import tasks, commands
import pydest
import asyncio
import json

class LittleLightClient(commands.AutoShardedBot):
    """Little Light bot"""

    def __init__(self):
        self.config = self.read_config()
        super().__init__(
            command_prefix = self.config["prefix"]
        )

        self.load_extension("events")

    def read_config(self, file_name = "config.json"):
        """Read and return json configuration file"""
        try:
            with open(file_name) as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            print("Configuration file not found.")

    async def query_player(self):
        """Find a player with name"""
        destiny = pydest.Pydest(self.config["destiny"]["api_key"])
        json = await destiny.api.search_destiny_player(3, "ASTRELION")
        await destiny.close()
        print(json)