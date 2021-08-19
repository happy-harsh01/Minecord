import discord
from discord.ext import commands


class Blocks(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def blocks(self, ctx, blocks: None):
        if blocks is None:
            em = discord.Embed(title="Blocks", description="```Use the command block <block> to get details on each block.```")
            await ctx.send(embed=em)


def setup(client):
    client.add_cog(Blocks(client))
