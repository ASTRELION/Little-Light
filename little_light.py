import discord
from discord.ext import tasks, commands
from destiny import Destiny

import pydest
import asyncio
import json
import sys

class LittleLightClient(commands.AutoShardedBot):
    """Little Light client"""

    def __init__(self):
        # Load configuration
        self.config = self.read_config()

        super().__init__(
            command_prefix = self.config["prefix"]
        )

        self.destiny = Destiny(self)

        extensions = [
            "events",
            "player"
        ]
        
        # Load extensions
        for extension in extensions:
            self.load_extension(extension)

    # Skip built in on_message so events.on_message gets called instead
    async def on_message(self, message): pass

    # config.json operations #

    def read_config(self, file_name: str = "config.json"):
        """Read and return json configuration file"""
        try:
            with open(file_name) as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            sys.exit("Configuration file not found.")

    def write_config(self, file_name: str = "config.json"): pass

    # user.json operations #

    def write_user(self, user: discord.User, memberships: dict):
        """Write user membership ID to file"""
        data = self.read_users()
        for m in memberships:
            data[str(user.id)][m] = memberships[m]

        with open("users.json", "w", encoding = "utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii = False, indent = 4)

    def write_users(self, user: discord.User, memberships: dict):
        """Writes base users.json file"""
        data = {}
        data[user.id] = memberships
        with open("users.json", "w", encoding = "utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii = False, indent = 4)

    def read_users(self):
        """Read entire users.json file into dictionary"""
        try:
            with open("users.json") as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            print("users.json not found. Creating a new one...")
            user_data = {}
            self.write_users(self.user, user_data)
            return self.read_users()