from discord.ext import commands
import json
profile = ".//main_resources//profiles.json"
info = ".//main_resources//info.json"

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
        with open(profile, 'r') as f:
            profiles = json.load(f)
            health = profiles[str(ctx.author.id)]["health"]
        if health > 100:
            pass
        else:
            if health == -value:
                self.kill(ctx)
                return
            else:
                health += value
        profiles[str(ctx.author.id)]["health"] = health
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def create_profile(self, ctx, name):
        with open(profile, 'r') as f:
            profiles = json.load(f)
        user_profile = {"name": name, "health": 100, "max_health": 100, "world": "over", "location":"home", "armour":{}, "inv":{}, "inv_size": 25, "places":[], "adv":[], "builds":[], "xp":0} 
        profiles.update(user_profile)
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)
    async def armour_durability_modifier(self, ctx, armour, value):
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
        profiles[str(ctx.author.id)]["armour"] = armours
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def equipt_armour(self, ctx, name):
    """Equipts the armour and increases the max health"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def break_armour(self, ctx, name):
    """Breaks the armour and decreases the max health"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def inv_manager(self, ctx, item, value):
    """Increases or decreases items value in the inventory
     Also adds new items to the inv"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        inv = profiles[str(ctx.author.id)]["inv"]
        if item in inv:
            if inv[item] == -value:
                inv.pop(item)
                if 'pickaxe' in item or 'sword' in item or 
                'axe' in item or 'shovel' in item or 'hoe' in item:
                    await ctx.send(f"{ctx.author.mention} your {item} broke down")
            else:
                inv[item] += value
        else:
            inv.update({item: value})
        profiles[str(ctx.author.id)]["inv"] = inv
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def inv_searcher(self, ctx, item):
    """Searches for item in the inventory, if founded returns true else returns false"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        if item in profiles[str(ctx.author.id)]["inv"]:
            return True
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
            profiles[str(ctx.author.id)]["inv"].pop(places)
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

    async def build_searcher(self, ctx, name):
    """Searches for builds in profile, if found returns true"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)
    
    async def location_changer(self, ctx, world=False, location=False):
    """"Changes user's location"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

    async def level(self, ctx):
    """Returns the level of the user"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)

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
        with open(profile, 'w') as f:
            json.dump(profiles, f, indent=4)
