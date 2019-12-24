import discord
from discord.ext import commands

async def wait_for_reaction_add(client, reaction: str, user: discord.user):
    """Wait for reaction add"""
    def check(r: discord.Reaction, u: discord.User):
        return str(r.emoji) == reaction and u == user

    result = await client.wait_for("reaction_add", check = check)
    return result

async def wait_for_message(client, message: discord.Message):
    def check(m: discord.Message):
        return True

    result = await client.wait_for("message", check = check)
    return result