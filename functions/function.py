import json
import discord
profile = ".\main_resources\profile.json"
channel = ".\main_resources\channels.json"

class func:
    """Functions which yield user details"""
    def __init__(self):
        pass

        # Game Functions
    def has_profile(self, ctx):
        """Checking if user has created a Profile or not"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        if str(ctx.author.id) in profiles:
            return True
        else:
            return False

    def is_not_restricted_channel(self, ctx):
        """Checking if the user is playing in the correct channel"""
        with open(channel, 'r') as f:
            channels = json.load(f)
            if str(ctx.guild.id) in channels:
                over = channels[str(ctx.guild.id)]['over']
                nether = channels[str(ctx.guild.id)]['nether']
                end = channels[str(ctx.guild.id)]['end']
                ch_id = str(ctx.channel.id)
                if ch_id == over or ch_id == nether or ch_id == end:
                    return True
                else:
                    return False
            else:
                return True

    def is_over_channel(self, ctx):
        """Checking if the user is playing in the Over World channel or not."""
        with open(channel, 'r') as f:
            channels = json.load(f)
        try:
            over_channel = channels[str(ctx.guild.id)]['over']
        except ValueError:
            # If they have not set up channels lets them play in any channel.
            return True
        if str(ctx.channel.id) == over_channel:
            return True
        else:
            return False



    async def inv(self, ctx, items, values: int):
        """Adding items to inventory"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        inv = profiles[str(ctx.author.id)]["inv"]
        if items in inv:
            a = inv[items]
            inv[items] = a + values
        else:
            inv["item"] = values
            json.dump(inv, f, indent=4)

    async def chanege_tools(self, ctx, tool):
        """Intalling tools in profile"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
            inv = profiles[str(ctx.author.id)]["inv"]
            default = ["sword", "axe", "pickaxe", "hoe", "shovel"]
            for items in inv:
                for tools in default:
                    if tools in items:
                        pass
                    else:
                        pass

    def search_inv_item(self, ctx, items: list):
        """Search item in inventory"""
        with open(profile, "r") as f:
            profiles = json.load(f)
        inv = profiles[str(ctx.author.id)]["inv"]
        for item in items:
            if item == list(inv.keys()):
                    return  True

    def info(self, ctx, info_type):
        """Returns person's info"""
        with open(profile,'r') as f:
            data = json.load(f)
            data = data[str(ctx.author.id)][info_type]
            return data

    def inv_tool(self, ctx, tool_type):
        """Returns person's info"""
        with open(profile,'r') as f:
            data = json.load(f)
            data = data[str(ctx.author.id)]["inv"][tool_type]
            return data

    def modify(self,ids , item:str, modification:str):
        """Opens profiles.json and modifies it."""
        with open(profile, 'w') as f :
            info = json.load(f)
            info[str(ids)][item] = modification
            json.dump(info, f, indent=4)
