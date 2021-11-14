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

mine_no = {"Netherite Pickaxe":"20-30","Diamond Pickaxe":"20-25",
"Gold Pickaxe":"15-25",'Iron Pickaxe':"10-15", 'Stone Pickaxe': '1-10',"Wooden Pickaxe":"1-5"}

class Action(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot        

    @commands.command()
    async def eat(self, ctx):
        await ctx.send("This command is yet to be made!\nSorry :(")

    @commands.command()
    async def test(self, ctx):
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
        inter = await msg.wait_for_dropdown(check=check)
        labels = inter.select_menu.selected_options
        await inter.reply(f"Your choices: {labels[0].label}")            
      
    @commands.command()
    async def go(self, ctx, location = None):
      with open(profiles, "r")as f:
        profile = json.load(f)
        places = profile[str(ctx.author.id)]["places"]
      if location is None:
        actionRow = []
        #Creating Buttons according to places user has discovered
        i = 1 
        for place in places:
          button = Button(
            label = place,
            custom_id = f"button{i}",
            style = ButtonStyle.blurple 
          )
          i += 1
          actionRow.append(button)
        print(ActionRow(actionRow))
        await ctx.send("Where do you wanna go ?\nClick on one of the buttons below", components = [ActionRow(actionRow)] )
        return

    @commands.command(alias="inventory" )
    async def inv(self, ctx):
        with open (profiles, 'r')as f:
          profile = json.load(f)
          inv = profile[str(ctx.author.id)]["inv"]
        target = 0
        size = 0        
        for i in list(inv.keys()):
          size += 1
        if size == 0:
          await ctx.reply("You have nothing in your inventory.")
          return
        page = 1
        max_page =  int(size/5)
        filter = None 
        if size%5 != 0:
          max_page += 1
        text = f"Use m!info [item] to get info on an item - Page {page} of {max_page}" 
        with open(info, "r") as f:
          data = json.load(f) 
        embed = discord.Embed(title=f"{ctx.author.name}'s inventory", description="Inventory Items")
        embed.set_footer(text=text, icon_url=ctx.author.avatar_url)
        
        #Creating Buttons
        fd = Button(style = ButtonStyle.blurple, label= "»", custom_id = "fd")
        bk = Button(style = ButtonStyle.blurple, label= "«", custom_id = "bk")
        fd_disabled = Button(style = ButtonStyle.grey, label= "»", custom_id = "fd_disabled", disabled=True )
        bk_disabled = Button(style = ButtonStyle.grey, label= "«", custom_id = "bk_disabled",disabled=True)

        #Sending Message
        if size <=  5:
          for i in list(inv.keys()):
            for j in list(data.keys()):
              if i in data[j]:
                name = i.replace("_", " ")
                name = name.capitalize()
                emoji = data["id"][list(inv.keys())[i]] 
                embed.add_field(name = f"{target+1}) {emoji} {name} - {inv[i]}", value= f"ID ```{list(inv.keys())[i]}``` - {j}")
                
            await ctx.reply(embed = embed, components = [ActionRow(bk_disabled, fd_disabled)] )    
            return
        for i in range(target, target + 5):
          for j in list(data.keys()):           
            if list(inv.keys())[i] in data[j]:
              name = list(inv.keys())[i].replace("_", " ")
              name = name.capitalize()
              emoji = data["id"][list(inv.keys())[i]] 
              embed.add_field(name= f"{target+1}) {emoji} {name} - {inv[list(inv.keys())[i]]}", value= f"ID ```{list(inv.keys())[i]}``` - {j}")
              target += 1
              break           
        msg = await ctx.reply(embed=embed, components= [ActionRow(bk_disabled, fd )]  )
        def check(m):
          return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        while True:
          print("Target = ",target)
          try:
            waiter = await msg.wait_for_button_click(check=check, timeout = 30.0  )
          except asyncio.TimeoutError:
            await msg.edit(embed=embed, components=[ActionRow(bk_disabled, fd_disabled)])
            return
          button = waiter.clicked_button.label

          #Monitoring Forward Button Click
          if button ==  "»":
            page += 1
            if target == 0:
              target = 5 
            button2 = fd                       
            i = 0      
            while True:
              print("i ",i, target)
              item = list(inv.keys())[target]
              if filter != None:
                if not item in data[filter]:
                  target += 1
                  continue
              emoji = data["id"][item]   
              name = item.replace("_"," ").capitalize()
              embed.set_field_at(i, name= f"{target+1}) {emoji} {name} - {inv[item]}", value= f"ID ```{item}``` - {func.item_type(item)}")
              target += 1                           
              if i == 4:  
                break
              i += 1 
              if target == size:
                button2 = fd_disabled
                if i != 4:
                  y = 4 
                  for i in range(i,5):
                    embed.remove_field(y)
                    y -= 1 
                    print("removed ",i)
                break
            embed.set_footer(text=f"Use m!info [item] to get info on an item - Page {page} of {max_page}", icon_url=ctx.author.avatar_url)  
            await msg.edit(embed=embed, components=[ActionRow(bk, button2)]  )  
          
        #Monitoring Backward Button Click
          elif button == "«":
            page -= 1
            button1 = bk             
            i = 0
            if target == size:
              print("max size reached", size%5)
              target -= size%5
              print(target)         
            while True:
              item = list(inv.keys())[target]
              if filter != None:
                if not item in data[filter]:
                  target -= 1
                  continue
              emoji = data["id"][item]
              name = item.replace("_"," ").capitalize()
              try:
                embed.set_field_at(i, name= f"{target+1}) {emoji} {name} - {inv[item]}", value= f"ID ```{item}``` - {func.item_type(item)}")
              except IndexError:
                embed.add_field( name= f"{target+1}) {emoji} {name} -{inv[item]}", value= f"ID ```{item}``` - {func.item_type(item)}")
              i += 1               
              if i == 4:
                break
              target -= 1
              if target == 0:
                button1 = bk_disabled
                break
            embed.set_footer(text=f"Use m!info [item] to get info on an item - Page {page} of {max_page}", icon_url=ctx.author.avatar_url)
            await msg.edit(embed=embed, components=[ActionRow(button1,fd)]  )
                    
                    

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
       

def setup(bot):
    bot.add_cog(Action(bot))

