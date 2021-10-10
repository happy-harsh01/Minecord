import discord
from discord.ext import commands
form .functions.function import Func
func = Func()

# Help Command
class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, cmd=None):
        if cmd is None:
            fields_dict = {"Activity Commands": "```eat, health, go, craft, mine, adventure, inventory, profile```",
            "Over World Commands": "```cave, fish, crop, enchant, trade, take, chest, build```",
            "Game Settings Commands": "```start, delete, change_name```",
            "Setup Commands": "```quick_setup, auto_setup, add_restricted_chan, set_over_chan, set_nether_chan, set_end_chan```"}
            func.send_embed(ctx, 'Help Menu',"",discord.Colour.red(),fields_dict,footer=True)
        else:
            with open ("cogs//functions//main_resources//help.json", 'r') as f:
                help = json.load(f)
            if not cmd in help:
                await ctx.send(f"No help command for {cmd} found.")
                return
            for help_cmd in list(help.keys()):
                if cmd in help_cmd:
                    search = {help_cmd: help[help_cmd]}
                    break
            func.send_embed(ctx, cmd+" Command",'',discord.Colour.red(),search, footer=True)
             with open ("cogs//functions//main_resources//help.json", 'w') as f:
                json.dump(help, f, indent=4)

def setup(client):
    client.add_cog(Help(client))
