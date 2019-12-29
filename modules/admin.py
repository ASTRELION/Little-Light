import discord
from discord.ext import commands
from little_light import LittleLightClient
import util
import destiny
import typing
import json
import datetime

def setup(client):
    client.add_cog(Admin(client))

class Admin(commands.Cog):
    """Admin related commands (server admins and owner only)"""
    def __init__(self, client: LittleLightClient):
        self.client = client
        self.config = client.config
        self.destiny = client.destiny

    # Owner Only Commands #

    @commands.command("load")
    @commands.bot_has_permissions(send_messages = True)
    @commands.is_owner()
    async def loadCommand(self, ctx, extension: str):
        """Load in a new extension"""
        try:
            self.client.load_extension(extension)
            await ctx.send("{} extension loaded.".format(extension))
        except:
            await ctx.send("{} extension could not be loaded.".format(extension))

    @commands.command("unload")
    @commands.bot_has_permissions(send_messages = True)
    @commands.is_owner()
    async def unloadCommand(self, ctx, extension: str):
        """Unload an extension"""
        try:
            self.client.unload_extension(extension)
            await ctx.send("{} extension unloaded.".format(extension))
        except:
            await ctx.send("{} extension could not be unloaded.".format(extension))

    @commands.command("reload")
    @commands.bot_has_permissions(send_messages = True)
    @commands.is_owner()
    async def reloadCommand(self, ctx, extension: str):
        """Reload an extension"""
        try:
            self.client.reload_extension(extension)
            await ctx.send("{} extension reloaded.".format(extension))
        except:
            await ctx.send("{} extension could not be reloaded.".format(extension))

    # Server Administrator Commands #
    
    # TODO
    ## Send a DM to server administrators when the bot doesn't have
    ## premission to do something

    @commands.command("info")
    @commands.bot_has_permissions(send_messages = True)
    @commands.has_permissions(administrator = True)
    async def infoCommand(self, ctx):
        """Get information about the bot"""
        appInfo = await self.client.application_info()
        
        embed = discord.Embed()
        datetime.date.today()
        items = {
            "Name": appInfo.name,
            "Description": appInfo.description,
            "Owner": str(appInfo.owner),
            "Created": str(self.client.user.created_at.strftime("%Y.%m.%d at %H:%M")),
            "Age": str((datetime.date.today() - self.client.user.created_at.date()).days) + " days",
            "Contact": "{}bugreport <message>".format(self.config["command_prefix"])
        }

        embed.add_field(
            name = "Label",
            value = "\n".join("**{}**".format(x) for x in items.keys())
        )

        embed.add_field(
            name = "Value",
            value = "\n".join(items.values())
        )

        await ctx.send(self.destiny.getGhostDialog("app_info"), embed = embed)

    @commands.command("bugreport")
    @commands.bot_has_permissions(send_messages = True)
    @commands.has_permissions(administrator = True)
    async def bugreportCommand(self, ctx, *, report: str):
        """Send a bug report to the bot owner"""
        owner = (await self.client.application_info()).owner

        embed = discord.Embed(
            title = "Bug Report from {}".format(ctx.author),
            description = report
        )

        await owner.send("", embed = embed)

    @commands.command("broadcast")
    @commands.bot_has_permissions(send_messages = True)
    @commands.has_permissions(administrator = True)
    async def broadcastCommand(self, ctx, *, broadcast: str):
        """Broadcast a message in the default text channel to all linked Guardians"""

    @commands.command("log")
    @commands.bot_has_permissions(send_messages = True)
    @commands.has_permissions(administrator = True)
    async def logCommand(self, ctx):
        """List the log of commands that have been recently executed"""