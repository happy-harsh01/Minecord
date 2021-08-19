from discord.ext import commands
import json


class GameFunction:

    @staticmethod
    def get_profiles():
        with open(".\\main_resources\\profile.profile.json", "r") as f:
            return json.load(f)
    
    async def break_tool(self, tool):
        """Breaks a tool , removes it from inventory and announces it."""
        pass
    
    async def tool_durability_modifier(self, value, type):
        """Increase or decreases Tools durability equipped by user. Tool health increases only when it is enchanted by 
        unbreaking and decreases when it gets damage."""
        pass
    
    async def armour_durability_modifier(self, value, type):
        """Increase or decreases Armour health(durability) equipped by user. Armour health increases only when it 
        is enchanted by unbreaking and decreases when it gets damage."""
        pass
    
    async def armour_breaker(self, armour):
        """Breaks user's armour and decreases his health increased by wearing it and also announces it."""
        pass

    async def armour_equiptor(self, amour):
        """When user equipts armour his health is increased."""
        pass
    
    async def increase_health(self, health_point):
        """Increases the players health when he eats something."""
        pass
    
    async def kill(self, ):
        """Kills the user, his inventory items are stored for sometime"""
        pass
    
    async def create_profile(self, ctx, name):
        """Creates user's profile contianing his data."""
        profile = {
            "name": name,
            "health": 100,
            "world": "Over World",
            "location": "Home",
            "inv": [],
            "places": [],
            "builds": [],
            "advancements": [],
            "xp": 0
        }
        profiles = self.get_profiles()
        profiles.update({str(ctx.author.id): profile})
        with open(".\\main_resources.\\profile.json", "w") as f:
            json.dump(profile, f)
        print(f"New profile created for {ctx.author}")
    
    async def xp(self, ctx, xp):
        """Increases or decreases the user's level"""
        profiles = self.get_profiles()
        profiles[ctx.author.id]["xp"] += xp
    
    async def fight(self, ):
        """Fights two player or mobs and subsequently decreses their health."""
        pass
    
    async def spawn(self, ):
        """Spawns mob randomly when they chat and adds mob to the list."""
        pass

    async def inv_manager(self, item, decrement=0, increment=0):
        """Manages inventory items by adding new items or sorting them
        If item is present modifies its quantity else adds that item in the inventory.
        Either increment or decrement argument is requied , both are not allowed to be given."""
        if decrement > 0 and increment > 0:
            raise ValueError("Both increment and decrement are not allowed to be given.")
        inv = self.get_profiles()["inv"]
        inv_items = list(inv.keys())
        if item in inv_items:
            orignal_value = inv[item]
            if increment > 0:
                inv_items = orignal_value + increment
            else:
                inv_items = orignal_value - decrement
        elif increment > 0:
            inv[item] = increment

    async def add_advancement(self, advancement):
        """Adds an advancement to the user's profile and also announces it."""
        profile = self.get_profiles()
        advancements = profile["advancements"]
        advancements.append(advancement)
        with open(".\\main_resources\\profile.profile.json", "w") as f:
            json.dump(advancements, f)
    
    async def place_searcher(self, place):
        """Searches for place in user places."""
        profile = self.get_profiles()
        places = profile["places"]
        if place in places:
            return True
        else:
            return False
        
    async def level(self, ctx):
        """Returns the user level."""
        profile = self.get_profiles()
        xp = profile[ctx.author.id]["xp"]
        return str(xp/10)
