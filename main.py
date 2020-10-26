import discord
from discord.ext import commands

TOKEN = "SETCER TOKEN"

app = commands.Bot(command_prefix="`")

@app.event # start code
async def startup():
  game = discord.Game("`도움")
  await app.change_presence(status=discord.Status.online, activity=game)
 
 
