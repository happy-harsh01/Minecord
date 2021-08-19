import discord
from discord.ext import commands
from functions.function import Func
from functions.game_functions import GameFunction
import json
import asyncio
import random
import time

func = Func()
is_over_channel = func.is_over_channel
profile = "D:\\Entertainment\\Harsh's Inventory\\Code With Harsh\\Minecord\\main_resources\\profile.json"

events = GameFunction()


class Over(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def enchant(self, ctx):
        if await is_over_channel(ctx):
            await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command()
    async def trade(self, ctx):
        if await is_over_channel(ctx):
            await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command()
    @commands.cooldown(1, 1800, type=commands.BucketType.user)
    async def fish(self, ctx):
        """Fishing command - complete"""
        if await is_over_channel(ctx):
            fishes = ["Raw Cod", "Raw Salmon", "Raw Salmon", "No fish"]
            fish = random.choice(fishes)
            quantity = random.randint(0, 6)
            if fish == "No fish":
                description = "You went on fishing but you got nothing lmao."
                embed = discord.Embed(title="Fishing", description=description, colour=discord.Colour.green())
                await ctx.send(emebed=embed)
                return
            if func.search_inv_item(ctx, "fishing rod"):
                if quantity == 0:
                    description = "You went on fishing but you got nothing lmao."

                else:
                    description = f"You went on fishing and you cached {quantity} fishes."
                embed = discord.Embed(title="Fishing", description=description, colour=discord.Colour.green())
                await func.add_inv(ctx, fish, quantity)
                await ctx.send(emebed=embed)

    @commands.command()
    async def build(self, ctx, monument=None):
        if await is_over_channel(ctx):
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
    @commands.cooldown(1, 3600, type=commands.BucketType.user)
    async def cave(self, ctx):
        if await is_over_channel(ctx):
            with open(profile, "r") as f:
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
    @commands.cooldown(1, 3600, type=commands.BucketType.user)
    async def chop(self, ctx):
        if await is_over_channel(ctx):
            if func.search_inv_item('Netherite Axe'):
                min_qty = 10
                max_qty = 20
            elif func.search_inv_item('Diamond Axe'):
                min_qty = 8
                max_qty = 16
            elif func.search_inv_item('Gold Axe'):
                min_qty = 6
                max_qty = 14
            elif func.search_inv_item('Iron Axe'):
                min_qty = 6
                max_qty = 12
            elif func.search_inv_item('Stone Axe'):
                min_qty = 3
                max_qty = 8
            elif func.search_inv_item('Wooden Axe'):
                min_qty = 1
                max_qty = 5
            else:
                min_qty = 1
                max_qty = 3
            qty_of_logs = random.randint(min_qty, max_qty)
            await func.add_inv(ctx, item, quantity)(ctx, "Log", qty_of_logs)
            description = f"{func.name(ctx)} went on chopping and brought back {qty_of_logs} logs"
            embed = discord.Embed(type="Copping Results", description=description, colour=discord.Colour.green())
            await ctx.send(emebed=embed)
            
    @commands.command()
    async def mine(self, ctx, block = None):
        if block is None:
            places = events.get_profiles()[str((ctx.author.id))]["builds"]
            if "shaft-mine" in places:
                pass
            else:
                pass
        else:
            pass
        

def setup(client):
    client.add_cog(Over(client))
