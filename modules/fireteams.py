import discord
from discord.ext import commands
from little_light import LittleLightClient
import util
import destiny
import typing
import json

def setup(client):
    client.add_cog(Fireteams(client))

class Fireteams(commands.Cog):
    """Fireteam related commands"""
    def __init__(self, client: LittleLightClient):
        self.client = client
        self.config = client.config
        self.destiny = client.destiny

    # fireteam {} #

    @commands.group("fireteam")
    async def fireteam(self, ctx):
        if (ctx.invoked_subcommand is None):
            await ctx.send("A sub-command is required for that.")

    @fireteam.command("list")
    async def fireteamListCommand(self, ctx):
        """Lists the members of your fireteam (max: 6)"""
        await ctx.send(ctx.author)

    @fireteam.command("invite")
    async def fireteamInviteCommand(self, ctx, user: discord.User):
        """Invite a user to your fireteam"""

    @fireteam.command("kick")
    async def fireteamKickCommand(self, ctx, user: discord.User):
        """Kick a user from your fireteam"""

    @fireteam.command("promote")
    async def fireteamPromoteCommand(self, ctx, user: discord.User):
        """Promote a user to fireteam leader"""

    @fireteam.command("disband")
    async def fireteamDisbandCommand(self, ctx):
        """Disband your fireteam"""

    # fireteam create {} #

    @fireteam.group("create")
    async def fireteamCreate(self, ctx):
        if (ctx.invoked_subcommand is None):
            await ctx.send("A sub-command is required for that.")

    @fireteamCreate.command("voice")
    async def fireteamCreateVoiceCommand(self, ctx):
        """Create a temporary voice channel for your fireteam"""

    @fireteamCreate.command("text")
    async def fireteamCreateTextCommand(self, ctx):
        """Create a temporary text channel for your fireteam"""