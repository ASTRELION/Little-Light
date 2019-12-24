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

    # Component types that may be requested
    component_types = {
        100: "profile",
        101: "vendorReceipts",
        102: "profileInventories",
        103: "profileCurrencies",
        104: "profileProgression",
        105: "platformSilver",
        200: "characters",
        201: "characterInventories",
        202: "characterProgressions",
        203: "characterRenderData",
        204: "characterActivities",
        205: "characterEquipment",
        300: "itemInstances",
        301: "itemObjectives",
        302: "itemPerks",
        303: "itemRenderData",
        304: "itemStats",
        305: "itemSockets",
        306: "itemTalenGrids",
        307: "itemCommonData",
        308: "itemPlugStates",
        309: "itemPlugObjectives",
        310: "itemReusablePlugs",
        400: "vendor",
        401: "vendorCategories",
        402: "vendorSales",
        500: "kiosks",
        600: "currencyLookups",
        700: "presentationNodes",
        800: "collectibles",
        900: "records",
        1000: "transitory"
    }

    class_types = {
        0: "Titan",
        1: "Hunter",
        2: "Warlock"
    }

    race_types = {
        0: "Human",
        1: "Awoken",
        2: "Exo"
    }

    def getGhostDialog(self, dialog_type: str):
        """Get a random ghost dialog option from dialog type"""
        rand = random.randrange(len(self.client.ghost_dialog[dialog_type]))
        return "*{}*".format(self.client.ghost_dialog[dialog_type][rand])

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

    # CHARACTERS
    async def getCharacter(self, membershipType: int, membershipID: int, characterID: int, components: list):
        session = self.getDestinySession()
        response = await session.api.get_character(membershipType, membershipID, characterID, components)
        await session.close()
        return response["Response"]