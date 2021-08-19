import discord
from discord.ext import commands
from functions.events import Events
import json
import random
import asyncio


event = Events(commands.Bot)
profile_check = event.has_profile
normal_channel_check = event.is_not_restricted_channel
location_channel_check = event.location_channel_check


class GameSettings(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def start(self, ctx):
        with open('profile.json', 'r') as f:
            prefix = json.load(f)
            if str(ctx.author.id) in prefix:
                await ctx.send('Profile already exist\nYou can start playing now')
            else:
                await ctx.send()
                prefix[str(ctx.author.id)] = {'name': 'Alex', "location": 'Over World', "sub_location": 'Home',
                                            'inv': {
                                                "tools":'n/a',
                                            },
                                            'builds':[],
                                            'home': 'n/a','farm': 'n/a',"health": 20, "place": []}
                with open('profile.json', 'w') as op:
                    json.dump(prefix, op, indent=4)
                await ctx.send("Profile has been created.\nYou can start playing now")

    @commands.command(aliases=["delete profile"])
    async def delete(self, ctx):
        await ctx.send('''Are you sure want to delete your profile ?
This step is highly irreversible.
Are you sure ?
Type ```Y``` or ```Yes``` to confirm or ```N``` or ```No``` to go back.''')

        def check(m):
            return m.author.id == ctx.author.id and m.channel == ctx.channel

        msg = await self.client.wait_for(event='message', timeout=30, check=check)
        try:
            if msg.content.lower == 'yes':
                with open('profile.json', 'w') as f:
                    person = json.load(f)
                    person.pop(str(ctx.author.idl))
                    json.dump(person, f, indent=4)
                await ctx.send('Profile deleted Successfully')
            else:
                await ctx.send('You stepped back from profile deletion!')
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} did not replied in time. What the hell he is doing!")

    @commands.command()
    async def change_name(self, ctx, name_new):
        with open('.\main_resources\profile.json', 'w')as f:
            names = json.load(f)
            names[str(ctx.author.id)]["name"] = name_new
            json.dump(names,f,indent=4)

def setup(client):
    client.add_cog(GameSettings(client))
