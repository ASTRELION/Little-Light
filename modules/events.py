import discord
from discord.ext import commands
from little_light import LittleLightClient

def setup(client):
    client.add_cog(Events(client))

class Events(commands.Cog):
    """Basic event listeners for Little Light Client"""

    def __init__(self, client: LittleLightClient):
        """Init"""
        self.client = client
        self.config = client.config

    @commands.Cog.listener()
    async def on_connect(self):
        """On bot connect"""
        print("Connected.")
        statuses = {
            "online": discord.Status.online,
            "offline": discord.Status.offline,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "do_not_disturb": discord.Status.dnd,
            "invisible": discord.Status.invisible
        }

        activityTypes = {
            "playing": discord.ActivityType.playing,
            "listening": discord.ActivityType.listening,
            "streaming": discord.ActivityType.streaming,
            "watching": discord.ActivityType.watching
        }

        activity = discord.Activity(
            name = self.config["activity"],
            type = activityTypes[self.config["activity_type"]]
        )

        await self.client.change_presence(
            activity = activity,
            status = statuses[self.config["status"]]
        )

    @commands.Cog.listener()
    async def on_ready(self):
        """On bot ready"""
        print("Ready.")
        print("Loading {} guilds...".format(len(self.client.guilds)))

        for guild in self.client.guilds:
            await self.client.write_guild(guild, {})
            print("Loaded {} guild".format(guild.name))

        print("Guilds loaded.")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """Called when bot receives a message"""
        if (message.author == self.client.user or
                not message.content.startswith(self.config["prefix"])):
            return

        ctx = await self.client.get_context(message, cls = commands.Context)

        if (ctx.valid):
            await self.client.invoke(ctx)