import discord
from discord.ext import commands, tasks
from cogs.functions.function import Func
from cogs.functions.events import Events
from cogs.functions.game_functions import GameFunction
import os
import time
import json
import asyncio
from dislash import InteractionClient
from itertools import cycle
from PIL import Image
from io import BytesIO

from keep_alive import keep_alive
intents = discord.Intents(messages = True, guilds = True, dm_messages = True, members = True, presences = True, dm_reactions = True, reactions = True, emojis = True ) 
client = commands.Bot(command_prefix=['m! ','m!'],case_insensetive=True,  help_command=None, intents = intents )
slash = InteractionClient(client) 
pfp = cycle([ "pick.png","grass.png", "discomine.jpg"])
profiles = "cogs/functions/main_resources/profiles.json" 

events = Func(client)
event = Events(client)
game = GameFunction()

#------On Ready------#
@client.event
async def on_ready():
  print("We are ready to go!")
  await client.change_presence(activity= discord.Game("Minecraft"))
  loop_health.start(client)

@tasks.loop(seconds=20)
async def change_pfp():
  print("Pfp changed")
  source = next(pfp)
  print(source, type(source))
  with open(source, "rb")as image:
    data = BytesIO(image.read())
    image = Image.open(data)
    await client.user.edit(avatar=image)

@tasks.loop(seconds= 100)
async def loop_health(client):
  with open(profiles, "r") as f:
    profile = json.load(f)
  for id in profile:
    if profile[id]["food"] == 100:
      if profile[id]["health"] != profile[id]["max_health"]:
        profile[id]["health"] += 2
    elif profile[id]["food"] == 0:
      profile[id]["health"] -= 2
      if profile[id]["health"] == 0:
        await game.kill()
      elif profile[id]["health"] < 30:
        try:
          user=client.get_user(int(id))
          await user.send(f"{user.mention} your health is very low\nTry eating something.")
        except Exception as e:
          print(e)
  with open(profiles, "w") as f:
    json.dump(profile, f, indent=4)
    
#-------Events-------#
client.event(event.on_message)
client.event(event.on_guild_leave)
client.event(event.on_command_error)
client.event(event.on_command_completion)
client.event(event.on_guild_channel_delete)
client.event(event.on_guild_join)

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
            print(f"{file}.json :\n ", e)
            print("\nAborting Mission....")
            exit()
    print("\n • All files working properly \n")
    keep_alive()
 
    client.run(os.environ['TOKEN'])
      
