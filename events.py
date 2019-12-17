import discord
from discord.ext import commands
import typing

class Events(commands.Cog):
    """Event listeners"""

    def __init__(self, client: commands.AutoShardedBot):
        """Init"""
        self.client = client
        self.config = client.config

    @commands.Cog.listener()
    async def on_connect(self):
        """On bot connect"""
        print("connected!")
        self.client.read_users()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Called when bot receives a message"""
        if (message.author == self.client.user or
                not message.content.startswith(self.config["prefix"])):
            return

        ctx = await self.client.get_context(message, cls = commands.Context)

        if (ctx.valid):
            await self.client.invoke(ctx)

def setup(client):
    client.add_cog(Events(client))