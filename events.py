import discord
from discord.ext import commands

class Events(commands.Cog):
    """Event listeners"""

    def __init__(self, client):
        """Init"""
        self.client = client
        print("blah")

    @commands.Cog.listener()
    async def on_connect(self):
        """On bot connect"""
        print("conected!")

def setup(client):
    client.add_cog(Events(client))