import discord
import os , json , random
from discord.ext import commands
from functions.function import Events

bot = commands.Bot(command_prefix='m!', case_insensitive=True)
bot.remove_command('help')

# Files needed -
# main.py
# greet.json
# profile.json
# channels.json

events = Events(bot)
bot.event(events.on_command_error)
bot.event(events.on_guild_leave)

@bot.event
async def on_ready():
    print("We are ready to Go!")

async def on_message(message):
    if bot.user.mentioned_in(message):
        with open(".\main_resources\greet.json","r") as f:
            greet = json.load(f)
        await message.channel.send(random.choice(greet["response"]))
    await bot.process_commands(message)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

if __name__ == '__main__':
    bot.run('TOKEN')
