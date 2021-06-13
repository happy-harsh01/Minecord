import discord
from discord.ext import commands
from functions.events import Events
import json, asyncio, random, time


event = Events(commands.Bot)
profile_check = event.has_profile
normal_channel_check = event.is_not_restricted_channel
location_channel_check = event.location_channel_check
user_info = event.modify

class Over(commands.Cog):
    def __init__(self, client):
        self.client = client

    # @commands.command()
    # async def chest(self, ctx, type):
    #     if normal_channel_check(ctx):
    #         if profile_check(ctx):
    #             await ctx.send("This command is yet to be made!\nSorry :(")

    # @commands.command()
    # async def take(self, ctx, item):
    #     if normal_channel_check(ctx):
    #         if profile_check(ctx):
    #             await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command()
    async def enchant(self, ctx):
        await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command()
    async def trade(self, ctx):
        await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command()
    async def fish(self, ctx):
        inv = event.inv_tool(ctx, "misc")
        fishes = ["Raw Cod", "Raw Salmon", "Raw Salmon"]
        choice = random.choice(fishes)
        no = random.randint(1,6)
        try:
            await event.inv(ctx, choice, no)
            with open(".\main_resources\profile.json","w") as f:
                a = inv["fishing rod"]
                inv["fishing rod"] = a - 2
                json.dump(inv, f, indent=4)
            await ctx.send(f"You caught out {no} {choice}")
        except KeyError:
            await ctx.send("You cannot fish with your bare hands. Get yourself a fishing rod.")

    @commands.command()
    async def build(self, ctx, monument=None):
        if monument is None:
            em = discord.Embed(title="Build Command", description='''Items to build
Level 1 House - Dirt House
Level 2 House - Wooden House
Level 3 House - Stone Mansion
Level 4 House - Modern Apartment
Level 5 House - Royal Castle
Farm Level 1 - Miniature Farm
Farm Level 2 - Small Farm
Farm Level 3 - Normal Farm
Farm Level 4 - Big Farm
Farm Level 5 - Giant Farm
Nether Portal''')
            em.set_footer(text="Use command ```build <item>``` to build an item.")
            await ctx.send(embed=em)


    @commands.command()
    @commands.cooldown(1,3600,type=commands.BucketType.user)
    async def cave(self, ctx):
        with open("D:\Entertainment\Harsh's Inventory\Code With Harsh\Minecord\main_resources\profile.json", r)as f:
            places = json.load(f)
            places = places[str(ctx.author.id)]["place"]
            for place in places:
                if place == 'cave':
                    pass
                elif place == 'underground cave':
                    pass
                elif place == 'ravine':
                    pass

    @commands.command()
    async def chop(self, ctx):
        breaking_time = event.wood_breaking_time(ctx)
        await ctx.send(f"{ctx.author.name}You went on to chop some trees...")
        initial = time.time
        while True:
            # Searching Tree
            await asyncio.sleep(2)
            for i in range(random.choice([5,5,5,8])):
                await event.inv(ctx,"Log",1)
                await asyncio.sleep(breaking_time)

def setup(client):
    client.add_cog(Over(client))
