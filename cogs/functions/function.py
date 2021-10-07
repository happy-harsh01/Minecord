import json
profile = ".\\main_resources\\profile.json"
channel = ".\\main_resources\\channels.json"
restricted_channels = ".\\main_resources\\restricted_channels.json"


class Func:

    # Game Functions
    @staticmethod
    async def has_profile(ctx):
        """Checking if user has created a Profile or not"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
        if str(ctx.author.id) in profiles:
            return True
        else:
            return False

    @staticmethod
    async def is_over_channel(ctx):
        """Checking if the user is playing in the Over World channel or not."""
        with open(channel, 'r') as f:
            channels = json.load(f)[str(ctx.guild.id)]['over']
        try:
            over_channel = channels
        except KeyError:
            # If they have not set up channels lets them play in any channel.
            return True
        if str(ctx.channel.id) == over_channel:
            return True
        else:
            return False

    @staticmethod
    async def add_inv(ctx, item, quantity: int):
        """Adds single item of definite quantity to inventory"""
        with open(profile, 'r') as f:
            inv = json.load(f)[str(ctx.author.id)]["inv"]
        if item in inv:
            a = inv[item]
            inv[item] = a + quantity
        else:
            inv.update({item: quantity})
        with open(profile, 'w') as f:
            json.dump(f, inv, indent= 4)

    @staticmethod
    async def search_inv_item(ctx, *items):
        """Searches for an item in the inventory, if item is present returns True else returns False"""
        with open(profile, "r") as f:
            inv = json.load(f)[str(ctx.author.id)]["inv"]
        item_found = False
        for item in items:
            if item == list(inv.keys()):
                    item_found = True
            else:
                item_found = False
        return item_found

    @staticmethod
    def name(ctx):
        with open(profile, 'r') as f:
            name = json.load(f)[str(ctx.author.id)]["name"]
            return name

    @staticmethod
    async def info(ctx, info_type):
        """Returns person's info"""
        with open(profile, 'r') as f:
            data = json.load(f)
            data = data[str(ctx.author.id)][info_type]
            return data

    @staticmethod
    async def is_not_restricted_channel(message):
        with open(restricted_channels, "r") as f:
            channels = json.load(f)
        try:
            if message.channel.id in channels[str(message.guild.id)]:
                return False
            else:
                return True
        except KeyError:
            pass
