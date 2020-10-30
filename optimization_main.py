import discord
from discord.ext import commands
from messages import give_msg
from random import randrange
TOKEN = "SECRET TOKEN"

app = commands.Bot(command_prefix="v!")


@app.event  # start code
async def on_ready():
    print("startup!")
    game = discord.Game("v!명령어 , v!도움 | For Gamers") # v!명령어 , v!도움 | For Gamers
    await app.change_presence(status=discord.Status.online, activity=game)


app.remove_command("help")
@app.command(name="명령어")
async def help(ctx, contents="help"):

    embed = discord.Embed(
        title="도움말",
        description=give_msg(contents),
        colour=0x4262F4
    )

    await ctx.send(embed=embed)


@app.command(name="배팅")
async def gambling_bet(ctx, money=1000):
    await ctx.send("돈 넣고 돈먹기를 시작합니다")
    persent = randrange(0, 1001)
    if persent <= 300 and persent >= 0:
        money = 0
    elif persent <= 500 and persent >= 310:
        money *= 1
    elif persent <= 700 and persent >= 510:
        money *= 2
    elif persent <= 900 and persent >= 710:
        money *= 3
    elif persent <= 950 and persent >= 910:
        money *= 4
    elif persent <= 975 and persent >= 951:
        money *= 5
    elif persent <= 990 and persent >= 976:
        money *= 10
    elif persent <= 1000 and persent >= 991:
        money *= 100
    else:
        await ctx.send("ERROR OCCUR")
    print(type(money))
    await ctx.send("[BETA] money : {}".format(money))

@app.command(name="del")
async def delete_msg(ctx, limit=1):
    await ctx.channel.purge(limit=limit)

if __name__ == "__main__":
    app.run(TOKEN)
