import discord
from discord.ext import commands
#from little_light import LittleLightClient
import pydest
import random
import typing

class Destiny:
    """Pydest API wrapper and Destiny utility"""
    def __init__(self, client):
        self.client = client
        self.config = client.config

    # Bungie memebership types (platforms)
    membership_types = {
        -1: "all",
        1: "xbox",
        2: "psn",
        3: "steam",
        4: "blizzard",
        5: "stadia"
    }

    # Ghost dialog options
    ghost_dialog = {
        "query_success": [
            "I found these results in the Tower database.",
            "I queried the Tower databases and found this.",
            "This is what I found.",
        ],
        "query_fail": [
            "I couldn't find any relevant information.",
            "I couldn't find any relevant information in the Tower databases.",
            "My queries of the Tower databases didn't return anything useful.",
            "I didn't find anything."
        ],
        "get_item_success": [

        ],
        "get_item_fail": [

        ],
        "get_guardian_success": [

        ],
        "get_guardian_fail": [

        ],
        "get_character_success": [

        ],
        "get_character_fail": [

        ],
        "manifest_update": [
            "I updated my internal databases.",
            "My internal databases have been updated.",
            "Some new information appeared in the Tower database, I'll take note of it."
        ]
    }

    def getGhostDialog(self, dialog_type: str):
        """Get a random ghost dialog option from dialog type"""
        rand = random.randrange(len(Destiny.ghost_dialog[dialog_type]))
        return "*{}*".format(Destiny.ghost_dialog[dialog_type][rand])

    ### BEGIN API CALLS ###

    # Decided to implement "my own" API calls so I can easily return
    # just the data I need without having to perform session logic
    # everywhere

    def getDestinySession(self):
        """Start a session with the Destiny API"""
        destiny = pydest.Pydest(self.config["destiny"]["api_key"])
        return destiny

    # HASH
    async def decodeHash(self, hashID: int, definition: str):
        session = self.getDestinySession()
        response = await session.decode_hash(hashID, definition)
        await session.close()
        return response

    # MANIFEST
    async def updateDestinyManifest(self):
        """Updates the locally stored Destiny manifest"""
        session = self.getDestinySession()
        await session.update_manifest()
        await session.close()

    async def getDestinyManifest(self):
        """Get the Destiny manifest"""
        session = self.getDestinySession()
        response = await session.api.get_destiny_manifest()
        await session.close()
        return response

    # PLAYERS
    async def searchDestinyPlayer(self, name: str, platform: int = -1):
        """Seach for a destiny player"""
        session = self.getDestinySession()

        response = await session.api.search_destiny_player(
            platform,
            name
        )

        await session.close()
        return response["Response"]

    async def getProfile(self, membershipType: int, membershipID: int, components: list):
        session = self.getDestinySession()
        response = await session.api.get_profile(membershipType, membershipID, components)
        await session.close()
        return response["Response"]