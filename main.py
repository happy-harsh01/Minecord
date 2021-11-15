import discord
from discord.ext import commands
from cogs.functions.function import Func
from cogs.functions.events import Events
import os
import time
import json
import asyncio
from dislash import InteractionClient

from keep_alive import keep_alive
intents = discord.Intents(messages = True, guilds = True, dm_messages = True, members = True, presences = True, dm_reactions = True, reactions = True, emojis = True ) 
client = commands.Bot(command_prefix=['m! ','m!'],case_insensetive=True,  help_command=None, intents = intents )
slash = InteractionClient(client) 

events = Func(client)
event = Events(client)

#------On Ready------#
@client.event
async def on_ready():
  print("We are ready to go!")
  await client.change_presence(activity= discord.Game("Minecraft"))    


#-------Events-------#
client.event(event.on_message)
client.event(event.on_guild_leave)
client.event(event.on_command_error)
client.event(event.on_command_completion)
client.event(event.on_guild_channel_delete)

#------Running------#
if __name__ == '__main__':
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"): 
            client.load_extension(f"cogs.{filename[:-3]}")
            print(f" • Loaded Cog : {filename}", end = "\r")
            time.sleep(.5)  
    files = ["info", "help", "profiles", "channels", "restricted_channels"]
    json_file = ""
    for file in files:        
      with open(f"cogs/functions/main_resources/{file}.json", "r") as f:
          try: 
            info = json.load(f)  
          except Exception as e:
            print(f"{file}.json : ", e)
            print("\nAborting Mission....")
            exit()
    print("\n • All files working properly \n")
    keep_alive()
 
    client.run(os.environ['TOKEN'])
      
