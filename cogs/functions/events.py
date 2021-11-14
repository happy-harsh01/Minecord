import discord
from discord.ext import commands
from .function import Func
import json
import asyncio
import random
from .game_functions import GameFunction

profile = "cogs/functions/main_resources/profile.json"
channels = "cogs/functions/main_resources/channels.json"
restricted =  "cogs/functions/main_resources/restricted_channels.json"
info = "cogs/functions/main_resources/info.json" 
over = ["chop", "crop", "fish", "trade", "enchant", "cave", "build"]

func = Func()
game = GameFunction() 

class Events:
    """Tells the bot what to do when an event occurs."""

    def __init__(self, client):
        self.client = client 
    
    async def on_message(self, message: discord.ext):          
        cmd = message.content.lower()[2:]
        if message.author == self.client.user:
            return
        if isinstance(message.channel, discord.DMChannel):
          if message.author.id == 894072003533877279:
            em = discord.Embed(title = "Do you want to send this message ?", description = message.content , colour = discord.Colour.red() ) 
            msg =  await message.channel.send(embed = em )           
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            def check(reaction, user):
              return user == message.author and str(reaction.emoji) == '✅'
            try:
              react, user = await self.client.wait_for( "reaction_add",check = check, timeout=30)
              await message.channel.send("Whom do you want to send ?")
              try:
                def check2(m): 
                  return m.author.id == message.author.id and m.channel.id == message.channel.id    
                mess = await self.client.wait_for("message", check=check2,timeout = 30)
              except asyncio.TimeoutError:
                return
              user =  self.client.get_user(int(mess.content))
              await user.send(message.content)
              em.set_footer(text="Sent" )
              await msg.edit(embed=em)
            except asyncio.TimeoutError:
              return
          else:
            await message.channel.send(message.content)        
          return
        if await func.is_restricted_channel(message):
          return       
        if self.client.user.mentioned_in(message):
            em = discord.Embed(title= 'Minecord Bot', description= "Hi I am Minecord, The Discord Minecraft bot, my prefix is ```m!```", colour= discord.Colour.green())
            em.set_thumbnail(url = self.client.user.avatar_url)
            em.add_field(name= "Invite", value="To invite the bot use the ```m!invite``` command")
            em.add_field(name= "Bug Fix", value="Report bugs and suggestions using the ```m!bug``` command")
            await message.channel.send(embed=em)
            return
        if (random.randint(1,10)) == 1:
          await game.spawn(message)
        if not message.content.startswith("m!"):
            return
        if 'start' in cmd or 'help' in cmd:
            await self.client.process_commands(message)        
            return
        if not await func.has_profile(message):
            await message.channel.send(f"{message.author.mention} you haven't created your profile yet.\nCreate your profile with the ```start``` command and start playing!")
            return
        await self.client.process_commands(message)        
      
    async def on_guild_leave(self, guild):
        """Handling when Bot leaves a server"""
        # Removing channels connections
        with open(channels, 'r') as f:
            chan = json.load(f)
        try:
            chan.pop(str(guild.id))
        except KeyError:
            print("Minecord left someones server, they didn't setup channels.")
        with open('channels.json:', 'w') as f:
            json.dump(chan, f, indent=4)
    
    async def on_command_error(self,ctx, error):
        """Handling errors"""
        if isinstance(error, commands.CommandNotFound):
            print("Ignoring one Command not found error.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await func.send_embed(ctx, "Missing Required Argument.", "Please give all the required arguments.\nUse ```m!help <command>``` to get more help", "red")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Please give me all permissions.\n```send message, embed links, attach files```")
        elif isinstance(error,commands.CommandOnCooldown):
          await func.send_embed(ctx, "Command On Cooldown", f"Take a rest, try again after ```{int(error.retry_after)}``` seconds", "red")
        elif isinstance(error,commands.MissingPermissions):
          em = discord.Embed( title=":x: Missing Permission :x:", description= "You are missing ```Manage Channel``` permission to use this command.", colour= discord.Colour.red())
          em.set_footer(text=f"{ctx.author} Missing Permission" , icon_url= ctx.author.id )
          await ctx.reply(embed=em)
        elif isinstance(error, commands.MemberNotFound):
          await ctx.send("Member not found")
        else:
            print(f"ERROR: {error}")
            agent = self.client.get_user(894072003533877279)
            if agent != None:
              await agent.send(f"CRASH REPORT ON COMMAND {ctx.command} : {error}")

    
    async def on_command_completion(self, ctx):     
      chance = random.randint(1,3)
      tip = random.randint(1,10)
      if chance == 2:       
        await game.xp_manager(ctx, random.randint(1,10))
      if tip == 10:
         with open(info, "r")as f:
           tip = json.load(f)["tips"]
         await ctx.send(f"**Quick Tip** : {random.choice(tip)}")


    async def on_guild_channel_delete(self, channel):
      ch = channel.id 
      dict = {}
      list = []  
      with open(restricted,'r')as f:
        restrict = json.load(f)
      with open(channels, 'r')as f:
        chan = json.load(f)
      try:
        if ch in restrict[str(channel.guild.id)]:
          restrict[str(channel.guild.id)].remove(channel.id)
          if restrict[str(channel.guild.id)] == list:
            restrict.pop(str(channel.guild.id))
        if ch == chan[str(channel.guild.id)]["over"]:
          chan[str(channel.guild.id)].pop("over")
        if ch == chan[str(channel.guild.id)]["nether"]:
            chan[str(channel.guild.id)].pop("nether")
        if ch == chan[str(channel.guild.id)]["end"]:
          chan[str(channel.guild.id)].pop("end")
        if chan[str(channel.guild.id)] == dict:
          chan.pop(str(channel.guild.id))
      except KeyError:
        pass
      with open(channels,'w')as f:
        json.dump(chan, f, indent=4)
      with open(restricted,'w')as f:
        json.dump(restrict, f, indent=4)
