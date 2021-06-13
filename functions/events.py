import discord
from discord.ext import commands
import json
import os

profile = ".\main_resources\profile.json"
channel = ".\main_resources\channels.json"

class Events:
    """Tells the bot what to do when an event occurs."""
    def __init__(self, bot):
        self.bot = bot


    async def on_guild_leave(self, guild):
        """Handelling when Bot leaves a server"""
        # Removing Prefix
        with open(channel, 'r') as f:
            chan = json.load(f)
        try:
            chan.pop(str(guild.id))
        except KeyError:
            print("Minecord left someones server, they didn't setup channels.")
        with open('channels.json', 'w') as f:
            json.dump(chan, f, indent=4)


    async def on_command_error(self, error, ctx):
        """Handelling errors"""
        if isinstance(error, commands.CommandNotFound):
            print("Ignoring one Command not found error.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please give all the required arguments.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("please give me all permissions.\n```send message, embed links, attach files```")
        else:
            raise error


def setup(client):
    client.add_cog(Events(client))
