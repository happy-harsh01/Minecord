import discord
from discord.ext import commands
import json
from .functions.game_functions import GameFunction
from .functions.function import Func
import asyncio
from dislash import ActionRow, Button, ButtonStyle

game = GameFunction()
func = Func()
profile = "cogs//functions//main_resources//profiles.json"
channel = "cogs//functions//main_resources//channels.json"
restricted = "cogs//functions//main_resources//restricted_channels.json"


class Settings(commands.Cog):
    def __init__(self, client):
        self.client = client                       

    @commands.command()
    async def start(self, ctx):
        if await func.has_profile(ctx):
          em = discord.Embed(title='Profile Already Exists', description='You already have a profile.\nWhat are you looking for ?', colour=discord.Colour.red()) 

          await ctx.send(embed=em)
          return
        def check(m):
            return m.author.id == ctx.author.id and m.channel == ctx.channel

        try:
            await ctx.send("Enter a name for your Character : ")
            msg = await self.client.wait_for('message', timeout=30, check=check)
            await game.create_profile(ctx, msg.content)
            em = discord.Embed(title='Profile Created Successfully', description='Profile has been created.\nYou can start playing now', colour=discord.Colour.green())
            await ctx.send(embed=em )
        except asyncio.TimeoutError:
           await ctx.send(f"{ctx.author.mention} did not replied in time. What the hell he is doing!")

    @commands.command(aliases=["delete profile"])
    async def delete(self, ctx):
        em =  discord.Embed(title='Profile Deletion Protocol', description='''Are you sure want to delete your profile ?
    This step is highly irreversible.
    Are you sure ?
    Type ```Y``` or ```Yes``` to confirm or ```N``` or ```No``` to go back.''', colour=discord.Colour.red())
        await ctx.send(embed=em  )

        def check(m):
            return m.author.id == ctx.author.id and m.channel == ctx.channel

        try:
            msg = await self.client.wait_for(event='message', timeout=30, check=check)
            if msg.content.lower() == 'yes' or msg.content.lower() == "y":
                with open(profile, 'r') as f:
                    person = json.load(f)
                    person.pop(str(ctx.author.id))
                with open(profile, 'w') as f:
                    json.dump(person, f, indent=4)
                em =         discord.Embed(title='Profile Deleted', description='Profile has been successfully deleted.', colour=discord.Colour.red())
                em.set_footer(text= f"{ctx.author}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=em )
            else:
                await ctx.send('You stepped back from profile deletion!')
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} did not replied in time. What the hell he is doing!")

    @commands.command()
    async def change_name(self, ctx, name_new):
        await game.change_name(ctx, name_new)
        em = discord.Embed(title='Name Changed Sucessfully', description=f'Succesfully changed your character name to {name_new}', colour=discord.Colour.green())  
        await ctx.send(embed=em )

      
    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def quick_setup(self, ctx):
        def check(m):
            return m.channel == ctx.channel and m.author == ctx.author
        try:
            await ctx.send("Enter the over world channel (only mention the channel)")
            msg = await self.client.wait_for(event= 'message', timeout=60.0, check=check)
            over = msg.content
            await ctx.send("Enter the nether world channel")
            msg = await self.client.wait_for('message', timeout=60.0, check=check)
            nether = msg.content
            await ctx.send("Enter the end world channel")
            msg = await self.client.wait_for(event= 'message', timeout=60.0, check=check)
            end = msg.content
            if await func.is_restricted_channel(over[2:-1]):
              await ctx.reply(f"{over} is restricted channel")
              return
            if await func.is_restricted_channel(nether[2:-1]):
              await ctx.reply(f"{nether} is restricted channel")
              return
            if await func.is_restricted_channel(end[2:-1]):
              await ctx.reply(f"{end} is restricted channel")
              return
            with open(channel, 'r') as f:
                channels = json.load(f)
            if str(ctx.guild.id) in channels:
                channels[str(ctx.guild.id)]['over'] = over[2:-1]
                channels[str(ctx.guild.id)]['nether'] = nether[2:-1]
                channels[str(ctx.guild.id)]['end'] = end[2:-1]
            else:
                channels.update({str(ctx.guild.id):{'over':over[2:-1],'nether': nether[2:-1], 'end':end[2:-1]}})
            with open(channel, 'w') as f:
                json.dump(channels, f, indent=4)
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention} did not replied in time what the hell he is doing.")
  
    @commands.command(alias="restrict")
    @commands.has_guild_permissions(manage_channels=True)
    async def add_restricted_chan(self, ctx, restricted_channel: discord.TextChannel):       
        """Adds the given channel in restricted channel list."""
        restricted_channel = restricted_channel.id 
        with open(restricted, 'r') as f:
            channels = json.load(f)
            if str(ctx.guild.id) in channels:       
                restrict_list =channels[str(ctx.guild.id)]             
                if str(ctx.channel.id) in restrict_list:
                  await func.send_embed(ctx, "Channel Already Exists", f"<#{restricted_channel}> is already a restricted channel", "red")
                  return
                restrict_list.append(restricted_channel)            
                channels[str(ctx.guild.id)] = restrict_list 
            else:
                channels.update({str(ctx.guild.id): [restricted_channel]})

        with open(restricted, 'w') as f:
            json.dump(channels, f, indent=4)
        await func.send_embed(ctx, "Added Restricted Channel", f"Successfully added <#{restricted_channel}> as a restricted channel.\nMinecord will not respond to any message it this channel", "green")
      
    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def set_over_channel(self, ctx, server_channel: discord.TextChannel):
        if await func.is_restricted_channel(server_channel, str(ctx.guild.id)):
         await ctx.reply(f"<£{server_channel.id}> is a restricted channel can't set it.")
         return
        with open(channel, 'r') as f:
            channels = json.load(f)
        if str(ctx.guild.id) in channels:
          if "over" in channels[str(ctx.guild.id)]:
            channels[str(ctx.guild.id)]["over"] = (server_channel.id)
          else: 
            channels[str(ctx.guild.id)].update({"over": (server_channel.id)})
        else:
          channels.update({str(ctx.guild.id): {"over": (server_channel.id)}})  
        with open(channel, 'w') as f:
            json.dump(channels, f, indent=4)
        await ctx.reply(f"Set <#{server_channel.id}> as a over world chan channel.")

    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def set_nether_channel(self, ctx, server_channel: discord.TextChannel):
        if await func.is_restricted_channel(server_channel, str(ctx.guild.id)):
         await ctx.reply(f"<£{server_channel.id}> is a restricted channel can't set it.")
         return
        with open(channel, 'r') as f:
            channels = json.load(f)
        if str(ctx.guild.id) in channels:
          if "nether" in channels[str(ctx.guild.id)]:
            channels[str(ctx.guild.id)]["nether"] = server_channel.id
          else:
            channels[str(ctx.guild.id)].update({"nether": server_channel.id})
        else:
          channels.update({str(ctx.guild.id):{"nether": server_channel.id}})
        
        with open(channel, 'w') as f:
            json.dump(channels, f, indent=4)
        await ctx.reply(f"Set <#{server_channel.id}> as nether world channel.")
    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def set_end_channel(self, ctx, server_channel: discord.TextChannel):
        if await func.is_restricted_channel(server_channel, str(ctx.guild.id)):
         await ctx.reply(f"<£{server_channel.id}> is a restricted channel can't set it.")
         return
        with open(channel, 'r') as f:
            channels = json.load(f)
        if str(ctx.guild.id) in channels:
          if "end" in channels[str(ctx.guild.id)]:
            channels[str(ctx.guild.id)]["end"] = server_channel.id
          else:
            channels[str(ctx.guild.id)].update({"end": server_channel.id})
        else:
          channels.update({str(ctx.guild.id):{"end": server_channel.id}})
        
        with open(channel, 'w') as f:
            json.dump(channels, f, indent=4)
        await ctx.reply(f"Set <#{server_channel.id}> as end world channel.") 

    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    async def unrestrict(self, ctx, server_channel: discord.TextChannel):
        if await func.is_restricted_channel(server_channel, str(ctx.guild.id)):
          with open(restricted, "r+") as f:
            restrict = json.load(f)
            restrict[str(ctx.guild.id)].remove(server_channel.id)
            if restrict[str(ctx.guild.id)] == []:
              restrict.pop(str(ctx.guild.id))
            json.dump(restrict, f, indent = 4)
            await func.send_embed(ctx, "Removed Restric Channel",f"Successfull removed <#{server_channel.id}> from restrictions. \nNow Minecord will respond to commands in that channel." , "green", footer=True)
        else:
            await ctx.send("That channel isn't a restricted one")
      
def setup(client):
    client.add_cog(Settings(client))
