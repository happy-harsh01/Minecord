import discord
from discord.ext import commands
from functions.events import Events
import asyncio
import random
import json

event = Events(commands.Bot)
# profile_check = event.profile_check
# normal_channel_check = event.normal_channel_check
# location_channel_check = event.location_channel_check
# user_info = event.modify

# Adventurable locations :- Cave:{Cave, Underground Cave, Ravine}, Village, Ocean, 
# normal_channel_check = event.normal_channel_check
profiles = ".\main_resources\profile.json"
channels = ".\main_resources\channels.json"

mine_no = {"Netherite Pickaxe":"20-30","Diamond Pickaxe":"20-25",
"Gold Pickaxe":"15-25",'Iron Pickaxe':"10-15", 'Stone Pickaxe': '1-10',"Wooden Pickaxe":"1-5"}

class Action(commands.Cog):
    # def __init__(self, bot: commands.Bot):
    #     self.bot = bot

    @commands.command()
    async def hi(self, ctx):
        await ctx.send("Hello I am Minecord, Minecraft Discord Bot ,My prefix is ```m!```, start playing!")

    @commands.command()
    async def eat(self, ctx):
        await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command()
    async def health(self, ctx):
        await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command()
    async def go(self, ctx, location):
        await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command()
    async def profile(self, ctx, user: None):
        if user is None:
            user = ctx.author
        await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command()
    async def inv(self, ctx):
        await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command()
    async def craft(self, ctx, item):
        await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command(aliases=['adv'])
    async def adventure(self, ctx):
        location = event.user_info(ctx.author.id, "loaction", "Adventure")
        em = discord.Embed(title=f"{ctx.name}'s Adventure", description="You went on an adventure.\nLet's check what do you find out!")
        await ctx.send(embed=em)
        await asyncio.sleep(random.choices(10, 20, 30, 40, 50, 60))
        num = random.randint(1,11)
        if num == 1:
            location = event.modify(ctx.author.id, "loaction", "Lost")
            await ctx.send(f"{ctx.author.mention} You are lost finding new locations.")
        else:
            num1 = random.randint(50)
            location = event.modify(ctx.author.id, "loaction", "Home")

    @commands.command()
    @commands.cooldown(1, 3600,type=commands.BucketType.user)
    async def mine(self, ctx, blocks:None):
        def pick(pickaxe):
            pickaxe = pickaxe.lower()
            if pickaxe == "netherite pickaxe":
                return "10-30"
            if pickaxe == "diamond pickaxe":
                return "10-20"
            if pickaxe == "iron pickaxe":
                return "10-15"
            if pickaxe == "stone pickaxe":
                return "1-10"
            if pickaxe == "wooden pickaxe":
                return "1-5"

        if blocks is None:
            if "shaft mine" in event.info(ctx, 'builds'):
                # Shaft mine banaya hai
                blocks = ["Cobblestone","Redstone", "Lapiz Lazuli", "Diorite", "Andesite","Iron ore", "Coal ore", "Gold ore", "Dirt", "Gravel", "Sand"]
                if event.inv_tool(ctx, "pickaxe") == "diamond pickaxe" or event.inv_tool(ctx, "pickaxe") == "netherite pickaxe":
                    # Diamond pickaxe or Netherite pickaxe hai
                    blocks = ["Cobblestone", "Redstone", "Lapiz Lazuli", "Diorite", "Andesite", "Iron ore","Coal ore", "Gold ore", "Dirt", "Gravel", "Sand"]
                    block = random.randint(1, 100)
                    if block >= 50:
                        # Fail
                        pass
                    elif block >= 70:
                        # Cobblestone
                        pass
                    elif block >= 85:
                        # Dirt
                        pass
                    elif block >= 95:
                        # Sand
                        pass
                    elif block >= 100:
                        # Iron ore
                        pass
                else:
                    # Wo sab nahi hai
                    pass
            else:
                # Shaft mine nai banaya hai
                block = random.randint(1,100)
                if block >= 50:
                    # Fail
                    pass
                elif block >= 70:
                    # Cobblestone
                    pass
                elif block >= 85:
                    # Dirt
                    pass
                elif block >= 95:
                    # Sand
                    pass
                elif block >= 100:
                    # Iron ore
                    pass
        else:
            pass

    @commands.command()
    async def hunt(self, ctx):
        await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command()
    async def location(self, ctx):
        with open("D:\Entertainment\Harsh's Inventory\Code With Harsh\Minecord\main_resources\profile.json", 'r') as f:
            loc = json.load(f)
        loc = loc[str(ctx.author.id)]["location"]
        loc_sub = loc[str(ctx.author.id)]["sub_location"]
        em = discord.Embed(name=f"{ctx.author.name}'s Location", description=f"Dimension : {loc}\nLocation : {loc_sub}")
        await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(Action(bot))

