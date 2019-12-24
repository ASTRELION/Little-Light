# Little Light
Discord bot with Destiny 2 integration.  
Written in Python using [Discord.py](https://github.com/Rapptz/discord.py) and [Pydest](https://github.com/jgayfer/pydest).

## Inviting the bot to your server

## Features
*As this bot is not completed yet, this feature list serves as a to-do list and may not be fully implemented*
- Destiny account linking
  - Link your Discord user with your Destiny account
  - Update your linked Destiny account when you create new characters or play on new platforms
- Character-specific statistics, milestones, and quests
- View your inventory, equipped items, and currency
- Search for any weapon or armor piece and list its stats
- Transfer items from your Vault to your characters
- All account information is live
- Supports all of Destiny's applicable platforms (Xbox, Playstation, Steam, ~~Blizzard~~, and Stadia)

## Installation
Preferably, use the offical bot and [invite it to your server](#inviting-the-bot-to-your-server).

Alternatively, you may clone this repository and run the bot yourself.  
*guide to be made*

## Configuration
*example_config.json holds default values without key values.*

> token

The bot's unique token. **DO NOT SHARE**

> destiny

Destiny's related configuration

>> api_key

The Destiny application API key. **DO NOT SHARE**

> prefix

Command prefix to be used.  
*Default: "d."*  
*Type: string*

> default_embed_color

Default embed color. This will be used most often.  
*Default: [ 255, 255, 255 ]*  
*Type: int array*

> success_embed_color

Embed color to display for success messages.  
*Default: [ 0, 255, 0 ]*  
*Type: int array*

> failure_embed_color

Embed color to display for failure messages.
*Default: [ 255, 0, 0 ]*  
*Type: int array*

> default_wait_time

Time to wait in seconds for responses from certain commands. Eg. reacting to a message or sending a response message.  
*Default: 60*  
*Type: int*

## Running
