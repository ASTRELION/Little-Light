import discord
from discord.ext import commands
from little_light import LittleLightClient
import util
import destiny
import typing
import json

def setup(client):
    client.add_cog(Clans(client))

class Clans(commands.Cog):
    """Clan related commands"""
    def __init__(self, client: LittleLightClient):
        self.client = client
        self.config = client.config
        self.destiny = client.destiny

    # clan {} #

    @commands.group("clan")
    async def clan(self, ctx):
        if (ctx.invoked_subcommand is None):
            await ctx.send("A sub-command is required for that.")

    @clan.command("list")
    async def clanListCommand(self, ctx):
        """Lists the members of your clan (max: 100)"""

    @clan.command("invite")
    async def clanInviteCommand(self, ctx, user: discord.User):
        """Invite a user to your clan"""

    @clan.command("message")
    async def clanMessageCommand(self, ctx, message: str):
        """Send a message to all members of your clan"""