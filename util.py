import discord
from discord.ext import commands
import asyncio

async def wait_for_reaction_add(client, reaction = None, user: discord.user = None):
    """Wait for reaction add"""
    def check(r: discord.Reaction, u: discord.User):
        isReaction = reaction is None or str(r.emoji) == reaction or str(r.emoji) in reaction
        isUser = user is None or u == user
        return isReaction and isUser
    
    try:
        result = await client.wait_for(
            "reaction_add", 
            check = check, 
            timeout = client.config["default_wait_time"]
        )
        return result
    except asyncio.TimeoutError:
        return None

async def wait_for_message(client, message: discord.Message):
    def check(m: discord.Message):
        return True

    result = await client.wait_for("message", check = check)
    return result