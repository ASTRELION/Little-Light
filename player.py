import discord
from discord.ext import commands
from little_light import LittleLightClient
from destiny import Destiny
import util
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

        print(json.dumps(data, indent = 4))

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

        characterArray = {
            str(membershipTypeInt): []
        }

        for k, v in characters.items():
            characterArray[str(membershipTypeInt)].append(int(k))
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

        membership = { 
            membershipTypeInt: membershipID
        }

        result = await util.wait_for_reaction_add(self.client, "\u2705", ctx.author)
        await ctx.send("Reacted.")

        print(characterArray)
        print(membership)
        self.client.write_user(ctx.author, memberships = membership, characters = characterArray)

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

        users = self.client.read_users()

        for key in users[str(user.id)]:
            response = await self.destiny.getProfile(key, users[str(user.id)][key], [100])
            responseString = json.dumps(response, indent = 4)
            print(responseString)
            #await ctx.send(responseString)

    @commands.command("profiles")
    async def profilesCommand(self, ctx, user: typing.Optional[discord.User] = None):
        """Lists all profiles associated with given user"""
        if (user is None):
            user = ctx.author

        users = self.client.read_users()
        profile = json.dumps(users[str(user.id)], indent = 4)
        await ctx.send(profile)

def setup(client):
    client.add_cog(Player(client))