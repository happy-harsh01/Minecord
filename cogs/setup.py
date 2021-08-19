import discord
from discord.ext import commands
import json
from functions.game_functions import GameFunction
import asyncio

game = GameFunction()
profile = "D:\\Entertainment\\Harsh's Inventory\\Code With Harsh\\Minecord\\main_resources\\profile.json"
channel = "D:\\Entertainment\\Harsh's Inventory\\Code With Harsh\\Minecord\\main_resources\\channels.json"
restricted = "D:\\Entertainment\\Harsh's Inventory\\Code With Harsh\\Minecord\\main_resources\\restricted_channels.json"


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def start(self, ctx):

        def check(m):
            return m.author.id == ctx.author.id and m.channel == ctx.channel

        try:
            await ctx.send("Enter a name for your Character : ")
            msg = await self.client.wait_for('message', timeout=30, check=check)
            await game.create_profile(ctx, msg)
            await ctx.send("Profile has been created.\nYou can start playing now")
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} did not replied in time. What the hell he is doing!")

    @commands.command(aliases=["delete profile"])
    async def delete(self, ctx):
        await ctx.send('''Are you sure want to delete your profile ?
    This step is highly irreversible.
    Are you sure ?
    Type ```Y``` or ```Yes``` to confirm or ```N``` or ```No``` to go back.''')

        def check(m):
            return m.author.id == ctx.author.id and m.channel == ctx.channel

        try:
            msg = await self.client.wait_for(event='message', timeout=30, check=check)
            if msg.content.lower() == 'yes' or msg.content.lower() == "y":
                with open(profile, 'r') as f:
                    person = json.load(f)
                    person.pop(str(ctx.author.id))
                with open(profile, 'r') as f:
                    json.dump(person, f, indent=4)
                await ctx.send('Profile deleted Successfully')
            else:
                await ctx.send('You stepped back from profile deletion!')
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} did not replied in time. What the hell he is doing!")

    @commands.command()
    async def change_name(self, ctx, name_new):
        with open(profile, 'w')as f:
            names = json.load(f)
            names[str(ctx.author.id)]["name"] = name_new
            json.dump(names, f, indent=4)

    @commands.command()
    async def set_restricted_channel(self, ctx, restricted_channel: discord.channel):
        """Adds the given channel in restricted channel list."""
        with open(restricted, 'r') as f:
            channels = json.load(f)
            if ctx.guild.id in channels:
                channels[str(ctx.guild.id)].append(restricted_channel)
            else:
                channels.update({str(ctx.guild.id): restricted_channel})

        with open(channel, 'w') as f:
            json.dump(channel, f, indent=4)

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
