import discord
from discord.ext import commands
from .functions.function import Func
import json
func = Func()

# Help Command
class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx,*, cmd=None):
        with open ("main_resources//help.json", 'r') as f:
                help = json.load(f)
        if cmd is None:
            cmd = "Help" 
            fields_dict = {"Activity Commands": "```eat, health, go, craft, mine, adventure, inventory, profile```",
            "Over World Commands": "```cave, fish, crop, enchant, trade, take, chest, build```",
            "Game Settings Commands": "```start, delete, change_name```",
            "Setup Commands": "```quick_setup, auto_setup, add_restricted_chan, set_over_chan, set_nether_chan, set_end_chan```"}
            await func.send_embed(ctx, cmd+" Command",'',"green",fields=fields_dict, footer=True )
            return 
        else:    
            if not cmd in help:
                await ctx.send(f"No help command for {cmd} found.")
                return
            for help_cmd in list(help.keys()):
                if cmd.lower() in help_cmd:
                    fields_dict = {help_cmd: help[help_cmd]}
                    break                 
        await func.send_embed(ctx, cmd+" Command",'',"green",fields=fields_dict, footer=True)
      
def setup(client):
    client.add_cog(Help(client))
