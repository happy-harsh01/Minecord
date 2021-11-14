import discord
from discord.ext import commands
from .functions.function import Func
from .functions.game_functions import GameFunction
import json
import asyncio
import random
import time

func = Func()
is_over_channel = func.is_over_channel
game = GameFunction()
profile = "cogs/functions/main_resources/profiles.json"
info = "cogs/functions/main_resources/info.json"

events = GameFunction()


class Over(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def enchant(self, ctx):
        if not await is_over_channel(ctx):
          return
        await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command()
    async def trade(self, ctx):
        if not await is_over_channel(ctx):
          return
        await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command()
    @commands.cooldown(1, 60, type=commands.BucketType.user)
    async def hunt(self, ctx):
        if not await is_over_channel(ctx):
          return
        chance = random.randint(1,100)
        quantity = random.randint(1, 3)
        hunt = None
        mob = None
        if chance <= 20:
          #Raw porkchop
          hunt = "raw_porkchop"
          mob = "Pig" 
        elif chance <= 26:
          #raw beef
          if await game.inv_searcher(ctx, "wooden_sword","stone_sword,""iron_sword","golden_sword","diamond_sword","netherite_sword"):
            hunt = "raw_beef"
            mob = "Cow"
        elif chance <= 32:
          #raw chicken
          if await game.inv_searcher(ctx, "stone_sword,""iron_sword","golden_sword","diamond_sword","netherite_sword"):
            hunt = "raw_chicken"
            mob = "Chicken"
        elif chance <= 38:
          #raw mutton
          if await game.inv_searcher(ctx, "stone_sword,""iron_sword","golden_sword","diamond_sword","netherite_sword"):
            hunt = "raw_mutton"
            mob = "Sheep"
        elif chance <= 44:
          #leather
          if await game.inv_searcher(ctx, "stone_sword,""iron_sword","golden_sword","diamond_sword","netherite_sword"):
            hunt = "leather"
            mob = "Cow"
        elif chance <= 50:
          #feather
          if await game.inv_searcher(ctx, "stone_sword,""iron_sword","golden_sword","diamond_sword","netherite_sword"):
            hunt = "feather"
            mob = "Chicken"
        elif chance <= 56:
          #wool
          if await game.inv_searcher(ctx, "stone_sword,""iron_sword","golden_sword","diamond_sword","netherite_sword"):
            hunt = "wool"
            mob = "Sheep"
        elif chance <= 62:
          # rotten flesh
          if await game.inv_searcher(ctx, "iron_sword","golden_sword","diamond_sword","netherite_sword"):
            hunt = "rotten_flesh"
            mob = "Zombie"
        elif chance <= 68:
          #gunpowder
          if await game.inv_searcher(ctx, "iron_sword","golden_sword","diamond_sword","netherite_sword"):
            hunt = "gunpowder"
            mob = "Creeper"
        elif chance <= 74:
          #bow
          if await game.inv_searcher(ctx, "iron_sword","golden_sword","diamond_sword","netherite_sword"):
            hunt = "bow"
            mob = "Skeleton"
        elif chance <= 80:
          #arrow
          if await game.inv_searcher(ctx, "iron_sword","golden_sword","diamond_sword","netherite_sword"):
            hunt = "arrow"
            mob = "Skeleton"
        elif chance <= 86:
          #spider_eye
          if await game.inv_searcher(ctx, "iron_sword","golden_sword","diamond_sword","netherite_sword"):
            hunt = "spider_eye"
            mob = "Spider"
        elif chance <= 92:
          if await game.inv_searcher(ctx, "diamond_sword", "netherite_sword"):
            #ender_pearl
            hunt = "ender_pearl"
            mob = "Enderman"
        elif chance <= 98:
          #iron_ingots & poppy
          if await game.inv_searcher(ctx, "netherite_sword"):
            hunt = "iron_ingots"
            mob = "Iron Golem"           
        if hunt is None:
            await ctx.reply("Haha you got nothing")
            return
        tool =  await game.tool_sercher(ctx, "sword")
        await game.inv_manager(ctx, tool, -random.randint(1,2)*quantity)
        await game.inv_manager(ctx, hunt, quantity)
        hunt = hunt.replace("_"," ")
        await ctx.reply(f"You killed a {mob} and got {quantity} {hunt}")
            
    
    @commands.command()
    @commands.cooldown(1, 1800, type=commands.BucketType.user)
    async def fish(self, ctx):
        """Fishing command - complete"""
        if not await is_over_channel(ctx):         
          return
        if await game.inv_searcher(ctx, "fishing_pole"):
          await ctx.reply("You don't even own a ```fishing pole```")
          return
        chance = random.randint(1,100)
        quantity = random.randint(1, 3)
        fish = None 
        if chance <= 50:
          await ctx.reply("Haha you got nothing!")
          return
        elif chance <= 60:
          fish = "raw_code"  
        if chance <= 70:        
          fish = "raw_salmon" 
        elif chance <= 80:
          pass
        elif chance <= 90:
          pass
        else:
          pass
        if fish == None:
          return
        await game.inv_manager(ctx, fish, quantity)
        await ctx.reply(f"You caught {quantity} {fish}") 
      
    @commands.command()
    async def build(self, ctx, monument=None):
        if not await is_over_channel(ctx):
          return 
        if monument is None:
          em = discord.Embed(title="Build Command", description='''Items to build
    Level 1 House - Dirt House
    Level 2 House - Wooden House
    Level 3 House - Stone Mansion
    Level 4 House - Modern Apartment
    Level 5 House - Castle-e-Minecraft
    Farm Level 1 - Miniature Farm
    Farm Level 2 - Smol Farm
    Farm Level 3 - Normal Farm
    Farm Level 4 - Big Farm
    Farm Level 5 - Giant Farm
    Nether Portal
    Xp Farm
    Shaft Mine''')
          em.set_footer(icon_url = ctx.author.avatar_url,  text="Use command build <item> to build an item.")
          await ctx.send(embed=em)
          return
        else:
          pass
        

    @commands.command()
    @commands.cooldown(1, 5000, type=commands.BucketType.user)
    async def cave(self, ctx):
      if await is_over_channel(ctx):
        with open(info, "r")as f:
          data = json.load(f)["id"] # Loading data for emoji       
        with open(profile, "r") as f:
          user = json.load(f)
          places = user[str(ctx.author.id)]["places"]
        cave = ""
        blocks = []
        for place in places:
          if place == 'cave':
            cave = "cave"
            choices = ["cobblestone", "iron_pickaxe", "coal", "diorite", "andesite", "gravel", "sand", "dirt"]
            blocks = random.choices(choices) 
            break 
          elif place == 'underground_cave':
            cave = "underground_cave"
            choices = ["cobblestone", "iron_pickaxe", "coal", "diorite", "andesite", "gravel", "diamond", "gold_ore", "emerald", "restone_dust", "lapiz_lazuli"]
            blocks = random.choices(choices) 
            break
          elif place == 'ravine':
            cave = "ravine"
            choices = ["cobblestone", "iron_pickaxe", "coal", "diorite", "andesite", "gravel", "diamond", "gold_ore", "emerald", "restone_dust", "lapiz_lazuli"]
            blocks = random.choices(choices) 
            break
        if cave == "":
          await ctx.reply("You haven't discovered any cave.")
          return
        #Adding item in inventory
        descrip = "You brought back" 
        for block in blocks:
          quantity = random.randint(1,110) 
          await game.inv_manager(ctx, block, quantity)
          block_name = block.remove("_"," ").cpitalize()
          descrip += f"\n{data[block]} {block_name} X {quantity}"
        await func.send_embed(ctx, f"{ctx.author.name} went on a {cave}", descrip, "green",True)

    @commands.command()
    @commands.cooldown(1, 150, type=commands.BucketType.user)
    async def chop(self, ctx):
        if not await is_over_channel(ctx):
          return
        if await game.inv_searcher(ctx, "wooden_axe"):
          quantity = random.randint(1,5)
          await game.inv_manager(ctx, "wooden_axe", -random.randint(1,2)*quantity)
        elif await game.inv_searcher(ctx, "stone_axe"):
          quantity = random.randint(3,8)
          await game.inv_manager(ctx, "stone_axe", -random.randint(1,2)*quantity)
        elif await game.inv_searcher(ctx, "iron_axe"):
          quantity = random.randint(6,12)
          await game.inv_manager(ctx, "iron_axe", -random.randint(1,2)*quantity)
        if await game.inv_searcher(ctx, "gold_axe"):
          quantity = random.randint(6,14)
          await game.inv_manager(ctx, "gold_axe", -random.randint(1,2)*quantity)
        if await game.inv_searcher(ctx, "diamond_axe"):
          quantity = random.randint(8,16)
          await game.inv_manager(ctx, "diamond_axe", -random.randint(1,2)*quantity)
        if await game.inv_searcher(ctx, "netherite_axe"):
          quantity = random.randint(10,20)
          await game.inv_manager(ctx, "netherite_axe", -random.randint(1,2)*quantity)
        else:
          quantity = random.randint(1,3)
        await game.inv_manager(ctx, "log", quantity)
        with open(info, "r")as f:
          data = json.load(f)
          emoji =  data["id"]["log"]
        await ctx.reply(f"You brought {quantity} logs {emoji}" )  

def setup(client):
    client.add_cog(Over(client))
