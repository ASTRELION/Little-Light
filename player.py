import discord
from discord.ext import commands
from little_light import LittleLightClient
from destiny import Destiny
import pydest
import typing
import json

class Player(commands.Cog):
    """Destiny related commands"""

    def __init__(self, client: LittleLightClient):
        self.client = client
        self.config = client.config
        self.destiny = client.destiny

    @commands.command("link")
    async def linkCommand(self, ctx, membershipID: int):
        """Link a membership ID with a discord user"""
        membership = { 
            3: membershipID
        }
        self.client.write_user(ctx.author, membership)

    @commands.command("search")
    async def searchCommand(self, ctx, *, player_name: str):
        """Search for a player with given name"""
        response =  await self.destiny.searchDestinyPlayer(player_name, "all")

        if (not response):
            await ctx.send(self.destiny.getGhostDialog("query_fail"))
            return

        embed = discord.Embed(
            title = ""
        )

        usernames = "\u200B"
        platforms = "\u200B"
        ids = "\u200B"
        
        for row in response:
            usernames += "{}\n".format(row["displayName"])
            platforms += "{}\n".format(self.destiny.membership_types[row["membershipType"]])
            ids += "{}\n".format(row["membershipId"])

        embed.add_field(
            name = "Display Name",
            value = usernames,
            inline = True
        )

        embed.add_field(
            name = "Platform",
            value = platforms,
            inline = True
        )

        embed.add_field(
            name = "ID",
            value = ids,
            inline = True
        )

        await ctx.send(self.destiny.getGhostDialog("query_success"), embed = embed)

    @commands.command("profile")
    async def profileCommand(self, ctx, user: discord.User):
        cursor = self.client.query(
            "SELECT * FROM membership WHERE user_id = %s", user.id
        )

        for membershipID, userID in cursor:
            response = await self.destiny.getProfile(3, membershipID, [100])
            await ctx.send(json.dumps(response, indent = 4))

def setup(client):
    client.add_cog(Player(client))