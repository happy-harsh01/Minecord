import discord
from discord.ext import commands
import json
from .functions.game_functions import GameFunction
from .functions.function import Func
import asyncio
from dislash import ActionRow, Button, ButtonStyle

game = GameFunction()
func = Func()

profiles = "cogs//functions//main_resources//profiles.json"
channel = "cogs//functions//main_resources//channels.json"


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def hi(self, ctx):
        await ctx.send("Hello I am Minecord, Minecraft Discord Bot ,My prefix is ```m!```, start playing!")
     
    @commands.command()
    async def invite(self, ctx):
        row_of_buttons = ActionRow(
          Button(
            style = ButtonStyle.link,
            label = "Invite",
            url = discord.utils.oauth_url(self.client.user.id, permissions= discord.Permissions(414467873393))),
          Button(
            style = ButtonStyle.link,
            label = "Vote",
            url = "https://top.gg/bot/896308161831657492" 
          )
        )         
        embed = discord.Embed(title="Invite Minecord", description="Glad to hear that you are inviting us to your server.",colour=discord.Colour.light_grey())
        msg = await ctx.send(embed=embed, components = [row_of_buttons])
        
        def check(item):
          return item.author.id == ctx.user.id
        try:
          await ctx.wait_for_button_click(check, timeout = 120.0)
        except asyncio.TimeoutError :
          row_of_button = ActionRow(
          Button(
            style = ButtonStyle.grey,
            label = "Invite",
            custom_id = "id1",
            disabled = True ))
          await msg.edit(components = [row_of_button] )

    @commands.command()
    async def health(self, ctx):
        with open(profiles, 'r') as f:
          profile = json.load(f)
        health = profile[str(ctx.author.id)]["health"]
        max_health = profile[str(ctx.author.id)]["max_health"]
        heart = await game.hearts(ctx)
        foods = await game.food(ctx)
        food = profile[str(ctx.author.id)]["food"]
        await ctx.reply(embed = discord.Embed(title=f"{ctx.author.name}'s health", description= f"{health} {heart} {max_health}\n{food} {foods} 100", colour= discord.Colour.red()).set_footer(text= f"{ctx.author}", icon_url = ctx.author.avatar_url))
    
    @commands.command()
    async def profile(self, ctx, user: discord.Member = None):
        if user is None:
          user = ctx.author 
        with open(profiles,'r')as f:
          profile = json.load(f)
          try:
            profile = profile[str(user.id)]
          except KeyError:
            await ctx.send("No user found")
            return
        proceed_button = Button(style = ButtonStyle.blurple, label = "Builds ›", custom_id= "builds_fd")
        name = profile["name"]
        level = profile["level"]
        xp = profile["xp"]
        max_xp = (level+1)*100
        health = profile["health"]
        max_health = profile["max_health"]
        descrip = f"**Name** : {name}\n**Xp** :{xp}/{max_xp}\n**Health** : {health}/{max_health}\n**Armour** : "
        dict = {}
        list = []
        if profile["armour"] == dict:
          descrip += "No Armour"
        else:
          for key, value in profile["armour"]:
            descrip +=  f"  • {key} : {value}\n"
        url = user.avatar_url 
        em = discord.Embed(title= f"{user.name}'s Profile", description= descrip, colour = discord.Colour.blue())
        em.set_thumbnail(url = str(url))        
        em.set_footer(text= f"Profile Requested by {ctx.author}" , icon_url= url )
        msg = await ctx.send(embed=em, components = [ActionRow(proceed_button)])
        while True:
          try:
            def check(m):
              return m.author.id == ctx.author.id and m.message.id == msg.id    
            waiter = await ctx.wait_for_button_click(check, timeout = 60.0 )
            button = waiter.clicked_button.label

            #Processing Button Click
            if button == "‹ Profile":
              descrip = f"**Name** : {name}\n**Xp** :{xp}/{max_xp}\n**Health** : {health}/{max_health}\n**Armour** :"
              if profile["armour"] == dict:
                descrip += "No Armour"
              else:
                for key, value in profile["armour"]:
                  descrip +=  f"  • {key} : {value}\n"
              em.description = descrip 
              await msg.edit(embed = em, components = [ActionRow(proceed_button)]  )
            elif button == "Builds ›" or button == "‹ Builds":
              descrip = "•Builds" 
              if profile["builds"] == list:
                descrip +="\nYou have build nothing"
              else:
                for build in profile["builds"]:
                  descrip += f"\n › {build}"
              em.description = descrip 
              await msg.edit(embed = em, components = [ActionRow(Button( style= ButtonStyle.blurple, label= "‹ Profile", custom_id= "profile_bk" ), Button( style= ButtonStyle.blurple, label= "Adventure ›", custom_id= "adventure_fd" ))])
            elif  button == "Adventure ›" or button == "‹ Adventure":
              descrip = "•Adventuress" 
              if profile["places"] == list:
                descrip +="\nYou have adventured nothing"
              else:
                for place in profile["places"]:
                  descrip += f"\n › {place}"
              em.description = descrip 
              await msg.edit(embed = em, components = [ActionRow(Button(style = ButtonStyle.blurple, label = "‹ Builds", custom_id= "builds_bk" ), Button(style = ButtonStyle.blurple, label = "Advancements ›", custom_id= "advancement_fd" ))]  )
            elif button == "Advancements ›" or button == "‹ Advancements":
              descrip = "•Advancements" 
              if profile["adv"] == list:
                descrip +="\nYou have got no advancements"              
              else:
                for advancement in profile["adv"]:
                  descrip += f"\n › {advancement}"
              em.description = descrip 
              await msg.edit(embed = em, components = [ActionRow(Button(style = ButtonStyle.blurple, label = "‹ Adventure", custom_id= "adventure_bk" ), Button(style = ButtonStyle.blurple, label = "Log ›", custom_id= "log" ))]  )
            elif button == "Log ›":
              descrip = "•Logs" 
              if profile["log"] == dict:
                descrip +="\nNo record"
              else:
                for log, times in profile["log"].items():
                  descrip += f"\n › {log} : {times}"
              em.description = descrip 
              await msg.edit(embed = em, components = [ActionRow(Button(style = ButtonStyle.blurple, label = "‹ Advancements", custom_id= "advancements_bk" ))])
          except asyncio.TimeoutError :
            await msg.edit(embed=em)
            return


    @commands.command(alias="xp" )
    async def level(self, ctx):
      level = await game.level(ctx)
      with open(profiles, 'r')as f:
        profile = json.load(f)
      xp = profile[str(ctx.author.id)]["xp"]
      await ctx.reply(embed = discord.Embed(title= f"{ctx.author.name}'s level", description = f"Level : {level}\n Xp : {xp} / {(level+1)*100}",colour = discord.Colour.blurple()  ))

    @commands.command()
    async def bug(self, ctx,*,bug):
      agent = self.client.get_user(894072003533877279)
      if agent == None:
        await ctx.reply("ERROR")
        return
      await agent.send(f"{ctx.author} says :- \n {bug}")

    @commands.command()
    async def vote(self, ctx):
      em = discord.Embed(title = "Vote Minecord", description =  "Thanks for voting Minecord at top.gg\nVote daily and get a bonus chest.", color = discord.Color.green()) 
      await ctx.send(embed= em, components = [ ActionRow(
        Button(style = ButtonStyle.link, label = "Vote", url = "https://top.gg/bot/896308161831657492" )
      )])

    @commands.command(alias="dev")
    async def developer(self,ctx):
      em = discord.Embed(title = "Mr.Harsh", description = "Hi, I make Bots like this, Vote and show support.\nID : Mr.Harsh#3188", colour = discord.Colour.dark_blue())
      em.set_thumbnail(url= (self.client.get_user(894072003533877279).avatar_url))
      invite = Button( label= "Invite", style=ButtonStyle.link, url = discord.utils.oauth_url(self.client.user.id))
      github = Button( label= "Mr-Harsh-Codes", style=ButtonStyle.link, url = "https://github.com/mr-harsh-codes" )
      await ctx.send(embed=em, components = [ActionRow(invite, github)])
  
def setup(client):
    client.add_cog(Misc(client))  
