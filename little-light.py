import discord
from discord.ext import tasks, commands

import json

class LittleLightClient(discord.AutoShardedClient):
    """Little Light bot"""

    def __init__(self):
        self.config = self.read_config()

        super().__init__(
            command_prefix = self.config["prefix"]
        )

    def read_config(self, file_name = "config.json"):
        """Read and return json configuration file"""
        try:
            with open(file_name) as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            print("Configuration file not found.")

    async def on_ready(self):
        print("Logged in as {}!".format(self.user))

    async def on_message(self, message: discord.Message):
        print("Message from {}: {}".format(message.author, message.content))

client = LittleLightClient()
client.run(client.config["token"], bot = True, reconnect = True)