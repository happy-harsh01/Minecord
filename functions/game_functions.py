from discord.ext import commands
import json
import random
import asyncio
from .function import Func
profile = "cogs//functions//main_resources//profiles.json"
info = "cogs//functions/main_resources//info.json"
func = Func()

class GameFunction:
    
    async def change_name(self, ctx, name):
      """Changes user name"""
      with open(profile, 'r') as f:
            profiles = json.load(f)
      profiles[str(ctx.author.id)]["name"] = name
      with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def change_health(self, ctx, value):
      """Changes user's health"""
      with open(profile, "r")as f:
        profiles = json.load(f)
        armour = profiles[str(ctx.author.id)]["armour"]
        health = profiles[str(ctx.author.id)]["health"]
        max_health = profiles[str(ctx.author.id)]["max_health"]
      if max_health == 100:
        health += value
        if health > 100:
          health = 100
      else:
        if value > 0:
          health += value
          if health > max_health:
            health = max_health
        else:
          for i in range(1, (-value)+1):
            health -= 1
            if health > 100:
              for armours in armour:
                armour[armours] -= random.randint(1,3)
                if armour[armours] == 0:
                  self.break_armour(ctx, armours)
      try:
        if health ==  0:
          await self.kill(ctx)
          await ctx.suthor.send("Oho you died.")
        elif health <= 30:
          await ctx.author.send("Oho you are on low health, try eating something.")
      except:
        pass
      with open(profile,"w")as f:
        profiles[str(ctx.author.id)]["armour"] = armour
        profiles[str(ctx.author.id)]["health"] = health
        profiles[str(ctx.author.id)]["max_health"] = max_health 
        json.dump(profiles, f, indent=4)
        
    async def create_profile(self, ctx, name):
        with open(profile, 'r') as f:
            profiles = json.load(f)
        user_profile = {"name": name, "health": 100, "max_health": 100, "food": 100, "world": "over", "location":"home", "armour":{}, "inv":{}, "inv_size": 25, "places":[], "adv":[], "builds":[],"log": {},"level":0, "xp":0} 
        profiles.update({str(ctx.author.id):user_profile})
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def armour(self, ctx, armour, value):
        """Mofidfies armour durability"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        armours = profiles[str(ctx.author.id)]["armour"]
        if armours[armour] == -value:
        # Breaking the armour if full durability has to be reduced
            self.break_armour(ctx, armour)
            return
        else:
            armours[armour] += value
        with open(profile, 'w') as f:
          profiles[str(ctx.author.id)]["armour"] = armours        
          json.dump(profiles, f, indent=4)

    async def equipt_armour(self, ctx, armour):
        """Equipts the armour and increases the max health"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        armours = profiles[str(ctx.author.id)]["armour"]
        with open(info, 'r') as f:
            infos = json.load(f)
        armour_dur = infos["armour"][armour]
        health_increase = infos["armour_health"][armour]
        if armour in armours:
          armours[armour] += armour_dur
        else:
          armours.update({armour: armour_dur})
        profiles[str(ctx.author.id)]["max_health"] += health_increase
        profiles[str(ctx.author.id)]["armour"] = armours
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def break_armour(self, ctx, name):
        """Breaks the armour and decreases the max health"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
            armours = profiles[str(ctx.author.id)]["armour"]
            max_health = profiles[str(ctx.author.id)]["max_health"]
        with open(info,'r') as f:
          data = json.load(f)
        max_health -= data["armour_health"][name]
        armours.pop(name)
        with open(profile, 'w') as f:
            profiles[str(ctx.author.id)]["armour"] = armours
            profiles[str(ctx.author.id)]["max_health"] = max_health 
            json.dump(profiles, f, indent=4)

    async def tool_sercher(self, ctx,tool_type):
      with open(profile,"r")as f:
        profiles = json.load(f) 
      inv = profiles[str(ctx.author.id)]["inv"]
      tools = ["wooden_", "stone_", "iron_", "gold_","diamond_", "netherite_"]
      for item in list(inv.keys()):
        for i in tools:
          if item == i + tool_type:
            return item  
      return None

    async def inv_manager(self, ctx, item, value):
        """Increases or decreases items value in the inventory
     Also adds new items to the inv"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        inv = profiles[str(ctx.author.id)]["inv"]
        inv_size =  profiles[str(ctx.author.id)]["inv_size"]
        with open(info, "r")as f:
          data = json.load(f)
        if item in inv:
            if inv[item] == -value:
                inv.pop(item)
                if item in data["tools"]:
                    await ctx.send(f"{ctx.author.mention} your {item} broke down")
            else:
                inv[item] += value
        else:
            inv_len = 0
            for i in list(inv.keys()):
              inv_len += 1
            if inv_size == inv_len:
              await ctx.send(f"{ctx.author.mention} your inventory is full, you dropped the {item}.\nPlease create space in your inventory using the ```drop``` command or use an ```chest```.")
              return
            inv.update({item: value})
        profiles[str(ctx.author.id)]["inv"] = inv
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def inv_searcher(self, ctx, item, value=None):
        """Searches for item in the inventory, if founded returns true else returns false"""       
        with open(profile, 'r') as f:
            profiles = json.load(f)
        inv =  profiles[str(ctx.author.id)]["inv"]
        if item in inv:
          if value is None: 
            return True
          elif inv[item] >= value:
            return True
          else: return False
        else:
            return False

    
    async def inv_size_manager(self, ctx, size):
        """Changes inv max size"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        profiles[str(ctx.author.id)]["inv_size"] == size
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def add_place(self, ctx, place, remove= False):
        """Adds place in the places list of the user id"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        if remove is False:
            profiles[str(ctx.author.id)]["places"].append(place)
        else:
            profiles[str(ctx.author.id)]["inv"].pop(place)
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def place_searcher(self, ctx, place):
        """Searches for place in user profile, if found returns true"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        if place in profiles[str(ctx.author.id)]["places"]:
            return True
        else:
            return False
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def adv_manager(self, ctx, adv):
        """Adds advancements in the user profile"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        profiles[str(ctx.author.id)]["adv"].append(adv)
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)
   
    async def adv_searcher(self, ctx, adv):
        """Searches for advancement in profile, if found returns true"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        if adv in profiles[str(ctx.author.id)]["adv"]:
            return True
        else:
            return False
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def builds_manager(self, ctx, build, remove=False):
        """Adds or removes builds from profile"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        if remove is False:
            profiles[str(ctx.author.id)]["builds"].append(build)
        else:
            profiles[str(ctx.author.id)]["builds"].pop(build)
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def build_searcher(self, ctx, build):
        """Searches for builds in profile, if found returns true"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        if build in profiles [str(ctx.author.id)]["builds"]:
            return True
        else:
            return False       

    def user_location(self, ctx, world = False ):
      with open(profile, "r")as f:
        prof = json.load(f)
      if not world:
        return prof[str(ctx.author.id)]["location"]
      else:
        return prof[str(ctx.author.id)]["world"]
        
    async def location_changer(self, ctx, world=False, location=False):
        """Changes user's location"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        if world != False:
            profiles[str(ctx.author.id)]["world"] = world
        if location != False:
            profiles[str(ctx.author.id)]["location"] = location
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def level(self, ctx):
        """Returns the level of the user"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        return profiles[str(ctx.author.id)]["level"]

    async def kill(self, ctx):
        """Kills the user and stores his inv item in temp inv for 1 min
    Also generates a kill code"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def xp_manager(self, ctx, xp):
        """Increases or decreases xp"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        profiles[str(ctx.author.id)]["xp"] += xp
        if await self.build_searcher(ctx, "xp_farm"):
          profiles[str(ctx.author.id)]["xp"] += xp
        if profiles[str(ctx.author.id)]["xp"] >= (profiles[str(ctx.author.id)]["level"]+1)*100:        
          profiles[str(ctx.author.id)]["xp"] -= (profiles[str(ctx.author.id)]["level"]+1) * 100
          profiles[str(ctx.author.id)]["level"] += 1
          await ctx.author.send(f"{ctx.author.mention} you reached level {profiles[str(ctx.author.id)]['level']}")
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)
        
    def log_cmd(self, ctx, cmd):          
      with open(profile, "r")as f:
        prof = json.load(f)
      if cmd in prof[str(ctx.author.id)]["log"]:
        prof[str(ctx.author.id)]["log"][cmd] += 1
      else:
        prof[str(ctx.author.id)]["log"].update({cmd: 1})
      with open(profile, "w")as f:
        json.dump(prof, f,indent=4)

    async def spawn(self, ctx):
      with open(info, "r")as f:
        data = json.load(f)
        mob_dict = data["mob"]
        mob_list = list(mob_dict.keys())
        mob = random.choice(mob_list) 
      with open(info, "w")as f:
        if not str(ctx.guild.id) in data:
          data["spawn"].update({ str(ctx.guild.id): mob})
          json.dump(data, f, indent=4)
          await ctx.send("A mob has spawned.\nUse command ```m!kill <mob_name>``` to kill the mob")

    async def despawn(self, ctx):
       with open(info, "r") as f:
         data = json.load(f)
         if str(ctx.guild.id) in data["spawn"] :
           mob = data ["spawn"][str(ctx.guild.id)]
           await ctx.channel.send(f"A wild {mob} despawned.")
           data["spawn"].pop( str(ctx.guild.id))
       with open(info, "w") as f:
        json.dump(data, f, indent=4)

    async def get_id(self, id):
      with open(info, "r")as f:
        data = json.load(f)
      for aliases in data["alias"]:
        if id in data["alias"][aliases]:
          return aliases
        if aliases == id:
          return aliases

    def food_level(self, ctx, value):
      with open(profile, "r") as f:
        profiles = json.load(f)
      if profiles[str(ctx.author.id)]["food"] + value > 100:
        profiles[str(ctx.author.id)]["food"] = 100
      else:
        profiles[str(ctx.author.id)]["food"] += value
        if profiles[str(ctx.author.id)]["food"] < 0:
          profiles[str(ctx.author.id)]["food"] = 0
      with open(profile, "w") as f:
        json.dump(profiles, f, indent=4)

    async def hearts(self, ctx):
      """Return String of hearts according to user's health."""
      with open(profile, "r") as f:
        profiles = json.load(f)
      health = profiles[str(ctx.author.id)]["health"]
      max_health = profiles[str(ctx.author.id)]["max_health"]
      heart = "<:minecraft_heart:898867063924330507>"
      half_heart = "<:half_heart:914832762773602324>"
      user_heart = ""
      if health == max_health:
        user_heart = heart*10
        return user_heart
      for i in range(1,health+1):
        if (i % 10) == 0:
          # Replacing Half heart by full heart.
          user_heart = user_heart.replace(half_heart, heart)
        elif (i % 5) == 0:
          user_heart += half_heart
      
      return user_heart

    async def food(self, ctx):
      """Return String of foods according to user's food level."""
      with open(profile, "r") as f:
        profiles = json.load(f)
      foods = profiles[str(ctx.author.id)]["food"]
      if foods == 0:
        return "0"
      food = "<:food:914830073067102218>"
      half_food = "<:half_food:914829417501589546>"
      user_food = ""
      if foods == 100:
        user_food = food*10
        return user_food
      for i in range(1,foods+1):
        if (i % 10) == 0:
          # Replacing Half heart by full heart.
          user_food = user_food.replace(half_food, food)
        elif (i % 5) == 0:
          user_food += half_food
      return user_food
