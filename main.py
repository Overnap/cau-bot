# Let us process asynchronously
import asyncio
# Import discord API
import discord
from discord.ext.commands import Bot
# For convenient time handling
from datetime import datetime
from pytz import timezone
# For serializing config
import json
# Import custom crawling module
import crawl

with open("config.json") as file:
    config = json.load(file)

is_running = False
bot = Bot(command_prefix=config["PREFIX"])

channels = []
channels_option = {}
undergraduate_data = []
college_data = []
abeek_review_data = []
abeek_notice_data = []
me_notice_data = []
me_employment_data = []


async def undergraduate_alert():
    crawled = await crawl.undergraduate_crawl()
    for post in crawled:
        exist = any(x == post for x in undergraduate_data)
        if not exist:
            print("[Main] New Post :", post.title)
            embed = discord.Embed(title=post.title, description=post.link, color=0x568DF5)
            embed.set_author(name="CAU 학사", url="https://www.cau.ac.kr/index.do",
                             icon_url="http://www.google.com/s2/favicons?domain=http://admission.cau.ac.kr/main.htm")
            for channel in channels:
                if channels_option[channel]["undergraduate"]:
                    await channel.send(embed=embed)
            undergraduate_data.append(post)
            # Delete old posts for memory management
            if len(undergraduate_data) > 20:
                undergraduate_data.pop(0)


async def college_alert():
    crawled = await crawl.college_crawl()
    for post in crawled:
        exist = any(x == post for x in college_data)
        if not exist:
            print("[Main] New Post :", post.title)
            embed = discord.Embed(title=post.title, description=post.link, color=0xEB422E)
            embed.set_author(name="공과대학",
                             url="http://coe.cau.ac.kr/main/main.php",
                             icon_url="http://www.google.com/s2/favicons?domain=http://admission.cau.ac.kr/main.htm")
            for channel in channels:
                if channels_option[channel]["college"]:
                    await channel.send(embed=embed)
            college_data.append(post)
            # Delete old posts for memory management
            if len(college_data) > 10:
                college_data.pop(0)


# FIXME: 보도/홍보 별 필요 없는거같은데
async def abeek_review_alert():
    crawled = await crawl.abeek_review_crawl()
    for post in crawled:
        exist = any(x == post for x in abeek_review_data)
        if not exist:
            print("[Main] New Post :", post.title)
            embed = discord.Embed(title=post.title, description=post.link, color=0xEB422E)
            embed.set_author(name="ABEEK 보도/홍보",
                             url="https://abeek.cau.ac.kr/notice/list2.jsp",
                             icon_url="http://www.google.com/s2/favicons?domain=http://admission.cau.ac.kr/main.htm")
            for channel in channels:
                if channels_option[channel]["abeek_review"]:
                    await channel.send(embed=embed)
            abeek_review_data.append(post)
            # Delete old posts for memory management
            if len(abeek_review_data) > 10:
                abeek_review_data.pop(0)


async def abeek_notice_alert():
    crawled = await crawl.abeek_notice_crawl()
    for post in crawled:
        exist = any(x == post for x in abeek_notice_data)
        if not exist:
            print("[Main] New Post :", post.title)
            embed = discord.Embed(title=post.title, description=post.link, color=0xE060A4)
            embed.set_author(name="ABEEK",
                             url="https://abeek.cau.ac.kr/notice/list.jsp",
                             icon_url="http://www.google.com/s2/favicons?domain=http://admission.cau.ac.kr/main.htm")
            for channel in channels:
                if channels_option[channel]["abeek_notice"]:
                    await channel.send(embed=embed)
            abeek_notice_data.append(post)
            # Delete old posts for memory management
            if len(abeek_notice_data) > 10:
                abeek_notice_data.pop(0)


async def me_notice_alert():
    crawled = await crawl.me_notice_crawl()
    for post in crawled:
        exist = any(x == post for x in me_notice_data)
        if not exist:
            print("[Main] New Post :", post.title)
            embed = discord.Embed(title=post.title, description=post.link, color=0xF5D356)
            embed.set_author(name="기계공학과",
                             url="http://me.cau.ac.kr/bbs/board.php?bo_table=sub5_1",
                             icon_url="http://www.google.com/s2/favicons?domain=http://admission.cau.ac.kr/main.htm")
            for channel in channels:
                if channels_option[channel]["me_notice"]:
                    await channel.send(embed=embed)
            me_notice_data.append(post)
            # Delete old posts for memory management
            if len(me_notice_data) > 10:
                me_notice_data.pop(0)


async def me_employment_alert():
    crawled = await crawl.me_employment_crawl()
    for post in crawled:
        exist = any(x == post for x in me_employment_data)
        if not exist:
            print("[Main] New Post :", post.title)
            embed = discord.Embed(title=post.title, description=post.link, color=0x59DE6D)
            embed.set_author(name="기계공학과 취업",
                             url="http://me.cau.ac.kr/bbs/board.php?bo_table=sub5_3",
                             icon_url="http://www.google.com/s2/favicons?domain=http://admission.cau.ac.kr/main.htm")
            for channel in channels:
                if channels_option[channel]["me_employment"]:
                    await channel.send(embed=embed)
            me_employment_data.append(post)
            # Delete old posts for memory management
            if len(me_employment_data) > 10:
                me_employment_data.pop(0)


