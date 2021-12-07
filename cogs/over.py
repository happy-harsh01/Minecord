import discord
from discord.ext import commands
from .functions.function import Func
from .functions.game_functions import GameFunction
import json
import asyncio
import random
import time
from dislash import ActionRow, Button, ButtonStyle, SelectMenu, SelectOption


func = Func()
is_over_channel = func.is_over_channel
game = GameFunction()
profile = "main_resources/profiles.json"
info = "main_resources/info.json"

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
        if await game.inv_searcher(ctx, "fishing_rod"):
          await ctx.reply("You don't even own a ```fishing rod```")
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
      build = Button(
        label = "Build",
        style = ButtonStyle.green,
        custom_id = "build"  )
      build_disabled = Button(
        label = "Build",
        style = ButtonStyle.red,
        custom_id = "build_disabled",
        disabled = True)
      def check(m):
            return m.author.id == ctx.author.id
      with open(info,"r")as f:
            data = json.load(f)
      if monument is None:
        target = "last" 
        #Creating Button          
        back = Button(
            label = "Back",
            style = ButtonStyle.grey,
            custom_id = "back")
        forward = Button(
            label = "»",
            style = ButtonStyle.blurple,
            custom_id = "forward")
        backward = Button(
            label = "«",
            style = ButtonStyle.blurple,
            custom_id = "backward")
        forward_disabled = Button(
            label = "»",
            style = ButtonStyle.blurple,
            custom_id = "forward_disabled",
            disabled = True)
        backward_disabled = Button(
            label= "«",
            style = ButtonStyle.blurple,
            custom_id = "backward_disabled",
            disabled = True)      
        em = discord.Embed(title="Build Command", description='''Items to build''', colour= discord.Colour.green())
        em.add_field(name= "Houses",value= "**Level 1 House - Dirt House**\n  id - ```dirt```\n**Level 2 House - Wooden House**\n  id - ```wooden```\n**Level 3 House - Stone Mansion**\n  id - ```stone```\n**Level 4 House - Modern Apartment**\n  id - ```modern```\n**Level 5 House - Castle-e-Minecraft**\n  id - ```castle```")
        em.set_footer(icon_url = ctx.author.avatar_url,  text="Use command build <item id> to build an item.")         
        msg = await ctx.send(embed=em, components = [ActionRow( backward_disabled, build, forward)])
        no_button_check = False
        button = "" 
        while True:
          try:
            if not no_button_check:
                waiter = await msg.wait_for_button_click(check=check, timeout = 60.0)
                button = waiter.clicked_button.label
            no_button_check = False 
          except asyncio.TimeoutError :
              print("Exit")
              await msg.edit(embed=em, components = [ActionRow( backward_disabled,build_disabled, forward_disabled)])
              return
          
          if button == "«":
            if target == "first":  
              target = "middle"
              em.set_field_at(0, name= "Farm", value = "**Farm Level 1 - Miniature Farm**\n  id - ```mini```\n**Farm Level 2 - Smol Farm**\n  id - ```smol```\n**Farm Level 3 - Normal Farm**\n  id - ```normal```\n**Farm Level 4 - Big Farm**\n  id - ```big```\n**Farm Level 5 - Giant Farm**\n  id - ```giant```" )
              await msg.edit(embed=em, components = [ActionRow( backward,build, forward)])
            else: 
                target = "last"
                em.set_field_at(0, name= "Houses",value= "**Level 1 House - Dirt House**\n  id - ```dirt```\n**Level 2 House - Wooden House**\n  id - ```wooden```\n**Level 3 House - Stone Mansion**\n  id - ```stone```\n**Level 4 House - Modern Apartment**\n  id - ```modern```\n**Level 5 House - Castle-e-Minecraft**\n  id - ```castle```")
                await msg.edit(embed=em, components = [ActionRow(backward_disabled, build, forward)])
          elif button == "Build":
            em.description = "What do you want to Build ?\nClick on the button to build an item."
            em.remove_field(index=0 )
            async def get_buttons(label, ids):
              buttons = []
              j = 0 
              for i in label:               
                builds = data["build"][ids[j]]
                if target != "middle":
                  for key in builds:
                    colour = await game.inv_searcher(ctx, key, value=builds[key])
                    if colour is False:
                      break
                else:
                  colour = await game.build_searcher(ctx, builds[0]) and await game.inv_searcher(ctx,builds[1], data["tools"][builds[1]] ) 
                if colour:
                  colour = ButtonStyle.green
                else:
                  colour = ButtonStyle.red   
                button = Button(
                  label = i,
                  style = colour,
                  custom_id = ids[j])
                j += 1
                buttons.append(button)
              return buttons
            buttons = []
            if target ==  "last":            
              labels = ["House Level 1 - Dirt House","House Level 2 - Wooden House","House Level 3 - Stone Mansion","House Level 4 - Modern Apartment","House Level 5 - Castle-e-Minecraft"]
              ids = ["dirt_house", "wooden_house","stone_mansion","modern_apartment","castle-e-minecraft"]
              buttons = await get_buttons(labels, ids)
              await msg.edit(embed =em, components = [ActionRow(buttons[0], buttons[1],buttons[2], buttons[3], buttons[4]), ActionRow(back)])
            elif target ==  "first":
              buttons = await get_buttons(["Xp Farm", "Shaft Mine", "Nether Portal"], ["xp_farm", "shaft_mine", "nether_portal"])
              await msg.edit(embed =em, components = [ActionRow(buttons[0], buttons[1],buttons[2], back)])
            else:
              label = ["Farm Level 1 - Miniature Farm", "Farm Level 2 - Smol Farm", "Farm Level 3 - Normal Farm", "Farm Level 4 - Big Farm", "Farm Level 5 - Giant Farm"] 
              ids = ["miniature_farm", "smol_farm", "normal_farm", "big_farm", "giant_farm"] 
              buttons = await get_buttons(label, ids)
              await msg.edit(embed =em, components = [ActionRow(buttons[0], buttons[1],buttons[2], buttons[3], buttons[4],), ActionRow(back)])
            try:
              waiter = await msg.wait_for_button_click(check=check, timeout = 60.0)
              buttons = waiter.clicked_button.custom_id
              if button != "back":
                build_cmd = self.client.get_command("build")
                await ctx.invoke(build_cmd, buttons)
              else:
                button = "«"
                no_button_check = True 
                em.add_field(name="Hi", value ="Bye" )
                continue
            except asyncio.TimeoutError :
              print("Exit")
              await msg.edit(embed=em, components = [ActionRow( backward_disabled,build_disabled, forward_disabled)])
              return
          else:
              if target == "last":
                target = "middle"
                em.set_field_at(0, name= "Farm", value = "**Farm Level 1 - Miniature Farm**\n  id - ```mini```\n**Farm Level 2 - Smol Farm**\n  id - ```smol```\n**Farm Level 3 - Normal Farm**\n  id - ```normal```\n**Farm Level 4 - Big Farm**\n  id - ```big```\n**Farm Level 5 - Giant Farm**\n  id - ```giant```" )            
                await msg.edit(embed=em, components = [ActionRow(backward,build, forward)])
              else:
                target = "first"
                em.set_field_at(0, name= "Other", value= "**Nether Portal**\n  id - ```nether```\n**Xp Farm**\n  id -  ```xp```\n**Shaft Mine**\n  id - ```shaft```")
                await msg.edit(embed=em, components = [ActionRow(backward,build, forward_disabled)])
      else:        
          monument = await game.get_id(monument)
          if monument is None:
            await ctx.send("The item you are looking for does not even exists lol")
            return
          builds = data["build"][monument]
          farms = ["miniature_farm", "smol_farm", "normal_farm", "big_farm", "giant_farm"]
          can_build = True
          em = discord.Embed(title = monument.replace("_", " ").capitalize(), description="", colour = discord.Colour.green())
          description = "" 
          if monument in farms:
              farm_name =  builds[0].replace("_"," ").capitalize()            
              if await game.build_searcher(ctx, builds[0]):
                description += f":white_check_mark: {farm_name}\n"
              else:
                can_build = False 
                description += f":x: {farm_name}\n"
              durability = data["tools"][builds[1]]
              name = builds[1].replace("_", " ").capitalize() 
              if game.inv_searcher(ctx, builds[1], durability):
                description += f"\n:white_check_mark: {name} :  {durability}\n"
              else:
                  can_build = False 
                  description += f"\n:x: {name} : {durability}\n"
          else:
            for building in builds:          
              name = building.replace("_"," ").capitalize()
              if await game.inv_searcher(ctx, building, builds[building]):
                description += f":white_check_mark: {name} : {builds[building]}\n"
              else:
                can_build = False 
                description += f":x: {name} : {builds[building]}\n"
          em.description = description 
          if can_build:
            msg = await ctx.send( embed=em, components = [ActionRow(Button(label= "End Interaction", style= ButtonStyle.grey,custom_id="end" ), build)])
          else:
            em.colour = discord.Colour.red() 
            msg = await ctx.send( embed=em, components = [ActionRow(Button(label= "End Interaction", style= ButtonStyle.grey,custom_id="end"), build_disabled)]  )
          while True:
            try:
              waiter = await msg.wait_for_button_click(check=check, timeout = 60.0 )
              if waiter.clicked_button.label == "Build":
                pass
              else:
                raise asyncio.TimeoutError
            except asyncio.TimeoutError:
              em.title = "Interaction Ended"
              em.description= "***: )***\nThanks for using Minecord" 
              await msg.edit(embed =em, components=[ActionRow(Button(label= "End Interaction", style= ButtonStyle.grey,custom_id="end", disabled=True),build_disabled)]  )

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

    @commands.command()
    async def crop(self, ctx):
      if not await is_over_channel(ctx):
          return
      with open(info, "r")as f:
        data = json.load(f) 
      em = discord.Embed(title= f"{ctx.author.name} Crop Production", description = "Your farm yielded this/n", colour= discord.Color.green())
      em.set_footer(text=f"{ctx.author} croped their farm" , icon_url= ctx.author.avatar_url)
      crops = []
      crop_quantity = [] 
      if not await game.build_searcher(ctx, "miniature_farm"):
        crops = ["wheat", "carrot"]
        crop_quantity = [ random.randint(1,5), random.randint(1,5)] 
      elif game.build_searcher(ctx, "smol_farm") :
        crops = ["wheat", "carrot"]
        crop_quantity = [ random.randint(1,10), random.randint(1,10)] 
      elif game.build_searcher(ctx, "normal_farm"):
        crops = ["wheat","carrot", "potato","beet", "pumpkin_pie"]
        crop_quantity = [ random.randint(1,10), random.randint(1,10) ,
random.randint(1, 5), random.randint(1, 5), random.randint(1,2)]
      elif game.build_searcher(ctx, "big_farm"):
        crops = ["wheat","carrot", "potato", "beet", "sugarcane", "pumpkin_pie", "melon_slice"]
        crop_quantity = [ random.randint(1,15), random.randint(1,15), random.randint(1,15), random.randint(1,10), random.randint(1, 10), random.randint(1,3), random.randint(1,3)] 
      elif game.build_searcher(ctx, "giant_farm"):
        crops = ["wheat","carrot", "potato", "beet", "sugarcane", "pumpkin_pie", "melon_slice"]
        crop_quantity = [ random.randint(1,20), random.randint(1, 20), random.randint(1, 20), random.randint(1,15), random.randint(1, 20), random.randint(1, 8), random.randint(1, 8)] 
      else:
        await ctx.reply("You haven't build an farm")
        return
      for crop in crops:
        emoji = data["id"][crop]
        crop_name = crop.replace("_", " ").capitalize()
        crop_quantity = crop_quantity[crops.index(crop)] 
        em.description += f"{emoji} {crop_name} X {crop_quantity}\n"
        await game.inv_manager(ctx, crop, crop_quantity)
      await ctx.send(embed=em)

def setup(client):
    client.add_cog(Over(client))
