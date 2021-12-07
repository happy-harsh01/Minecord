import json
import discord
from discord.ext import commands
profile = "cogs/functions/main_resources/profiles.json"
channel = "cogs/functions/main_resources/channels.json"
restricted_channels = "cogs/functions/main_resources/restricted_channels.json"
info = "cogs/functions/main_resources/info.json"


class Func:

    def __init__(self, client=None ):
        self.client = client 
 
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
 
    async def is_over_channel(self, ctx):
        """Checking if the user is playing in the Over World channel or not."""
        with open(channel, 'r') as f:
            channels = json.load(f)
        try:
            over_channel = channels[str(ctx.guild.id)]['over']
        except KeyError:
            # If they have not set up channels lets them play in any channel.
            return True
        if str(ctx.channel.id) == over_channel:
            return True
        else:         
            await ctx.send(f"{ctx.author.mention} you can use over world commands in <#{over_channel}> channel.")       
            ctx.command.reset_cooldown( ctx)
            return False

    
    @staticmethod
    async def is_restricted_channel(message, guild = None):
        guild_id = ""
        channel_id = ""
        if isinstance(message, discord.TextChannel):
          channel_id = message.id
          guild_id = guild
        else:
          guild_id = str(message.guild.id)
          channel_id = message.channel.id
        with open(restricted_channels, "r") as f: 
          channels = json.load(f)
        try:
            restricted_chan = channels[guild_id]
            if channel_id in restricted_chan:               
                return True
            else:
                return False
        except KeyError:         
            return False

    async def is_correct_channel(self, ctx):
        """Check whether the user is playing in the correct channel or not"""
        with open(profile, 'r') as f:
            profiles = json.load(f)
            loc = profiles[str(ctx.author.id)]["location"]
        with open(channel, 'r') as f:
            channels = json.load(f)   
        if str(ctx.guuld.id) in channels:
            try:
              if channels[str(ctx.guild.id)][loc] == str(ctx.channel.id):
                return True
              else:
                return False
            except KeyError:
              return True
        else:
            return True
      
    async def send_embed(self, ctx, title, description,colour,fields=None, footer=False):
        embed = discord.Embed(title=title, description=description)
        if colour == 'red':
          embed.colour = discord.Colour.red()
        elif colour == 'green':
          embed.colour = discord.Colour.green()
        if footer == "plain":
          embed.set_footer(text=f" {ctx.author}", icon_url=ctx.author.avatar_url)
        elif footer != False:
            embed.set_footer(text=f"Request by {ctx.author}", icon_url=ctx.author.avatar_url)        
        if fields != None and fields != {}:
            for i in list(fields.keys()):
                          embed.add_field(name=i,value=fields[i] )
        await ctx.send(embed=embed)

    @staticmethod
    def item_type(item):
        with open(info, 'r')as f:
          data = json.load(f)
        for i in list(data.keys()):
          if item in data[i]:
            return i

    