async def main_coroutine():
    # System main coroutine

    # To prevent multiple execution
    global is_running
    is_running = True

    # Crawl and alarm
    while True:
        t = datetime.now(timezone("Asia/Seoul"))
        # Record start time
        print("[Main] Coroutine started : " + t.strftime("%Y/%m/%d %H:%M:%S"))

        # For debugging, only work with more than one user
        if len(channels) != 0:
            futures = [asyncio.ensure_future(me_notice_alert()), asyncio.ensure_future(me_employment_alert()),
                       asyncio.ensure_future(abeek_notice_alert()), asyncio.ensure_future(college_alert()),
                       asyncio.ensure_future(undergraduate_alert())]
            await asyncio.gather(*futures)
            # TODO: me 사이트에 동시다발적으로 접속하면 막히는 듯 한꺼번에 처리하던가 html을 메모하던가 해서 해결하자

        # Record completion time
        print("[Main] Coroutine completed : " + datetime.now(timezone("Asia/Seoul")).strftime("%Y/%m/%d %H:%M:%S"))
        # Repeat with delay
        await asyncio.sleep(config["DELAY"])


@bot.event
async def on_ready():
    print("[BOT] The bot is ready!")

    # Run only once
    global is_running
    if not is_running:
        await main_coroutine()


bot.remove_command('help')


@bot.command()
async def help(ctx):
    await ctx.send("`!start`, `!stop` - Start and stop the notification.\n"
                   "`!undergraduate`, `!college`, `!abeek`, `!me`, `!employment` - Turn on and off specific alarms.\n"
                   "`!도움말` - Korean help.")


@bot.command()
async def 도움말(ctx):
    await ctx.send("`!시작`, `!종료` - 알람을 시작하고 종료합니다.\n"
                   "`!학사`, `!단과대`, `!아빅`, `!기계공`, `!취업` - 특정 알람을 끕니다.")


@bot.command()
async def start(ctx):
    if ctx.channel not in channels:
        channels.append(ctx.channel)
        print("[BOT] The alert started :", ctx.channel)
        if ctx.channel not in channels_option:
            channels_option[ctx.channel] = {"undergraduate": True,
                                            "abeek_review": False,
                                            "abeek_notice": True,
                                            "me_notice": True,
                                            "me_employment": True,
                                            "college": True}
            print("[BOT] The new channel has been initialized : ", ctx.channel)
        await ctx.send("알리미가 시작되었습니다.")
    else:
        await ctx.send("이미 알리미가 실행 중입니다.")


@bot.command()
async def stop(ctx):
    if ctx.channel in channels:
        channels.remove(ctx.channel)
        print("[BOT] The alert stopped :", ctx.channel)
        await ctx.send("알리미가 정지되었습니다.")
    else:
        await ctx.send("알리미가 실행 중이지 않습니다.")


@bot.command()
async def undergraduate(ctx):
    if ctx.channel in channels:
        if channels_option[ctx.channel]["undergraduate"]:
            channels_option[ctx.channel]["undergraduate"] = False
            await ctx.send("학사 알림을 껐습니다.")
        else:
            channels_option[ctx.channel]["undergraduate"] = True
            await ctx.send("학사 알림을 켰습니다.")
    else:
        await ctx.send("먼저 알리미를 실행해야 합니다.")


@bot.command()
async def college(ctx):
    if ctx.channel in channels:
        if channels_option[ctx.channel]["college"]:
            channels_option[ctx.channel]["college"] = False
            await ctx.send("단과대 알림을 껐습니다.")
        else:
            channels_option[ctx.channel]["college"] = True
            await ctx.send("단과대 알림을 켰습니다.")
    else:
        await ctx.send("먼저 알리미를 실행해야 합니다.")


@bot.command()
async def abeek(ctx):
    if ctx.channel in channels:
        if channels_option[ctx.channel]["abeek_notice"]:
            channels_option[ctx.channel]["abeek_notice"] = False
            await ctx.send("ABEEK 알림을 껐습니다.")
        else:
            channels_option[ctx.channel]["abeek_notice"] = True
            await ctx.send("ABEEK 알림을 켰습니다.")
    else:
        await ctx.send("먼저 알리미를 실행해야 합니다.")


@bot.command()
async def me(ctx):
    if ctx.channel in channels:
        if channels_option[ctx.channel]["me_notice"]:
            channels_option[ctx.channel]["me_notice"] = False
            await ctx.send("기계공학과 알림을 껐습니다.")
        else:
            channels_option[ctx.channel]["me_notice"] = True
            await ctx.send("기계공학과 알림을 켰습니다.")
    else:
        await ctx.send("먼저 알리미를 실행해야 합니다.")


@bot.command()
async def employment(ctx):
    if ctx.channel in channels:
        if channels_option[ctx.channel]["me_employment"]:
            channels_option[ctx.channel]["me_employment"] = False
            await ctx.send("기계공학과 취업 알림을 껐습니다.")
        else:
            channels_option[ctx.channel]["me_employment"] = True
            await ctx.send("기계공학과 취업 알림을 켰습니다.")
    else:
        await ctx.send("먼저 알리미를 실행해야 합니다.")


@bot.command()
async def 시작(ctx):
    await start(ctx)


@bot.command()
async def 종료(ctx):
    await stop(ctx)


@bot.command()
async def 학사(ctx):
    await undergraduate(ctx)


@bot.command()
async def 단과대(ctx):
    await college(ctx)


@bot.command()
async def 아빅(ctx):
    await abeek(ctx)


@bot.command()
async def 기계공(ctx):
    await me(ctx)


@bot.command()
async def 취업(ctx):
    await employment(ctx)


bot.run(config["TOKEN"])
