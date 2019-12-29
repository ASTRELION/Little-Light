import discord
from discord.ext import commands
from little_light import LittleLightClient
from destiny import Destiny
import util
import pydest
import typing
import json

def setup(client):
    client.add_cog(Player(client))

class Player(commands.Cog):
    """Played-specific commands for general purpose use"""

    def __init__(self, client: LittleLightClient):
        self.client = client
        self.config = client.config
        self.destiny = client.destiny

    @commands.command("update")
    async def updateCommand(self, ctx):
        """Update your associated Destiny account to include new characters"""

    @commands.command("unlink")
    async def unlinkCommand(self, ctx):
        """Unlink your Discord profile from any existing Destiny accounts"""

    @commands.command("link")
    @commands.bot_has_permissions(manage_roles = True, send_messages = True)
    async def linkCommand(self, ctx, membershipType: str, membershipID: int):
        """Link a membership ID with a discord user"""
        msg = await ctx.send(self.destiny.getGhostDialog("loading"))

        membershipTypeInt = next(
            k for k, v in self.destiny.membership_types.items() if v == membershipType
        )
        components = [100, 200]
        response = await self.destiny.getProfile(membershipTypeInt, membershipID, components)
       
        embed = discord.Embed(
            title = "Are you sure you want to link to this account?",
            description = "This will reset any existing links and link your discord user to this account."
        )

        data = response[self.destiny.component_types[100]]["data"]
        userInfo = data["userInfo"]

        embed.add_field(
            name = "Display Name",
            value = userInfo["displayName"]
        )
        
        embed.add_field(
            name = "Platform",
            value = self.destiny.membership_types[membershipTypeInt]
        )

        embed.add_field(
            name = "\u200B",
            value = "Characters",
            inline = False
        )

        characters = response[self.destiny.component_types[200]]["data"]
        classes = "\u200B"
        races = "\u200B"
        timePlayeds = "\u200B"

        memberData = {
            "memberships": [],
            "characters": []
        }

        for k, v in characters.items():
            memberData["characters"].append(int(k))
            classes += "{}\n".format(self.destiny.class_types[v["classType"]])
            races += "{}\n".format(self.destiny.race_types[v["raceType"]])
            timePlayeds += "{:.2f} hours\n".format(int(v["minutesPlayedTotal"]) / 60)

        embed.add_field(
            name = "Class",
            value = classes
        )

        embed.add_field(
            name = "Race",
            value = races
        )

        embed.add_field(
            name = "Time Played",
            value = timePlayeds
        )

        embed.add_field(
            name = "\u200B",
            value = "Seasons Played",
            inline = False
        )

        for seasonHash in data["seasonHashes"]:
            season = await self.destiny.decodeHash(seasonHash, "DestinySeasonDefinition")
            embed.add_field(
                name = "Season {}".format(season["seasonNumber"]),
                value = season["displayProperties"]["name"]
            )
        
        await msg.edit(content = "", embed = embed)
        await msg.add_reaction("\u2705")
        await msg.add_reaction("\u274C")

        memberData["memberships"] = { 
            membershipTypeInt: membershipID
        }

        result = await util.wait_for_reaction_add(self.client, reaction = ["\u2705", "\u274C"], user = ctx.author)
        
        if (result and str(result[0]) == "\u2705"):
            roleID = self.client.read_guild(ctx.guild)["guardian_role_id"]
            await ctx.author.add_roles(
                ctx.guild.get_role(roleID),
                reason = "Added by Little Light"
            )
            self.client.write_user(ctx.author, memberData)
            await ctx.send("Your account has been linked.")
        else:
            await ctx.send("Account linking failed.")

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
    async def profileCommand(self, ctx, user: typing.Optional[discord.User] = None):
        """Display given user's profile information"""
        if (user is None):
            user = ctx.author

        for key in self.client.read_user(user)["memberships"]:
            response = await self.destiny.getProfile(key, self.client.read_user(user)["memberships"][key], [100])
            responseString = json.dumps(response, indent = 4)
            print(responseString)
            #await ctx.send(responseString)

    @commands.command("characters")
    async def charactersCommand(self, ctx, user: typing.Optional[discord.User] = None):
        """Display a summary of all of your characters"""
        if (user is None):
            user = ctx.author

    @commands.command("inspect")
    async def inspectCommand(self, ctx, user: discord.User):
        """Inspect a player. View their profile and equipped items"""