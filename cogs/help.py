import discord
from discord.ext import commands


# Help Command
class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        em = discord.Embed(title='Help Menu', colour=discord.color.red())
        em.add_field(name="Activity Commands",value="```eat, health, go, craft, mine, adventure, inventory, profile```")
        em.add_field(name="Over World Commands", value="```cave, fish, crop, enchant, trade, take, chest, build```")
        em.add_field(name="Nether Commands", value="``` ```")
        em.add_field(name="End Commands", value="``` ```")
        em.add_field(name="Game Settiings Commands", value="")
        em.add_field(name="Setup Commands", value="```")
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def start(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='start', value="start playing by creating a profile")
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command(aliases=['delete profile'])
    async def delete(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='delete profile', value='Delete your profile\n'
                                                  'This is very risky and will delete your all data and game progress')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def hunt(self, ctx):
        em = discord.Embed(title='Help Menu', colour=discord.color.red())
        em.add_field(name='hunt <time>', value='Go on hunting for some time.')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def chop(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='chop <time>', value='Chop some trees for a time.')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def crop(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='crop', value='Cuts grown crops and shows the seed again.')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def fish(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='fish', value='Catches some fish.')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def mine(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='mine <time>', value='Goes on mining for given time.')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def cave(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.colour.red())
        em.add_field(name='cave', value='Goes for mining ore in a cave. Expires when the cave is fully discovered.')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def go(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='go <location>', value='Goes to the specific location.\n'
                                                 'Use ```help go location`` for full list of locations')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command(aliases=['adv'])
    async def adventure(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.Red())
        em.add_field(name='adventure', value="Goes on an adventure to find different locations.\n"
                                             "It takes about one minute to adventure."
                                             "There's a 20% chance that you forget your way back.")
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def eat(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='eat', value='Eats food from inventory until health is full.')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def health(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='health', value='Shows your health.')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def use(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='use', value='Use an usable item from your inventory\n'
                                       'Use ```help use list``` command for full list of usable items')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def chest(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='chest <type>', value='Opens chest of specific type from home.\n'
                                                'Use ```help chest list``` command for full list of chest in home')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def craft(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='craft <item>', value='Craft an item by the help of Crafting table.\n'
                                                'Use ```help craft list``` for full list of craftable items.')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def build(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='build <monument>', value='Build a specific Monument.\n'
                                                    'Use ```help build list``` command for full list of '
                                                    'buildable monuments.')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def take(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='take <item>', value='Takes items from home chests to your inventory.')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command(aliases=['inv'])
    async def inventory(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='inventory', value='Shows your inventory')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command()
    async def profile(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='profile <user>', value='Shows your profile.\nIf a user is given shows his profile.\n'
                                                  'Note : <user> is optional argument.')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command(aliases=["go location", "location list"])
    async def location(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='locations', value='')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command(aliases=["build list"])
    async def monuments(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.Red())
        em.add_field(name='Buildable Items List', 
        value='''Level 1 House - Dirt House
Level 2 House - Wooden House
Level 3 House - Stone Mansion
Level 4 House - Modern Apartment
Level 5 House - Royal Castle
Farm Level 1 - Miniature Farm
Farm Level 2 - Small Farm
Farm Level 3 - Normal Farm
Farm Level 4 - Big Farm
Farm Level 5 - Giant Farm
Nether Portal''')

        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command(alias='craft list')
    async def craftable_items(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='Craftable Items Lis', value='')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command(aliases=["use list"])
    async def use_list(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='Useable Items List', value='')
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)

    @help.command(aliases=['change name'])
    async def name(self, ctx):
        em = discord.Embed(title='Help Command', colour=discord.color.red())
        em.add_field(name='change name <name>', value="Changes your character's name.")
        em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author}")
        await ctx.send(emebed=em)


def setup(client):
    client.add_cog(Help(client))

