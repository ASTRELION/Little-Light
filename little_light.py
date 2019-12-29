import discord
from discord.ext import commands
from destiny import Destiny

import pydest
import asyncio
import json
import sys
import logging

class LittleLightClient(commands.AutoShardedBot):
    """Little Light client"""

    def __init__(self):
        # Configuration files
        self.config = self.read_json_file("config.json")
        self.ghost_dialog = self.read_json_file(self.config["dialog_file"])
        # Data file paths
        self.DATA_PATH = self.config["data_path"]
        self.GUILDS_PATH = self.DATA_PATH + "guilds/"
        self.USERS_PATH = self.DATA_PATH + "users/"

        super().__init__(
            command_prefix = self.config["command_prefix"]
        )

        # Init Destiny API
        self.destiny = Destiny(self)

        # Setup logging
        self.logger = logging.getLogger("LittleLightLogger")
        self.logger.setLevel(logging.DEBUG)

        fh = logging.FileHandler("littlelight.log")
        fh.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s:%(levelname)s$ %(message)s", 
            "%Y-%m-%d::%H:%M:%S"
        )
        
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

        # Load extensions
        for extension in self.config["extensions"]:
            self.load_extension(extension)
            self.logger.debug("Loaded {} module".format(extension))

    # Skip built-in on_message so events.on_message gets called instead
    async def on_message(self, message): pass

    # Generic File Operations #

    def read_json_file(self, file_name: str):
        """Read and return given json file as a dictionary object"""
        try:
            with open(file_name) as json_file:
                return json.load(json_file)
        except FileNotFoundError:
            self.logger.warning("File {} not found. Creating a new one...".format(file_name))
            self.write_json_file(file_name, {})
            return self.read_json_file(file_name)

    def write_json_file(self, file_name: str, data: dict):
        """Write a json file from dictionary object"""
        try:
            with open(file_name, "w", encoding = "utf-8") as json_file:
                json.dump(data, json_file, ensure_ascii = False, indent = 4)
        except:
            self.logger.error("File {} could not be written!".format(file_name))

    def get_discord_color(self, rgb: list):
        """Return a discord.Color from an RGB list"""
        return discord.Color.from_rgb(
            rgb[0],
            rgb[1],
            rgb[2]
        )

    # User Data Operations #

    def write_user(self, user: discord.User, data: dict):
        """Write user to file"""
        data["user_id"] = user.id
        data["user_name"] = str(user)

        self.write_json_file(self.USERS_PATH + "u{}.json".format(user.id), data)

    def read_user(self, user: discord.User):
        """Read user into dict object"""
        return self.read_json_file(self.USERS_PATH + "u{}.json".format(user.id))

    # Guild Data Operations #

    async def write_guild(self, guild: discord.Guild, data: dict):
        """Write a guild to file"""
        data["guild_id"] = guild.id
        data["guild_name"] = guild.name
        data["member_count"] = len(guild.members)

        # Create and store a new Guardian role if it does not exist
        if ("guardian_role_id" not in data.keys()):
            guardianRole = None

            for role in guild.roles:
                if (role.name == "Guardian"):
                    guardianRole = role
                    exit

            if (guardianRole is None):
                guardianRole = await guild.create_role(
                    name = "Guardian",
                    color = self.get_discord_color(self.config["default_role_color"]),
                    mentionable = True,
                    reason = "Created by Little Light [DO NOT REMOVE]"
                )

            data["guardian_role_id"] = guardianRole.id

        self.write_json_file(self.GUILDS_PATH + "g{}.json".format(guild.id), data)

    def read_guild(self, guild: discord.Guild):
        """Read a guild to dict"""
        return self.read_json_file(self.GUILDS_PATH + "g{}.json".format(guild.id))