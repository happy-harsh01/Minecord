import discord
from discord.ext import commands
import json
import os

make_profile = "You haven't created a profile yet.\nStart by creating a profile with ```start``` command."
Yes = ['YES', 'YeS', 'YEs', 'yEs', 'yES', 'yeS', 'yes']
blocks = ['Cobblestone', "Stone", "Gravel", "Dirt", 'Andesite', 'Granite', 'Diorite', 'Sand']
mobs = ['Cow', 'Sheep', 'Chicken', 'Pig', 'Zombie', 'Skeleton', 'Creeper', 'Spider', 'Golem']
# -----Tools -----
wooden_tools = ['Wooden Sword', 'Wooden Pickaxe', 'Wooden Axe', 'Woden Hoe']
stone_tools = ['Stone Sword', 'Stone Pickaxe', 'Stone Axe', 'Stone Hoe']
iron_tools = ['Iron Sword', 'Iron Pickaxe', 'Iron Axe', 'Iron Hoe']
gold_tools = ['Gold Sword', 'Gold Pickaxe', 'Gold Axe', 'Gold Hoe']
diamond_tools = ['Diamond Sword', 'Diamond Pickaxe', 'Diamond Axe', 'Diamond Hoe']
netherite_tools = ['Netherite Sword', 'Netherite Pickaxe', 'Netherite Axe', 'Netherite Hoe']

profile = ".\\main_resources\\profile.json"
channel = ".\\main_resources\\channels.json"


class Events:
    """Tells the bot what to do when an event occurs."""

    @staticmethod
    async def on_guild_leave(guild):
        """Handling when Bot leaves a server"""
        # Removing channels connections
        with open(channel, 'r') as f:
            chan = json.load(f)
        try:
            chan.pop(str(guild.id))
        except KeyError:
            print("Minecord left someones server, they didn't setup channels.")
        with open('channels.json', 'w') as f:
            json.dump(chan, f, indent=4)

    @staticmethod
    async def on_command_error(error, ctx):
        """Handling errors"""
        if isinstance(error, commands.CommandNotFound):
            print("Ignoring one Command not found error.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please give all the required arguments.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Please give me all permissions.\n```send message, embed links, attach files```")
        else:
            raise error
