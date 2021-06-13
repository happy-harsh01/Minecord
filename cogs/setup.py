import discord
from discord.ext import commands
import json


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    async def set_setting_channel(self, ctx, server_channel: discord.channel):
        with open('channels.json', 'r') as f:
            channel = json.load(f)
            channel = channel[str(ctx.guild.id)]
            channel['settings'] = str(server_channel)

        with open('channels.json', 'w') as f:
            json.dump(channel, f)

    @commands.command()
    async def set_over_channel(self, ctx, server_channel: discord.channel):
        with open('channels.json', 'r') as f:
            channel = json.load(f)
            channel = channel[str(ctx.guild.id)]
            channel['over'] = str(server_channel)

        with open('channels.json', 'w') as f:
            json.dump(channel, f)

    @commands.command()
    async def set_nether_channel(self, ctx, server_channel: discord.channel):
        with open('channels.json', 'r') as f:
            channel = json.load(f)
            channel = channel[str(ctx.guild.id)]
            channel['nether'] = str(server_channel)

        with open('channels.json', 'w') as f:
            json.dump(channel, f)

    @commands.command()
    async def set_end_channel(self, ctx, server_channel: discord.channel):
        with open('channels.json', 'r') as f:
            channel = json.load(f)
            channel = channel[str(ctx.guild.id)]
            channel['end'] = str(server_channel)

        with open('channels.json', 'w') as f:
            json.dump(channel, f)


def setup(client):
    client.add_cog(Settings(client))

