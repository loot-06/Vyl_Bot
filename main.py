# ============== import module ============== #
# sleep time
import asyncio
# discord main module
import discord
# discord sub module
from discord.ext import commands
# get messages
from messages import give_msg
# for gambling
from random import randrange
# for use vyl_bot database
import mysql.connector
# ============== import module ============== #


# ==================== For Main Declaration ==================== #
# discord bot's TOEKN (for run bot)
TOKEN = "TOKEN"

# discord bot prefix(v!)
bot = commands.Bot(command_prefix="v!")


# ==================== For Main Declaration ==================== #


# ==================== DATABASE FORMAT ==================== #
class Mysql:
    def __int__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            port='3306',
            user='root',
            password='PASSWORD',
            db="vyl_bot"
        )

    def connect(self):
        self.db = self.conn.cursor()

    def close(self):
        self.db.close()


    def check_user_in_db(self, USER_ID):
        self.db = self.conn.cursor()
        try:
            check_Query = "SELECT * FROM member WHERE name=%s;"
            self.db.execute(check_Query, (USER_ID))
            getted = self.db.fetchall()
            if getted != None:
                print("SERVICE:USER CHECKED")
                return True
            elif getted == None:
                print("SERVISE:USER IS NOT IN DATABASE")
        finally:
            self.close()

    def make_user_in_db(self, USER_ID, rule="USER"):
        self.db = self.conn.cursor()
        try:
            make_Query = "INSERT INTO member(name, vyl, rule, logged_time) VALUES (%s, 1000, %s,now());"
            try:
                self.db.execute(make_Query, (USER_ID, rule))
            except Exception as E:
                print("SERVICE:USER CREATE FAIL")
                self.close()
                return E

        finally:
            self.close()

    def log_report(self, USER_ID, contents):
        self.connect()
        try:
            report_Query = "INSERT INTO report(writer, contents) VALUES(%s, %s);"
            try:
                self.db.execute(report_Query, (USER_ID, contents))
                print("SERVICE:REPORT LOG AT DATABASE")
            except Exception as E:
                print("SERVICE:LOG REPORT FAIL")
                self.close()
                return E

        finally:
            self.close()

    def update_vyl(self, USER_ID, plus_vyl=None):
        self.db = self.conn.cursor()
        if plus_vyl == None:
            raise KeyError
        try:
            get_vyl_Query = "SELECT vyl FROM member WHERE name=%s;"
            try:
                self.db.execute(get_vyl_Query, (USER_ID))
            except Exception as E:
                print("CHECK USER FAIL")
                self.close()
                return E
            getted_vyl = self.db.fetchone()
            update_vyl = getted_vyl + plus_vyl
            update_Query = "UPDATE member SET vyl=%s WHERE name=%s;"
            try:
                self.db.execute(update_Query,(update_vyl, USER_ID))
            except Exception as E:
                print("FAIL TO UPDATE USER 'vyl'")
                self.close()
                return E

        finally:
            self.close()
    # TODO : DO EXCEPTION
    def check_user(self, USER_ID, check_type="USER"):
        self.db = self.conn.cursor()
        try:
            if check_type == "REPORT":
                try:
                    self.db.execute("USE report;")
                    if USER_ID != None:
                        check_report_Query ="SELECT * FROM report WHERE writer=%s;"
                finally:
                    self.db.execute(check_report_Query, (USER_ID))
                    give_content = self.db.fetchall()
                    return give_content
            else:
                try:
                    if USER_ID != None:
                        check_member_Query = "SELECT * FROM member WHERE writer=%s;"
                finally:
                    self.db.execute(check_member_Query, (USER_ID))
                    give_content = self.db.fetchall()
                    return give_content
        finally:
            self.close()
# ==================== DATABASE FORMAT ==================== #


# ==================== MAIN CODE ==================== #
# Use database class
db = Mysql()
# start code
@bot.event
async def on_start():
    # To check bot is start
    print("Discord bot on start")
    # Set bot's game
    game = discord.Game("v!명령어 , v!도움 | For Gamers")
    # apply game
    await bot.change_presence(status=discord.Status.online, activity=game)

# help code
@bot.command("도움", aliases=('명령어',))
async def help_msg(ctx, content="help"):
    # make embed
    embed = discord.Embed(
        title="> 도움말",
        description=give_msg(content),  # get msg from messages.py
        colour=0x4262F4
    )
    # use embed
    await ctx.send(embed=embed)
 
@bot.command(name="신고")
async def report(ctx, *, content=None):
    # delect message to protect report info
    await ctx.channel.purge(limit=1)
    # Preparation for error occurrence
    if content == None:
        await ctx.send("신고할 내용이 입력되지 않았습니다")
    else:
        # log to database
        return_data = db.log_report(ctx.author.id, content)
        # check database
        if return_data != True:
            await ctx.send(f"에러발생\n한번더 시도해보시고 그래도 안되면 관리자'𝓁𝑜𝑜𝓉#0204'에게 문의주세요\n{return_data}")
        # check database
        elif return_data:
            user = await bot.fetch_user(ctx.author.id)
            await user.send("신고가 접수되었습니다")

# ==================== MAIN CODE ==================== #


# entry point
if __name__ == '__main__':
    # run discord bot
    bot.run(TOKEN)
