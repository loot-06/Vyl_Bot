import discord
from discord.ext import commands
from VB_project.messages import give_msg
TOKEN = "SECRET TOKEN "

app = commands.Bot(command_prefix="v!")


@app.event  # start code
async def on_ready():
    print("startup!")
    game = discord.Game("v!명령어 , v!도움 | For Gamers") # v!명령어 , v!도움 | For Gamers
    await app.change_presence(status=discord.Status.online, activity=game)


app.remove_command("help")
@app.command(name="명령어", alisases=("help","도움"))
async def help(ctx, contents="help"):


    embed = discord.Embed(
        title="도움말",
        description=give_msg(contents),
        colour=0x4262F4
    )

    await ctx.send(embed=embed)

if __name__ == "__main__":
    app.run(TOKEN)
