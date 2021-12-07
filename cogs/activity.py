import discord
from discord.ext import commands
from .functions.game_functions import GameFunction
from .functions.function import Func
import asyncio
import random
import json
from dislash import InteractionClient, ActionRow, Button, ButtonStyle, SelectMenu, SelectOption


game = GameFunction()
func = Func()
profiles = "cogs//functions//main_resources//profiles.json"
channels = "cogs//functions//main_resources//channels.json"
info =  "cogs/functions/main_resources/info.json"

class Action(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot        

    @commands.command()
    async def eat(self, ctx, eatable=None, quantity= None):
      with open(profiles, "r")as f:
        profile = json.load(f)
        inv = profile[str(ctx.author.id)]["inv"]
      with open(info, "r")as f:
        data = json.load(f)
      if eatable is None:
        msg = await ctx.send("Loading Eatable Food items from your inventory")
        while True:
          buttons = [] 
          em = discord.Embed(title= "Eat Command", description = "All eatable items from your inventory are here\nClick on button on eat an item.\nIf there is not button which means you have nothing to eat.", colour= discord.Colour.green())
          em.add_field(name="Health", value=await game.hearts(ctx))
          em.add_field(name="Hunger", value=await game.food(ctx))
          for item in inv:
            if item in data["food"] and item!= "wheat" and item!="spider_eye" and item!="sugarcane":
              buttons.append(ActionRow(Button( label=item.replace("_"," ").capitalize()+ f" X {inv[item]}" , style=ButtonStyle.blurple, custom_id = item)))
          await msg.edit(content=None, embed=em, components= buttons)
          try:
            waiter = await msg.wait_for_button_click(check = lambda x : x.author.id == ctx.author.id, timeout= 30)
          except asyncio.TimeoutError:
            await msg.edit(embed= discord.Embed(title= "Interaction Ended", description="***: )***\nThanks for using Minecord.", colour= discord.Colour.light_grey()), components = [])
            return
          button=waiter.clicked_button.custom_id
          health_increase = random.randint(1,20)
          await game.inv_manager(ctx, button, -1)
          game.food_level(ctx,health_increase)
      else:
        eatable = await game.get_id(eatable)
        if eatable is None:
          await ctx.send("The item you are trying to eat doesn't exists")
          return
        if not eatable in inv:
          await ctx.send("You don't even own this item")
          return
        if isinstance(int, quantity):
          if inv[eatable] < quantity:
            await ctx.send("Too large quantity")
            return
        elif quantity == "max" or quantity == "all":
          quantity = inv[eatable]
        else:
          await ctx.send("Quantity is not defined or invalid quantity.\nQuantity can be number or ```max``` or ```all```.")
          return      
        health_increase = data["food_health"][eatable] * quantity
        await game.inv_manager(eatable, -quantity)
        await game.food_level(health_increase)
        food_name = eatable.replace("_"," ").capitalize ()
        msg = await ctx.send(f"You ate {quantity}  {food_name}", components=Button(label= "Check Health", style=ButtonStyle.blurple, custom_id= "health_check_button") )
        waiter = await self.client.wait_for_button_click(check = lambda x : x.autuor.id == ctx.author.id, timeout= 30)
        cmd = await self.client.get_command("health")
        await ctx.invoke(cmd, ctx)

    @commands.command()
    async def test(self, ctx):
        raise asyncio.TimeoutError
        emoji = self.bot.get_emoji(898892686831017984) 
        msg = await ctx.send(
        f"{emoji} :x: This message has a select menu!",
        components=[
            SelectMenu(
                custom_id="test",
                placeholder="Choose up to 1 options.",
                max_values=1,
                options=[
                    SelectOption("Option 1", "value 1"),
                    SelectOption("Option 2", "value 2"),
                    SelectOption("Option 3", "value 3")
                ]
            )
        ]
    )
        def check(m):
          return m.author == ctx.author  
        '''inter = await msg.wait_for_dropdown(check=check)
        labels = inter.select_menu.selected_options
        await inter.reply(f"Your choices: {labels[0].label}")'''
        @self.bot.event()
        async def wait_for_dropdown(argument):
          print(argument)
          await ctx.send("Woah it worked")
      
    @commands.command()
    async def go(self, ctx, location=None):
      with open(profiles, "r")as f:
        profile = json.load(f)[str(ctx.author.id)]
        places = profile["places"]
      if location is None:
        components = []
        for place in places:
          components.append(ActionRow( Button( label= place.replace("_"," ").capitalize(), style = ButtonStyle.blurple, custom_id = place)))
        em = discord.Embed(title="Location to Go", description="Where do you want to go ?\nClick on button to go to a place.", colour= discord.Colour.blue())
        em.set_footer(text= "Use command location to know your location", url= ctx.author.url)
        msg= await ctx.send(embed=em, components= components)
        try:
          waiter = msg.wait_for_button_click(check = lambda x: x.author.id == ctx.author.id, timeout= 30)
        except asyncio.TimeoutError:
          msg.edit(embed= discord.Embed(title="Interaction Ended" , description="***: )***\nThanks for using Minecord", colour = discord.Colour.light_grey()))
          return
        location = waiter.clicked_button_cutom_id      
        location = await game.get_id(location)
        location_name = location.replace("_"," ").capitalize()
      await ctx.send(f"You went to {location_name}", file = open(f"cogs/assets/{location}.png"))
      await game.location(location)

    @commands.command(alias="inventory" )
    async def inv(self, ctx):
        with open (profiles, 'r')as f:
          profile = json.load(f)
          inv = profile[str(ctx.author.id)]["inv"]
        with open(info,"r")as f:
          data = json.load(f) 
        target = 0
        size = 0        
        for i in list(inv.keys()):
          size += 1
        if size == 0:
          await ctx.reply("You have nothing in your inventory.")
          return
        def get_type(id):
          for keys in data:
            if id in data[keys]:
              return keys
        def get_filter_size(id):
          size = 0 
          for i in inv:
            if i in data[id]:
              size += 1
        page = 1
        max_page =  int(size/5)
        filter = None 
        if size%5 != 0:
          max_page += 1
        pages = []
        target = 0
        for i in range(max_page):
          em = discord.Embed(title= f"{ctx.author.name}'s inventory", description = "Inventory Items", colour=discord.Colour.green() )
          if max_page > (i+1):
            items = 5 
          elif max_page == (i+1):
            remaining =  size%5
            if remaining == 0:
              items = 5 
            else:
              items = remaining 
          for item in range(items):
              id = list(inv.keys())[target] 
              name = id.replace( "_"," ").capitalize()
              emoji = data["id"][id]
              em.add_field(name = f"{target+1}) {emoji} {name} - {inv[id]}", value= f"ID ```{list(inv.keys())[target]}``` - {get_type(id)} - [Click here for item info](https://github.com/)", inline=False )
              target += 1
          em.set_footer(text=f"Use m!info [item] to get info on an item - Page {page+i} of {max_page}", icon_url=ctx.author.avatar_url)
          pages.append(em)   
         
        #Creating Buttons
        fd = Button(style = ButtonStyle.blurple, label= "»", custom_id = "fd")
        bk = Button(style = ButtonStyle.blurple, label= "«", custom_id = "bk")
        fd_disabled = Button(style = ButtonStyle.grey, label= "»", custom_id = "fd_disabled", disabled=True )
        bk_disabled = Button(style = ButtonStyle.grey, label= "«", custom_id = "bk_disabled",disabled=True)
        #Creating Select Menu.
        filter_bar = SelectMenu(custom_id="filter",
                placeholder="Choose up to 1 option.",
                max_values=1,
                options=[SelectOption("Blocks","block"),SelectOption("Jewel","jewels"), SelectOption("Usables","usables"), SelectOption("Food","food") ,                 SelectOption("Tools","tools"), SelectOption("Armour","armour")]) 
        
        #Sending Message
        if max_page ==  1:
          fd2 = fd_disabled
          await ctx.send(embed=pages[0], components=[ActionRow(bk_disabled, fd2)])
          return
        else:
          fd2 = fd 
        msg = await ctx.send(embed=pages[0], components=[filter_bar, ActionRow(bk_disabled, fd2)])
        while True:
          try:
            def check(m):
              return m.author.id == ctx.author.id  
            waiter, pending = await asyncio.wait([ 
              msg.wait_for_button_click(check=check, timeout = 30.0),
              msg.wait_for_dropdown(check=check, timeout=30.0 )
            ],                        return_when=asyncio.FIRST_COMPLETED)
          except asyncio.TimeoutError:       
            await msg.edit(embed=discord.Embed(title= "Interaction Ended", description="***: )***\nThanks for using Minecord",colour= discord.Colour.blue()), components=[ActionRow(bk_disabled, fd_disabled)])
            return
          for i in waiter:
            print(i.result)
          button = waiter.clicked_button.label
          backward = bk
          forward = fd  
          if button ==  "»":
            page += 1
            if page == max_page:
              forward = fd_disabled 
          elif button == "«":
            page -= 1
            if page == 1:
              backward = bk_disabled
          await msg.edit(embed = pages[page-1], components = [ActionRow(backward, forward)] )                        
                    
    @commands.command()
    async def craft(self, ctx, item):
        await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command(aliases=['adv'])
    @commands.cooldown(1,1800,type= commands.BucketType.user )
    async def adventure(self, ctx):
        chance = random.randint(1, 100) 
        adv = None 
        if chance <= 40:
          await ctx.reply("Haha you found nothing!")
          return
        elif chance <= 50:
          if not await game.place_searcher(ctx, "ocean"):
            adv = "ocean" 
        elif chance <= 60:
          if not await game.place_searcher(ctx, "village"):
            adv = "village" 
        elif chance <= 70:
          if not await game.place_searcher(ctx, "pillager_tower"):
            adv = "pillager_tower" 
        elif chance <= 80:
          if not await game.place_searcher(ctx, "cave"):
            adv = "cave" 
        elif chance <= 85:
          if not await game.place_searcher(ctx, "underground_cave"):
            adv = "underground_cave"
        elif chance <= 90:
          if not await game.place_searcher(ctx, "ravine"):
            adv = "ravine" 
        elif chance <= 92:
          if not await game.place_searcher(ctx, "igloo"):
            adv = "igloo" 
        elif chance <= 94:
          if not await game.place_searcher(ctx, "witch's_hut"):
            adv = "witch's_hut"  
        elif chance <= 96:
          if not await game.place_searcher(ctx, "jungle_temple"):
            adv = "jungle_temple" 
        elif chance <= 98:
          if not await game.place_searcher(ctx, "wooden_mansion"):
            adv = "wooden_mansion" 
        else:  
          if not await game.place_searcher(ctx, "desert_temple"):
            adv = "desert_temple"
        if adv is None:
          await ctx.reply("Haha you found nothing!")
          return
        await game.xp_manager(ctx, random.randint(1,10))
        await game.add_place(ctx, adv)      
        await ctx.reply(f"You went on an adventure and found a {adv}")

    @commands.command()
    @commands.cooldown(1, 3600,type=commands.BucketType.user)
    async def mine(self, ctx):
      #preperation
      tool_type = await game.tool_sercher(ctx, "pickaxe")     
      blocks = 0 
      max = 3
      if tool_type ==  None:
        await ctx.send("You don't own a pickaxe :(")     
        return          
      chance = random.randint(1, 100)
      build = await game.build_searcher(ctx,"shaf:t_mine")
      loc = game.user_location(ctx, world=True) 
      description = "" 
      if build :
        #max and blocks settings
        if tool_type == "netherite_pickaxe":
          blocks = random.randint(1,4) 
          max = 15 
        elif tool_type == "diamond_pickaxe":
          blocks = random.randint(1,3) 
          max = 12 
        elif tool_type == "gold_pickaxe":
          blocks = random.randint(1,2) 
          max = 10 
        elif tool_type == "iron_pickaxe":
          blocks = random.randint(1,2                     ) 
          max = 5        
      else:
        blocks = 1  
      block = None
      for i in range(blocks):
        quantity = random.randint(1, max)
        
        #Assigning Blocks
        if chance <= 20:
          #Giving Obsidian
          if tool_type == "netherite_pickaxe" or tool_type == "diamond_pickaxe" and chance == 1 and loc == "over":
            block = "obsidian"
            await game.xp_mana
        elif chance <= 30:
          #cobblestone
          if build and loc=="over":
            block = "cobblestone"                
        elif chance <= 40:
          #cobblestone
          if loc == "over":
            block = "cobblestone"          
        elif chance <= 50:
          #cobblestone
          if loc == "over"  :
            block = "cobblestone"
          elif loc == "nether":
            block = "netherrack" 
          else:
            block = "end_stone"       
        elif chance <= 60:
         #cobblestone
          if build and loc=="over":
            if chance <= 55:
              block = "cobblestone"
            else:
              block = "dirt"
          elif loc == "over"  :           block = "sand"  

          elif loc == "nether":
            block = "netherrack"
          else:
            block = "end_stone"       
        elif chance <= 70:
          if loc == "over":
            if build:
              block = "coal_ore"
              await game.xp_manager(ctx, random.randint(1,10))
            else:
              block = "dirt" 
          elif loc == "nether":
            block = "netherrack"         
          else:
            block = "end_stone"        
        elif chance <= 80:
          if loc == "over":
            if build:
              block =  "iron_ore"
              await game.xp_manager(ctx, random.randint(1,10))
            else:
              if chance <= 75:
                block = "dirt"
              else:
                block = "iron_ore"
                await game.xp_manager(ctx, random.randint(1,10))
          elif loc == "nether":
            block = "netherrack" 
          else:
            block = "end_stone" 
        elif chance <= 90:
          if loc == "over":
            if build:
              if chance <= 85:
                block = "iron_ore"
                await game.xp_manager(ctx, random.randint(1,10))
              elif chance <= 87:
                block = "sand"
              elif chance <= 89:
                block = "gravel"
              else:
                block = "diamond"
                await game.xp_manager(ctx, random.randint(1,30))
            else:
              block = "coal"
              await game.xp_manager(ctx, random.randint(1,10))
          elif loc == "nether":
            block = "netherrack" 
          else:
            block = "end_stone" 
        elif chance <= 100:
          if loc == "over":
            if build:
              if chance <= 92:
                block = "diorite" 
              elif chance <= 94:
                block = "andesite" 
              elif chance <= 96:
                block = "gold_ore"
                await game.xp_manager(ctx, random.randint(1,10))
              elif chance <= 98:
                block = "redstone_dust"
                await game.xp_manager(ctx, random.randint(1,10))
              else:
                block = "lapiz_lazuli"
                await game.xp_manager(ctx, random.randint(1,10))
            else:
              if chance <= 96:
                block = "gravel"
              elif chance <= 98:
                block = "diorite"
              else:
                block = "andesite" 
          elif loc == "nether":
            block = "nether_quartz"
            await game.xp_manager(ctx, random.randint(1,10))
            if chance == 100:
              block = "ancient_debris"
              await game.xp_manager(ctx, random.randint(1,50))
          else:
            block = "end_stone" 
        if block is None:
          await ctx.send("Haha you got nothing!")
          return
        game.log_cmd(ctx, "mine")
        with open(info, "r")as f:
          data = json.load(f)
          emoji = data["id"][block]
        description += f"{i+1}) {emoji} {block} x {quantity}"
        await game.inv_manager(ctx, block, quantity)
        await game.inv_manager(ctx, tool_type, -random.randint(1,2))
      em = discord.Embed(title="Mining Results", description= description  , colour = discord.Colour.green()) 
      await ctx.reply(embed=em)        

          
    @commands.command(aliases=["loc"] )     
    async def location(self, ctx):
        with open(profiles, 'r') as f:
            profile = json.load(f)
        loc = profile[str(ctx.author.id)]["world"]
        loc_sub = profile[str(ctx.author.id)]["location"]
        em = discord.Embed(title=f"{ctx.author.name}'s Location", description=f"World : {loc.capitalize()}\nLocation : {loc_sub.capitalize()}", colour = discord.Colour.blue() )
        await ctx.send(embed=em)

    @commands.command()
    async def kill(self, ctx, mob):
        if isinstance(mob, discord.member):
          print("Hai")
          pass
          return

    @commands.command()
    async def throw(self, ctx, item, value):
      with open(profiles,"r")as f:
        profile = json.load(f)
        inv = profile[str(ctx.author.id)]["inv"]
      if not item in inv:
        await ctx.send("The item u r looking for isn't in your inventory.")
        return
      if value == "max" or value == "all":
        profile[str(ctx.author.id)]["inv"].pop(item)
      else:
        try:
          value = int(value)
          await game.inv_manager(ctx, item, value)
        except:
          await ctx.send("Amount can be ```max```, ```all``` or an integer only")
          return
      with open(profiles, "w") as f:
        json.dump(profile, f, indent=4)
      await ctx.send("Item thrown from inventory")

    @commands.command()
    async def use(self, ctx, item):
      item = await game.get_id(item)
      if item is None:
        await ctx.reply("The item you are looking for dosen't exsists")
        return
      with open(profiles, "r") as f:
        profile = json.load(f)[str(ctx.author.id)]
        inv = profile["inv"]
      if not item in inv:
        await ctx.reply("That item isn't in your inventory lmao")
        return
      with open(info, "r") as f:
        data = json.load(f)
      if item in data["armour"]:
        pass
      elif item in data["usables"]:
        pass
      else:
        await ctx.reply("You cant use that item")

def setup(bot):
    bot.add_cog(Action(bot))
