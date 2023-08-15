import datetime


import traceback
import discord, sqlite3, os, random, asyncio, requests, json, time, re, sys
from func import *
from Setting import *
from discord_webhook import DiscordEmbed, DiscordWebhook
from discord_buttons_plugin import ButtonType
from discord_components import DiscordComponents, ComponentsBot, Select, SelectOption, Button, ButtonStyle, ActionRow

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

admin_id = 관리자
bakara_on = 0
hz_on = 0
hz_h = []
hz_z = []
bkr_p=[]
bkr_b=[]
bkr_p_p=[]
bkr_b_p=[]
bkr_d=[]
doing_bet = []
doing_bet2 = []
doing_bet3 = []
doing_bet4 = []
total = 0
ktotal = 0
mtotal = 0
충전중 = 0
t = 0
ti = 0
tim = 0
ttii = 0
r_t=0
bkr_total_p = 0
bkr_total_b = 0
hz_total_h = 0
hz_total_z = 0
coin_on = 1
dt_on = 0
dt_total_d = 0
dt_total_t = 0
km_on = 0
doing_bet5 = []
# 룰렛 ㅡㅡㅡㅡ
rl_on=0
doing_bet6 = []
bue = 8
event = 0


def get_kr_min():
    return datetime.datetime.now().strftime('%M')


def getinfo(id):
    url = f"https://discordapp.com/api/users/{id}"
    he = {
        "Authorization": f"Bot {봇토큰}"
    }
    res = requests.get(url, headers=he)
    r = res.json()
    return r

if not (os.path.isfile("./database/database.db ")):
    con = sqlite3.connect("./database/database.db")
    cur = con.cursor()
    cur.execute(
        "CREATE TABLE users (id INTEGER, money INTEGER, boggle_bet_pick TEXT, boggle_bet_money INTEGER, is_bet INTEGER, ban INTEGER, ladder_bet_pick TEXT, ladder_bet_money INTEGER, wllet_bet_pick TEXT, wllet_bet_money INTEGER, owrun_bet_pick TEXT, owrun_bet_money INTEGER, eos1_bet_pcik TEXT, eos1_bet_money INTEGER, pwball_bet_pick TEXT, pwball_bet_money INTEGER, eos5_bet_pcik TEXT, eos5_bet_money INTEGER, powerladder_bet_pick TEXT, powerladder_bet_money INTEGER, ad_bet_pick TEXT, ad_bet_money INTEGER, rotoball_bet_pick TEXT, rotoball_bet_money INTEGER, rotoladder_bet_pick TEXT, rotoladder_bet_money INTEGER, hz_bet_pick TEXT, hz_bet_money INTEGER, coin_bet_money INTEGER, perc INTEGER)")
    con.commit()
    con.close()

@client.event
async def on_ready():
    DiscordComponents(client)
    print(f"")
    print(f"─────────────────────────────────────────────────────")
    print(
        f"메인시스템을 실행 합니다.: {client.user}\n봇 초대 링크 : https://discord.com/oauth2/authorize?client_id={client.user.id}&permissions=8&scope=bot")
    print(f"─────────────────────────────────────────────────────")
    print(f"사용 중인 서버 : {len(client.guilds)}개 관리 중")
    print(f"")

    while True:
        await client.change_presence(activity=discord.Game(f"코린랜드 운영"), status=discord.Status.online)
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Game(f"코린랜드 관리"), status=discord.Status.online)
        await asyncio.sleep(5)


@client.event
async def on_message(message):
    global ktotal
    global total
    global mtotal
    global bakara_on
    global hz_on
    global dt_on
    global hz_h
    global hz_z
    global bkr_p
    global bkr_b
    global bkr_p_p
    global bkr_b_p
    global bkr_d
    global doing_bet
    global doing_bet2
    global p
    global b
    global p_add_card
    global b_add_card
    global player_card
    global banker_card
    global player_card2
    global banker_card2
    global bkr_round
    global t
    global ti
    global tim
    global hz_round
    global bkr_total_p
    global bkr_total_b
    global hz_total_h
    global hz_total_z
    global doing_bet3
    global coin_on
    global doing_bet4
    global d_card
    global t_card
    global dt_total_d
    global dt_total_t
    global dt_round
    # 경마
    global km_round
    global ttii
    global doing_bet5
    global km_on
    global h1_op_on
    global h2_op_on
    global h3_op_on
    global h4_op_on
    global h1_go
    global h2_go
    global h3_go
    global h4_go
    # 룰렛
    global rl_round
    global r_t
    global doing_bet6
    global rl_on
    global number1
    global color
    global bue

    def talmoembed(embedtitle, description):
        return discord.Embed(title=embedtitle, description=description, color=0x2f3136)

    if message.author.bot:
        return

    con = sqlite3.connect("./database/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
    user_info = cur.fetchone()
    

    if (user_info == None):
        cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
            message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None))
        con.commit()
        con.close()
    else:
        cur.execute("SELECT * FROM users WHERE id == ?;", (client.user.id,))
        client_info = cur.fetchone()
        if (int(user_info[1]) >= int(client_info[-1])):
            if not (user_info[5] == 3):
                cur.execute("UPDATE users SET ban = ? WHERE id == ?;", (3, message.author.id))
                await message.author.send(f"<@{message.author.id}> 졸업 되셨습니다.", embed=talmoembed("배팅실패", f"잔액이 {client_info[-1]}원이상이 되셔셔 자동 졸업되셨습니다."))
                con.commit()
                con.close()
            #con.commit()
            #con.close()
            #con.commit()
            else:
                con.commit()
                con.close()
        else:
            con.commit()
            con.close()
        
        #con.commit()
        #con.close()
    if message.content.startswith(".몰수 "):
        if message.author.id in admin_id:
            user = message.mentions[0].id
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user,))
            user_info = cur.fetchone()
            if user_info[1]==None:
                await message.reply(embed=talmoembed("몰수 실패", "그 유저는 가입하지 않은 유저입니다."))
                con.close()
            elif user_info[1]==0:
                await message.reply(embed=talmoembed("몰수 실패", "0원을 가진 유저는 몰수가 불가능합니다!"))
                con.close()
            else:
                await message.reply(embed=talmoembed("몰수 완료", f"{user_info[1]}원을 몰수했습니다!"))
                cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                            (0, user))
                con.commit()
                con.close()
        else:
            await message.reply(embed=talmoembed("권한없음", "관리자만 사용가능한 명령어입니다."))

    if message.content.startswith("!내역"):
        if message.author.id in admin_id:
            try:
                user = message.mentions[0].id
                await message.reply(file=discord.File(f"./bet_log/{user}.txt"))
                os.remove(f"./bet_log/{user}.txt")
            except:
                await message.reply(embed=talmoembed("내역없음", "해당 유저는 아직 내역이 기록되있지않습니다."))
        else:
            await message.reply(embed=talmoembed("권한없음", "관리자만 사용가능한 명령어입니다."))

    if message.content.startswith('!계좌변경 '):
        if message.author.id in admin_id:
            setss=message.content.split(" ")[1]
            if message.content.split(" ")[1] == "국민" or message.content.split(" ")[1] == "토스" or message.content.split(" ")[1] == "카뱅" or message.content.split(" ")[1] == "신한":
                if message.content.split(" ")[1] == "국민":
                    banks="KB국민은행 252525-02-559744 정호린"
                    bankmsg="국민"
                    con = sqlite3.connect("./database/database.db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (1030050736110850129,))
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                (0, 1030050736110850129))
                    con.commit()
                    con.close()
                elif message.content.split(" ")[1] == "카뱅":
                    banks="카카오뱅크 7777-02-5651566 정호린"
                    bankmsg="카뱅"
                    con = sqlite3.connect("./database/database.db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (1030050736110850129,))
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                (1, 1030050736110850129))
                    con.commit()
                    con.close()
                elif message.content.split(" ")[1] == "신한":
                    banks="신한 110-53914-7644 신영민"
                    bankmsg="신한"
                    con = sqlite3.connect("./database/database.db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (1030050736110850129,))
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                (3, 1030050736110850129))
                    con.commit()
                    con.close()
                else:
                    banks="토스뱅크 1908-8522-0679 정호린"
                    bankmsg="토스"
                    con = sqlite3.connect("./database/database.db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (1030050736110850129,))
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                (2, 1030050736110850129))
                    con.commit()
                    con.close()
                await message.reply(f"> **계좌번호가 **{bankmsg}**||`{banks}`|| 으로 변경되었습니다.**")

        else:
            await message.reply(embed=talmoembed("권한없음", "관리자만 사용가능한 명령어입니다."))

    if message.content.startswith("!수수료"):
        if message.author.id in admin_id:
            amount = int(message.content.split(" ")[1])
            await message.reply(embed=talmoembed("수수료 계산완료",f"{amount}에서 10% 수수료 뺀 가격은 {round(amount*0.9)} 입니다."))
        else:
            await message.reply(embed=talmoembed("권한없음", "관리자만 사용가능한 명령어입니다."))
    if message.content.startswith("!조회"):
        if message.author.guild_permissions.administrator:
            user = message.mentions[0].id
            name = message.mentions[0].name
            log = ""

            id = 입출금로그
            channel = client.get_channel(int(id))
            await message.reply("잠시 기다려주세요...")
            async for messaged in channel.history(limit=None):
                if messaged.content != None:
                    if f"{str(user)}" in messaged.content:
                        log += f"{messaged.content}\n"
            list_1 = log.split("\n")
            list_a = []
            list_b = []
            for i in list_1:
                if "충전" in i:
                    list_a.append(i)
            for i in list_1:
                if "환전하" in i:
                    list_b.append(i)
            money = 0
            mm = 0
            for i in list_a:
                ii = i.split("원을")[0]
                numbers = ii.split("님이 ")[1]
                money += int(numbers)
            for i in list_b:
                ii = i.split("원을")[0]
                numbers = ii.split("님이 ")[1]
                mm += int(numbers)

            embed = discord.Embed(title=f"{name}님의 정보입니다.", description=f"{name}님의 충전액 : {money}\n{name}님의 환전액 : {mm}",
                                color=0x2f3136)
            await message.reply(embed=embed)


    if (message.content == '!충전'):
        await message.delete()
        if message.author.id in admin_id:
            charge_embed = discord.Embed(title="계좌/문상 충전", description="```yaml\n계좌/문상 충전 버튼 중 원하는 것을 눌러주세요```", color=0x2f3136)
            account = Button(label="계좌충전", custom_id="계좌충전", style=ButtonStyle.blue)
            #culture = Button(label="문상충전", custom_id="문상충전", style=ButtonStyle.red)
            await client.get_channel(충전채널).send(embed=charge_embed, components=
            ActionRow(
                [account],
            )
                                                )
                    
    if message.content == "!룰렛":
        if message.author.id in admin_id:
            rs_pe = client.get_channel(룰렛회차)
            # pe_rs = await rs_pe.send(f"`1회차`가 진행되고있습니다.")
            round_rs = ''
        #if rl_on == 0:
            await message.channel.send(f"<#{룰렛2채널}> 에 게임이 시작됩니다.")
            rl_on = 1
            rl_round = 0
            while True:
                rl_round += 1
                number1 = random.randint(0, 36)
                color = roulette_color(number1)
                rs_ch = 룰렛유출픽
                await client.get_channel(rs_ch).send(
                    f"{rl_round}회차\n빨강" if color == "red" else f"{rl_round}회차\n검정" if color == "black" else f"{rl_round}회차\n그린")
                r_t = 60
                rl_ch = client.get_channel(룰렛2채널)
                bet_embed = discord.Embed(title=f"{rl_round}회차 배팅가능시간입니다.",
                                        description=f"```ansi\n[0;41m빨강[0m , [0;40m검정[0m  , [1;32m초록[0m 에 배팅해주십시오.\n남은 배팅시간 : `{r_t}` ```", color=0x2f3136)
                bet_embed.set_footer(text=서버이름)
                bet_msg = await rl_ch.send(embed=bet_embed)
                for i in range(0, 12):
                    await asyncio.sleep(5)
                    r_t -= 5
                    bet_embed = discord.Embed(title=f"{rl_round}회차 배팅가능시간입니다.",
                                            description=f"```ansi\n[0;41m빨강[0m , [0;40m검정[0m  , [1;32m초록[0m 에 배팅해주십시오.\n남은 배팅시간 : `{r_t}` ```",
                                            color=0x2f3136)
                    bet_embed.set_footer(text=서버이름)
                    await bet_msg.delete()
                    bet_msg = await rl_ch.send(embed=bet_embed)
                if color == "red":
                    close_embed = discord.Embed(title=f"{rl_round}회차 배팅이 마감되었습니다", description=f'''
```
숫자

`{number1}`
```
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
🔴 빨강 : {number1} {"✅" if color == "red" else ""}   {"< 승리! > X1.95배" if color == "red" else ""}\n
                        ''', color=0xff0000)
                elif color == "black":
                    close_embed = discord.Embed(title=f"{rl_round}회차 배팅이 마감되었습니다", description=f'''
```
숫자

`{number1}`
```
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
⚫ 검정 : {number1}   {"✅" if color == "black" else ""}   {"< 승리! > X1.95배" if color == "black" else ""}\n
''', color=0x000000)
                else:
                    close_embed = discord.Embed(title=f"{rl_round}회차 배팅이 마감되었습니다", description=f'''
```
숫자

`{number1}`
```
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
🟢 그린 : {number1}   {"✅" if color == "green" else ""}   {"< 승리! > X8배" if color == "green" else ""}\n
                        ''', color=0x00ff00)

                close_embed.set_image(url=roulette_image(number1))
                await bet_msg.delete()
                bet_msg = await rl_ch.send(embed=close_embed, components="")
                bet_log = ""
                conn = sqlite3.connect('./database/database.db')
                c = conn.cursor()
                list_a = list(c.execute("SELECT * FROM users"))
                for i in list_a:
                    if (i[28] == None):
                        continue
                    conn = sqlite3.connect('./database/database.db')
                    c = conn.cursor()
                    if color == "red":
                        배당 = 1.95
                    elif color == "black":
                        배당 = 1.95
                    else:
                        배당 = 8

                    if i[28] == color:

                        bet_log += (f"**<@{i[0]}> {i[28]} {round(i[29] * 배당)} 적중**\n")
                        c.execute("UPDATE users SET money = money + ? where id=?", (round(i[29] * 배당), i[0],))
                        f = open(f"./bet_log/{i[0]}.txt", "a", encoding="utf-8-sig")
                        f.write(
                            f'''                
배팅게임 : 리틀룰렛
배팅회차 : {rl_round}
배팅내역 : {i[28]}
배팅금 : {i[29]}
적중 / 미적중 : 적중
적중 금액 : {round(i[29] * 배당-1)}
남은 금액 : {i[1] + round(i[29] * 배당)}
======================
''')
                        f.close()
                    else:

                        bet_log += (f"**<@{i[0]}> {i[28]} 미적중**\n")
                        f = open(f"./bet_log/{i[0]}.txt", "a", encoding="utf-8-sig")
                        f.write(
                            f'''                
배팅게임 : 리틀룰렛
배팅회차 : {rl_round}
배팅내역 : {i[28]}
배팅금 : {i[29]}
적중 / 미적중 : 미적중
남은 금액 : {i[1]}
======================
''')
                        f.close()

                    c.execute("UPDATE users SET rl_bet_pick = ? where id=?", (None, i[0],))
                    c.execute("UPDATE users SET rl_bet_money = ? where id=?", (None, i[0],))
                    conn.commit()
                    conn.close()
                if color == "red":
                    color = f"{color} 🔴"
                elif color == "black":
                    color = f"{color} ⚫"
                else:
                    color = f"{color} 🟢"
                round_rs = f"\n\n`{rl_round}회차` -- **{color.upper()}**"
                doing_bet6 = []
                ch = client.get_channel(룰렛배팅내역)
                await ch.send(f"`{rl_round}회차`\n\n{bet_log}")
                await rs_pe.send(f"{round_rs}")
    if message.content.startswith('.룰렛 '):
    #if rl_on != 0:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if not user_info[5] == 3:
            if message.content.split(" ")[2] == "올인":
                if (int(user_info[1]) >= 1000):
                    amount = int(user_info[1])
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                try:
                    amount = int(message.content.split(" ")[2])
                except:
                    con.close()
                    await message.channel.send(embed=talmoembed("배팅실패", "**```금액은 정수만 배팅이 가능합니다.```**"))
                    return
            if not amount < 1000:
                if user_info[1] >= amount:
                    choice = message.content.split(" ")[1]
                    if choice == "빨" or choice == "검" or choice == "초":
                        if not message.author.id in doing_bet6:
                            doing_bet6.append(message.author.id)
                            if user_info[1] >= 1000:

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                            (user_info[1] - int(amount), message.author.id))
                                if choice == "빨":
                                    choice="red"
                                elif choice == "검":
                                    choice = "black"
                                else:
                                    choice = "green"
                                cur.execute("UPDATE users SET rl_bet_pick = ? WHERE id == ?;",
                                            (choice, message.author.id))

                                cur.execute("UPDATE users SET rl_bet_money = ? WHERE id == ?;",
                                            (amount, message.author.id))
                                con.commit()
                                con.close()
                                await message.reply(
                                    embed=talmoembed("배팅성공", f"**> {rl_round}회차 {choice.upper()}에 배팅이 완료되었습니다.\n\n잔액 : {user_info[1] - amount}**"))

                            else:
                                con.close()
                                await message.channel.send(
                                    embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```이미 배팅중입니다.```**"))
                    else:
                        con.close()
                        await message.channel.send("**```빨/검/초 중에서만 배팅해주세요.```**")
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("배팅실패", "**```1000원이상부터 배팅이 가능합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))
    #else:
        #await message.channel.send(embed=talmoembed("배팅실패", "**```게임이 진행되고있지않습니다.```**"))
    if message.content.startswith('!룰렛레드 '):
        if message.channel.id == 룰렛채널:
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()
            if message.content.split(" ")[1] == "올인":
                if (int(user_info[1]) >= 1000):
                    amount = int(user_info[1])
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                amount = int(message.content.split(" ")[1])

            if (user_info == None):
                cur.execute(
                    "INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                        message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None,
                        None, None,
                        None, None, None, None, None, None, None, None, None, None, None, None))
                con.commit()
                con.close()

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                if (amount >= 1000):
                    if (amount <= user_info[1]):
                        if not (user_info[5] == 3):
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] - amount, message.author.id))
                            con.commit()
                            con.close()

                            number1 = random.randint(0, 36)
                            number2 = random.randint(0, 100)
                            color = roulette_color(number1)

                            if color == "red":
                                if number2 >= 53:
                                    bet_list = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]
                                    number1 = random.choice(bet_list)
                                    color = roulette_color(number1)
                                else:
                                    bet_list = [15, 4, 2, 17, 6, 13, 11, 8, 10, 25, 33, 20, 31, 22, 29, 28, 35, 26]
                                    number1 = random.choice(bet_list)
                                    color = roulette_color(number1)

                            if color == "red":
                                is_hit = "적중"
                                con = sqlite3.connect("./database/database.db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                user_info = cur.fetchone()

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                            (round(user_info[1] + (amount * 1.95)), message.author.id,))
                                con.commit()

                                con.close()
                                await message.reply(embed=talmoembed("배팅완료",
                                                                    f"**```py\n배팅완료\n번호 : {str(number1)}, 색깔 : {color.upper()}, {is_hit}\n\n잔액 : {round(user_info[1] + (amount * 1.95))}```**"))
                            else:
                                is_hit = "미적중"

                                con.close()
                                await message.reply(embed=talmoembed("배팅완료",
                                                                    f"**```py\n배팅완료\n번호 : {str(number1)}, 색깔 : {color.upper()}, {is_hit}\n\n잔액 : {user_info[1] - amount}```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```당신은 차단된 유저입니다.```**"))
                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("배팅실패", "**```1000원 이상부터 배팅이 가능합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("배팅실패", "**```가입되어 있지 않은 유저입니다.```**"))
        else:
            await message.reply(embed=talmoembed('베팅실패', f"<#{룰렛채널}> 채널에서만 배팅가능합니다."))


    if message.content.startswith('!그래프 '):
        if message.channel.id == 그래프채널:
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()
            if message.content.split(" ")[1] == "올인":
                if (int(user_info[1]) >= 1000):
                    amount = int(user_info[1])
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                amount = int(message.content.split(" ")[1])

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                if (amount >= 1000):
                    if (amount <= user_info[1]):
                        if not (user_info[5] == 3):
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] - amount, message.author.id))
                            con.commit()
                            con.close()
                            bae = 1
                            stop = Button(label="중단", custom_id="stop", style=ButtonStyle.red)
                            g_m = await message.reply(embed=talmoembed(f"배팅완료 {amount}원",
                                                                        f"**```py\n배팅완료\n현재 배수 : {bae}```**"), components=
                                ActionRow(
                                    [stop],
                                )
                                                            )
                            while True:
                                try:
                                    interaction = await client.wait_for("button_click",
                                                                        check=lambda inter: inter.custom_id != "",
                                                                        timeout=1)
                                except asyncio.exceptions.TimeoutError:
                                    pass
                                try:
                                    if message.author.id == interaction.user.id:
                                        print("버튼이 눌러졌어요!")
                                        break
                                except:
                                    pass

                                number1 = random.randint(0, 10)
                                print(number1)

                                if number1 <= bue:
                                    bae+=0.1
                                    bae=round(bae*10)
                                    bae=bae/10
                                    await g_m.edit(embed=talmoembed(f"배팅완료 {amount}원",
                                                                        f"**```py\n배팅완료\n현재 배수 : {bae}```**"))
                                else:
                                    bae=0
                                    await g_m.edit(embed=talmoembed(f"배팅완료 {amount}원",
                                                                    f"**```py\n배팅완료\n현재 배수 : {bae}```**"), components="")
                                    break
                            await g_m.edit(embed=talmoembed(f"그래프 종료",
                                                            f"**```py\n현재 배수 : {bae}, 승리금 : {round(amount * (bae-1))}```**"), components="")
                            f = open(f"./bet_log/{user_info[0]}.txt", "a", encoding="utf-8-sig")
                            f.write(
                                f'''                
배팅게임 : 그래프
배팅금 : {amount}
적중 금액 : {round(amount * (bae-1))}
남은 금액 : {round(user_info[1] + round(amount * (bae-1)))}
======================
''')
                            f.close()
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                            user_info = cur.fetchone()
                            con.commit()

                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (round(user_info[1] + round(amount * bae)), message.author.id,))
                            con.commit()

                            con.close()

                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```당신은 차단된 유저입니다.```**"))
                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("배팅실패", "**```1000원 이상부터 배팅이 가능합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("배팅실패", "**```가입되어 있지 않은 유저입니다.```**"))
        else:
            await message.reply(embed=talmoembed('배팅실패', f"<#{그래프채널}> 채널에서만 배팅가능합니다."))

    if message.content.startswith('!룰렛블랙 '):
        if message.channel.id == 룰렛채널:
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()
            if message.content.split(" ")[1] == "올인":
                if (int(user_info[1]) >= 1000):
                    amount = int(user_info[1])
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                amount = int(message.content.split(" ")[1])

            if (user_info == None):
                cur.execute(
                    "INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                        message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None,
                        None, None,
                        None, None, None, None, None, None, None, None, None, None, None, None))
                con.commit()
                con.close()

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                if (amount >= 1000):
                    if (amount <= user_info[1]):
                        if not (user_info[5] == 3):
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] - amount, message.author.id))
                            con.commit()
                            con.close()

                            number1 = random.randint(0, 36)
                            number2 = random.randint(0, 100)

                            color = roulette_color(number1)

                            if color == "black":
                                if number2 >= 53:
                                    bet_list = [15, 4, 2, 17, 6, 13, 11, 8, 10, 25, 33, 20, 31, 22, 29, 28, 35, 26]
                                    number1 = random.choice(bet_list)
                                    color = roulette_color(number1)
                                else:
                                    bet_list = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]
                                    number1 = random.choice(bet_list)
                                    color = roulette_color(number1)

                            if color == "black":
                                is_hit = "적중"
                                con = sqlite3.connect("./database/database.db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                user_info = cur.fetchone()

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                            (round(user_info[1] + (amount * 1.95)), message.author.id,))
                                con.commit()

                                con.close()
                                await message.reply(embed=talmoembed("배팅완료",
                                                                    f"**```py\n배팅완료\n번호 : {str(number1)}, 색깔 : {color.upper()}, {is_hit}\n\n잔액 : {round(user_info[1] + (amount * 1.95))}```**"))
                            else:
                                is_hit = "미적중"

                                con.close()
                                await message.reply(embed=talmoembed("배팅완료",
                                                                    f"**```py\n배팅완료\n번호 : {str(number1)}, 색깔 : {color.upper()}, {is_hit}\n\n잔액 : {user_info[1] - amount}```**"))

                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```당신은 차단된 유저입니다.```**"))
                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("배팅실패", "**```1000원 이상부터 배팅이 가능합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("배팅실패", "**```가입되어 있지 않은 유저입니다.```**"))
        else:
            await message.reply(embed=talmoembed('베팅실패', f"<#{룰렛채널}> 채널에서만 배팅가능합니다."))

    if message.content.startswith('!룰렛그린 '):
        if message.channel.id == 룰렛채널:
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()
            if message.content.split(" ")[1] == "올인":
                if (int(user_info[1]) >= 1000):
                    amount = int(user_info[1])
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                amount = int(message.content.split(" ")[1])

            if (user_info == None):
                cur.execute(
                    "INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                        message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None,
                        None, None,
                        None, None, None, None, None, None, None, None, None, None, None, None))
                con.commit()
                con.close()

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                if (amount >= 1000):
                    if (amount <= user_info[1]):
                        if not (user_info[5] == 3):
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] - amount, message.author.id))
                            con.commit()
                            con.close()

                            number1 = random.randint(0, 36)

                            color = roulette_color(number1)

                            if color == "green":
                                is_hit = "적중"
                                con = sqlite3.connect("./database/database.db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                user_info = cur.fetchone()

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                            (round(user_info[1] + (amount * 8)), message.author.id,))
                                con.commit()

                                con.close()
                                await message.reply(embed=talmoembed("배팅완료",
                                                                    f"**```py\n배팅완료\n번호 : {str(number1)}, 색깔 : {color.upper()}, {is_hit}\n\n잔액 : {round(user_info[1] + (amount * 8))}```**"))
                            else:
                                is_hit = "미적중"

                                con.close()
                                await message.reply(embed=talmoembed("배팅완료",
                                                                    f"**```py\n배팅완료\n번호 : {str(number1)}, 색깔 : {color.upper()}, {is_hit}\n\n잔액 : {user_info[1] - amount}```**"))

                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```당신은 차단된 유저입니다.```**"))
                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("배팅실패", "**```1000원 이상부터 배팅이 가능합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("배팅실패", "**```가입되어 있지 않은 유저입니다.```**"))
        else:
            await message.reply(embed=talmoembed('베팅실패', f"<#{룰렛채널}> 채널에서만 배팅가능합니다."))

    if (message.content == '3!코인'):
        if message.author.id in admin_id:
            coin_on = 1
            not_come = 0
            min = int(get_kr_min()) % 3
            await message.channel.send(f"<#{코인채널}> 에 게임이 시작됩니다.")
            coin_embed = discord.Embed(title="3분에 한번씩 값이 변동됩니다.",
                                    description=f"```yaml\n아래채널에서 명령어로 원하는 금액을 매수해주세요.```",
                                    color=0x2f3136)
            # coin = Button(label="코인매수", custom_id="코인투자", style=ButtonStyle.green)
            # recall = Button(label="매도", custom_id="돈빼기", style=ButtonStyle.gray)
            coin_embed.set_footer(text=f'{3 - int(min)}분 남았습니다.')
            coin_msg = await client.get_channel(코인채널).send(embed=coin_embed)
            while True:
                min = int(get_kr_min()) % 3
                text = ''
                if min == 0:
                    if not_come == 0:
                        not_come = 1
                        for i in doing_bet3:
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                            user_info = cur.fetchone()
                            user = client.get_user(i)
                            new_money = int(f'{round(user_info[-2] * ((user_info[-1] / 100) + 1))}')
                            if new_money <= 100:
                                new_money = 0
                                doing_bet3.remove(i)
                            text += f"{user}: {user_info[-2]}원 -> {new_money}원 {round(user_info[-2] * (user_info[-1] / 100))}원 {'🔺' if user_info[-2] * (user_info[-1] / 100) > 0 else '🔽'}\n"
                            f = open(f"./bet_log/{user_info[0]}.txt", "a", encoding="utf-8-sig")
                            f.write(
f'''                
배팅게임 : 리틀코인
적중 금액 : {new_money-user_info[-2]}
남은 금액 : 머니 : {user_info[1]} 매수금 : {int(new_money)}
======================
''')
                            f.close()
                            cur.execute("UPDATE users SET coin_bet_money = ? WHERE id == ?;",
                                        (new_money, i))
                            cur.execute("UPDATE users SET perc = ? WHERE id == ?;",
                                        (random.randint(-100, 100), i))
                            con.commit()
                            con.close()
                        if text == '':
                            coin_embed = discord.Embed(title="투자가 마감되었습니다.",
                                                    description=f"```yaml\n아무도 매수하지않았습니다.```",
                                                    color=0x2f3136)
                        else:
                            coin_embed = discord.Embed(title="투자가 마감되었습니다.",
                                                    description=f"```yaml\n{text}```",
                                                    color=0x2f3136)
                        await coin_msg.delete()
                        coin_msg = await client.get_channel(코인채널).send(embed=coin_embed)
                    else:
                        await asyncio.sleep(30)
                elif min != get_kr_min():
                    min = int(get_kr_min()) % 3
                    not_come = 0
                    coin_embed = discord.Embed(title="3분에 한번씩 값이 변동됩니다.",
                                            description=f"```yaml\n아래채널에서 명령어로 원하는 금액을 매수해주세요.```",
                                            color=0x2f3136)
                    coin_embed.set_footer(text=f'{3 - int(min)}분 남았습니다.')
                    await coin_msg.edit("", embed=coin_embed)

    if message.content.startswith('!코인'):

        amsg = await message.channel.send("잠시만 기다려주세요..")
        conn = sqlite3.connect("./database/database.db")
        c = conn.cursor()
        list_all = list(c.execute("SELECT * FROM users"))
        list_all.sort(key=lambda x: -x[1])
        print()
        res_text = "=======투자액=======\n\n"
        idx = 0
        for ii in list_all[0:15]:
            if ii[-2] != 0 and ii[-2] != None:
                idx += 1
                res_text += str(idx) + ". " + str(await client.fetch_user(ii[0])) + " - " + str(ii[-2]) + "원 투자중\n"

        conn.close()
        res_text = discord.Embed(title=f'유저 {idx}명의 투자내역입니다.',
                                description=f'{res_text}',
                                color=0x2f3136)
        await amsg.edit("", embed=res_text)

    if message.content.startswith('!순위'):
        if message.author.id in admin_id:
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()

            if (user_info == None):
                cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                    message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                    None,
                    None, None, None, None, None, None, None, None, None, None, None, None))
                con.commit()
                con.close()
            try:
                args = message.content.split(" ")[1]
            except:
                args = ""

            amsg = await message.channel.send("잠시만 기다려주세요..")
            if (len(args) == 2):
                int(args).pop(0)
                counts = int(args[0])
                conn = sqlite3.connect("./database/database.db")
                c = conn.cursor()
                list_all = list(c.execute("SELECT * FROM users"))
                list_all.sort(key=lambda x: -x[1])
                print()
                res_text = "=======순위=======\n\n"
                idx = 1
                for ii in list_all[0:counts]:
                    res_text += str(idx) + ". " + str(await client.fetch_user(ii[0])) + " - " + str(ii[1]) + "원 \n"
                    idx += 1
                conn.close()
                # await amsg.edit(res_text)
                res_text = discord.Embed(title=f'유저 {counts}명의 순위에요!',
                                        description=f'{res_text}',
                                        color=0x2f3136)
                await amsg.edit("", embed=res_text)


            else:
                conn = sqlite3.connect("./database/database.db")
                c = conn.cursor()
                list_all = list(c.execute("SELECT * FROM users"))
                list_all.sort(key=lambda x: -x[1])
                print()
                res_text = "=======순위=======\n\n"
                idx = 1
                for ii in list_all[0:10]:
                    res_text += str(idx) + ". " + str(await client.fetch_user(ii[0])) + " - " + str(ii[1]) + "원 \n"
                    idx += 1
                conn.close()
                res_text = discord.Embed(title='유저 10명의 순위에요!',
                                        description=f'{res_text}',
                                        color=0x2f3136)
                await amsg.edit("", embed=res_text)
        else:
            await message.reply(embed=talmoembed("권한없음", "관리자만 사용가능한 명령어입니다."))

    if message.content == "!홀짝":
        if message.author.id in admin_id:
            rs_pe = client.get_channel(홀짝회차)
            # pe_rs = await rs_pe.send(f"`1회차`가 진행되고있습니다.")
            round_rs = ''
            # leng = 0
            # bet_msg = await client.get_channel(홀짝채널).send(f"start")
            #if hz_on == 0:
            await message.channel.send(f"<#{홀짝채널}> 에 게임이 시작됩니다.")
            hz_on = 1
            hz_round = 0
            while True:
                text = ''
                hz_round += 1
                hz_h = []
                hz_z = []
                oplog = ''
                result = "홀" if random.randint(0, 1) == 1 else '짝'
                await client.get_channel(유출픽).send(f"> {hz_round}회차\n> `{result}`")
                t = 60
                hz_ch = client.get_channel(홀짝채널)
                bet_embed = discord.Embed(title=f"{hz_round}회차 배팅가능시간입니다.",
                                        description=f"홀 또는 짝에 배팅해주십시오.\n\n남은 배팅시간 : `{t}`", color=0x2f3136)
                bet_embed.set_footer(text=서버이름)

                bet_msg = await client.get_channel(홀짝채널).send(embed=bet_embed)
                for i in range(0, 12):
                    await asyncio.sleep(5)
                    t -= 5
                    bet_embed = discord.Embed(title=f"{hz_round}회차 배팅가능시간입니다.",
                                            description=f"홀 또는 짝에 배팅해주십시오.\n\n남은 배팅시간 : `{t}`",
                                            color=0x2f3136)
                    bet_embed.set_footer(text=서버이름)
                    await bet_msg.delete()
                    bet_msg = await client.get_channel(홀짝채널).send(embed=bet_embed)
                    if t == 0:
                        break
                if result == "홀":
                    for i in hz_h:
                        
                        con = sqlite3.connect("./database/database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                        user_info = cur.fetchone()
                        user = client.get_user(i)
                        new_money = int(f'{(user_info[27] * 1.95):.0f}')
                        text += f"{user}: 홀에 {user_info[27]}원 -> {new_money}원 (적중)\n"
                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                    (user_info[1] + new_money, i))
                        cur.execute("UPDATE users SET hz_bet_pick = ? where id=?", (None, i,))
                        cur.execute("UPDATE users SET hz_bet_money = ? where id=?", (None, i,))
                        con.commit()
                        con.close()
                        f = open(f"./bet_log/{i}.txt", "a", encoding="utf-8-sig")
                        f.write(
                            f'''                
배팅게임 : 홀짝
배팅회차 : {hz_round}
배팅내역 : 홀
배팅금 : {user_info[27]}
적중 / 미적중 : 적중
적중 금액 : {round(user_info[27] * 0.95)}
남은 금액 : {user_info[1] + user_info[27] * 1.95}
======================
    ''')
                        f.close()
                    for i in hz_z:
                        
                        con = sqlite3.connect("./database/database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                        user_info = cur.fetchone()
                        user = client.get_user(i)
                        new_money = 0
                        text += f"{user}: 짝에 {user_info[27]}원 -> {new_money}원 (미적중)\n"
                        cur.execute("UPDATE users SET hz_bet_pick = ? where id=?", (None, i,))
                        cur.execute("UPDATE users SET hz_bet_money = ? where id=?", (None, i,))
                        con.commit()
                        con.close()
                        f = open(f"./bet_log/{i}.txt", "a", encoding="utf-8-sig")
                        f.write(
                            f'''                
배팅게임 : 홀짝
배팅회차 : {hz_round}
배팅내역 : 짝
배팅금 : {user_info[27]}
적중 / 미적중 : 미적중
남은 금액 : {user_info[1]}
======================
''')
                        f.close()
                else:
                    for i in hz_h:
                        con = sqlite3.connect("./database/database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                        user_info = cur.fetchone()
                        user = client.get_user(i)
                        new_money = 0
                        text += f"{user}: 홀에 {user_info[27]}원 -> {new_money}원 (미적중)\n"
                        cur.execute("UPDATE users SET hz_bet_pick = ? where id=?", (None, i,))
                        cur.execute("UPDATE users SET hz_bet_money = ? where id=?", (None, i,))
                        con.commit()
                        con.close()
                        f = open(f"./bet_log/{i}.txt", "a", encoding="utf-8-sig")
                        f.write(
                                f'''                
배팅게임 : 홀짝
배팅회차 : {hz_round}
배팅내역 : 홀
배팅금 : {user_info[27]}
적중 / 미적중 : 미적중
남은 금액 : {user_info[1]}
======================
''')
                        f.close()
                    for i in hz_z:
                        con = sqlite3.connect("./database/database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                        user_info = cur.fetchone()
                        user = client.get_user(i)
                        new_money = int(f'{(user_info[27] * 1.95):.0f}')
                        text += f"{user}: 짝에 {user_info[27]}원 -> {new_money}원 (적중)\n"
                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                    (user_info[1] + new_money, i))
                        cur.execute("UPDATE users SET hz_bet_pick = ? where id=?", (None, i,))
                        cur.execute("UPDATE users SET hz_bet_money = ? where id=?", (None, i,))
                        con.commit()
                        con.close()
                        f = open(f"./bet_log/{i}.txt", "a", encoding="utf-8-sig")
                        f.write(
                            f'''                
배팅게임 : 홀짝
배팅회차 : {hz_round}
배팅내역 : 짝
배팅금 : {user_info[27]}
적중 / 미적중 : 적중
적중 금액 : {round(user_info[27] * 0.95)}
남은 금액 : {user_info[1] + user_info[27] * 1.95}
======================
''')
                        f.close()
                if text == '':
                    close_embed = discord.Embed(title=f"{hz_round}회차 배팅이 마감되었습니다",
                                                description=f"{hz_round}회차 결과 : `{result}`\n\n```아무도 참여하지 않았습니다.```",
                                                color=0x2f3136)
                    close_embed.set_footer(text='10초후 다음 회차가 시작됩니다.')
                else:
                    close_embed = discord.Embed(title=f"{hz_round}회차 배팅이 마감되었습니다",
                                                description=f"{hz_round}회차 결과 : `{result}`\n\n```{text}```",
                                                color=0x2f3136)
                    close_embed.set_footer(text='10초후 다음 회차가 시작됩니다.')
                await bet_msg.delete()
                bet_msg = await client.get_channel(홀짝채널).send(embed=close_embed, components="")
                await asyncio.sleep(10)
                doing_bet = []
                hz_total_h = 0
                hz_total_z = 0
                if result == "홀":
                    if text != '':
                        result = f"{result} :one: "
                    else:
                        result = f"{result} :one: "
                else:
                    if text != '':
                        result = f"{result} :two: "
                    else:
                        result = f"{result} :two: "
                round_rs = f"\n\n`{hz_round}회차` -- **{result}**"
                ch = client.get_channel(배팅내역)
                await ch.send(f"`{hz_round}회차`\n\n{text}")
                await rs_pe.send(f"{round_rs}")
                await bet_msg.delete()
    if message.content.startswith('.홀짝 '):
        #if hz_on != 0:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if not user_info[5] == 3:
            if message.content.split(" ")[2] == "올인":
                if (int(user_info[1]) >= 1000):
                    amount = int(user_info[1])
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                try:
                    amount = int(message.content.split(" ")[2])
                except:
                    con.close()
                    await message.channel.send(embed=talmoembed("배팅실패", "**```금액은 정수만 배팅이 가능합니다.```**"))
                    return
            if not amount < 1000:
                if user_info[1] >= amount:
                    if t > 10:
                        if not message.author.id in doing_bet:
                            doing_bet.append(message.author.id)

                            choice = message.content.split(" ")[1]
                            if user_info[1] >= 1000:
                                if choice == "홀":
                                    hz_h.append(message.author.id)
                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                (user_info[1] - amount, message.author.id))
                                    cur.execute("UPDATE users SET hz_bet_pick = ? WHERE id == ?;",
                                                (choice, message.author.id))
                                    cur.execute("UPDATE users SET hz_bet_money = ? WHERE id == ?;",
                                                (amount, message.author.id))
                                    con.commit()
                                    con.close()
                                    await message.channel.send(
                                        f"**> {hz_round}회차 {choice}에 배팅이 완료되었습니다.\n\n잔액 : {user_info[1] - amount}**")
                                    hz_total_h += amount
                                elif choice == "짝":
                                    hz_z.append(message.author.id)
                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                (user_info[1] - amount, message.author.id))
                                    cur.execute("UPDATE users SET hz_bet_pick = ? WHERE id == ?;",
                                                (choice, message.author.id))
                                    cur.execute("UPDATE users SET hz_bet_money = ? WHERE id == ?;",
                                                (amount, message.author.id))
                                    con.commit()
                                    con.close()
                                    await message.channel.send(
                                        f"**> {hz_round}회차 {choice}에 배팅이 완료되었습니다.\n\n잔액 : {user_info[1] - amount}**")
                                    hz_total_z += amount
                                else:
                                    con.close()
                                    await message.channel.send(
                                        embed=talmoembed("배팅실패", "**```홀/짝 중에서만 배팅해주세요.```**"))
                            else:
                                con.close()
                                await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```이미 배팅중입니다.```**"))
                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("배팅실패", "**```배팅이 마감되었습니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("배팅실패", "**```1000원이상부터 배팅이 가능합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))
    #else:
        #await message.channel.send(embed=talmoembed("배팅실패", "**```게임이 진행되고있지않습니다.```**"))

    if message.content.startswith('.비트코인사다리 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 1000):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 1000):
                if (amount <= user_info[1]):
                    req = requests.get("https://bepick.net/json/game/btc_ladder.json?" + str(time.time()).split(".")[0],
                                    headers={
                                        "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        # "Host": "ntry.com",
                                        # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }).json()

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 15):
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                button_first_hole = Button(label="좌", custom_id="좌", style=ButtonStyle.blue)
                                button_first_zzak = Button(label="우", custom_id="우", style=ButtonStyle.red)
                                button_first_un = Button(label="삼", custom_id="삼", style=ButtonStyle.blue)
                                button_first_op = Button(label="사", custom_id="사", style=ButtonStyle.red)
                                button_pa_hole = Button(label="홀", custom_id="홀", style=ButtonStyle.blue)
                                button_pa_zzak = Button(label="짝", custom_id="짝", style=ButtonStyle.red)

                                embed = discord.Embed(title="배팅하기",
                                                    description='**비트코인사다리 배팅하기**\n**```배팅할 곳의 버튼을 클릭하여 배팅해주세요.```**\n**```diff\n+ The bet was successful.```**',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [button_first_hole, button_first_zzak, button_first_un, button_first_op],
                                    [button_pa_hole, button_pa_zzak],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('시간초과', "**```py\n버튼은 5초동안 누르실수있습니다. 다시 시도해주세요.```**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET ladder_bet_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET ladder_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        con.commit()
                                        con.close()
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        req = requests.get('https://bepick.net/live/result/btc_ladder', headers={
                                            "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                            # "Host": "ntry.com",
                                            # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                            "X-Requested-With": "XMLHttpRequest",
                                        }).json()
                                        await message.reply(embed=talmoembed('배팅완료',
                                                                            f'<@{message.author.id}>\n**```배팅완료\n\n{interaction.custom_id} / {str(amount)}\n\n{int(req["round"]) + 1}회차에 진행됩니다.```**'))
                                        con.close()
                                        break
                                    # else:
                                    #     embed = discord.Embed(title='보글게임즈', description="**배팅 실패**\n**```배팅은 본인만 가능합니다.```**", color=0x2f3136)
                                    #     embed.set_footer(text='보글게임즈')
                                    #     await interaction.respond(embed=embed)
                                    #     continue

                            else:
                                con.close()
                                await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("배팅실패", "**```배팅이 마감되었습니다.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("배팅실패", "**```1000원이상부터 배팅이 가능합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("배팅실패", "**```가입되어 있지 않은 유저입니다.```**"))

    if message.content.startswith('.보글사다리 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 1000):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 1000):
                if (amount <= user_info[1]):
                    req = requests.get(
                        "https://bepick.net/json/game/bubble_ladder3.json?" + str(time.time()).split(".")[0],
                        headers={
                            "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                            # "Host": "ntry.com",
                            # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                            "X-Requested-With": "XMLHttpRequest",
                        }).json()

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 15):
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                button_first_hole = Button(label="좌", custom_id="좌", style=ButtonStyle.blue)
                                button_first_zzak = Button(label="우", custom_id="우", style=ButtonStyle.red)
                                button_first_un = Button(label="삼", custom_id="삼", style=ButtonStyle.blue)
                                button_first_op = Button(label="사", custom_id="사", style=ButtonStyle.red)
                                button_pa_hole = Button(label="홀", custom_id="홀", style=ButtonStyle.blue)
                                button_pa_zzak = Button(label="짝", custom_id="짝", style=ButtonStyle.red)

                                embed = discord.Embed(title="배팅하기",
                                                    description='**보글사다리 배팅하기**\n**```배팅할 곳의 버튼을 클릭하여 배팅해주세요.```**\n**```diff\n+ The bet was successful.```**',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [button_first_hole, button_first_zzak, button_first_un, button_first_op],
                                    [button_pa_hole, button_pa_zzak],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('시간초과', "**```py\n버튼은 5초동안 누르실수있습니다. 다시 시도해주세요.```**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET rotoball_bet_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET rotoball_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        con.commit()
                                        con.close()
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        req = requests.get('https://bepick.net/live/result/bubble_ladder3', headers={
                                            "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                            # "Host": "ntry.com",
                                            # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                            "X-Requested-With": "XMLHttpRequest",
                                        }).json()
                                        await message.reply(embed=talmoembed('배팅완료',
                                                                            f'<@{message.author.id}>\n**```배팅완료\n\n{interaction.custom_id} / {str(amount)}\n\n{int(req["round"]) + 1}회차에 진행됩니다.```**'))
                                        con.close()
                                        break
                                    # else:
                                    #     embed = discord.Embed(title='보글게임즈', description="**배팅 실패**\n**```배팅은 본인만 가능합니다.```**", color=0x2f3136)
                                    #     embed.set_footer(text='보글게임즈')
                                    #     await interaction.respond(embed=embed)
                                    #     continue

                            else:
                                con.close()
                                await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("배팅실패", "**```배팅이 마감되었습니다.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("배팅실패", "**```1000원이상부터 배팅이 가능합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("배팅실패", "**```가입되어 있지 않은 유저입니다.```**"))

    if message.content.startswith('.와이룰렛 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 1000):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 1000):
                if (amount <= user_info[1]):
                    req = requests.get("https://bepick.net/json/game/y_roulette.json?" + str(time.time()).split(".")[0],
                                    headers={
                                        "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }).json()

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 15):
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                button_first_red = Button(label="빨강", custom_id="빨강", style=ButtonStyle.red)
                                button_first_yellow = Button(label="노랑", custom_id="노랑", style=ButtonStyle.blue)
                                button_first_hole = Button(label="홀", custom_id="홀", style=ButtonStyle.blue)
                                button_first_zzak = Button(label="짝", custom_id="짝", style=ButtonStyle.red)
                                button_first_un = Button(label="언더", custom_id="언더", style=ButtonStyle.blue)
                                button_first_op = Button(label="오버", custom_id="오버", style=ButtonStyle.red)

                                embed = discord.Embed(title="배팅하기",
                                                    description='**와이룰렛 배팅하기**\n**```배팅할 곳의 버튼을 클릭하여 배팅해주세요.```**\n**```diff\n+ The bet was successful.```**',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [button_first_red, button_first_yellow],
                                    [button_first_hole, button_first_zzak, button_first_un, button_first_op],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('시간초과', "**```py\n버튼은 5초동안 누르실수있습니다. 다시 시도해주세요.```**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET wllet_bet_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET wllet_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        con.commit()
                                        con.close()
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        req = requests.get('https://bepick.net/live/result/y_roulette', headers={
                                            "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                            # "Host": "ntry.com",
                                            # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                            "X-Requested-With": "XMLHttpRequest",
                                        }).json()

                                        await message.reply(embed=talmoembed('배팅완료',
                                                                            f'<@{message.author.id}>\n**```배팅완료\n\n{interaction.custom_id} / {str(amount)}\n\n{int(req["round"]) + 1}회차에 진행됩니다.```**'))
                                        con.close()
                                        break
                                    # else:
                                    #     embed = discord.Embed(title='보글게임즈', description="**배팅 실패**\n**```배팅은 본인만 가능합니다.```**", color=0x2f3136)
                                    #     embed.set_footer(text='보글게임즈')
                                    #     await interaction.respond(embed=embed)
                                    #     continue

                            else:
                                con.close()
                                await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("배팅실패", "**```배팅이 마감되었습니다.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("배팅실패", "**```1000원이상부터 배팅이 가능합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("배팅실패", "**```가입되어 있지 않은 유저입니다.```**"))

    if message.content.startswith('.타조 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 1000):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 1000):
                if (amount <= user_info[1]):
                    req = requests.get(
                        "https://bepick.net/json/game/jw_ostrichrun.json?" + str(time.time()).split(".")[0], headers={
                            "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                            "X-Requested-With": "XMLHttpRequest",
                        }).json()

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 15):
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                owrunright = Button(label="우", custom_id="우", style=ButtonStyle.blue)
                                owrunleft = Button(label="좌", custom_id="좌", style=ButtonStyle.red)

                                embed = discord.Embed(title="배팅하기",
                                                    description='**타조게임 배팅하기**\n**```배팅할 곳의 버튼을 클릭하여 배팅해주세요.```**\n**```diff\n+ The bet was successful.```**',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [owrunright, owrunleft],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('시간초과', "**```py\n버튼은 5초동안 누르실수있습니다. 다시 시도해주세요.```**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET owrun_bet_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET owrun_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        con.commit()
                                        con.close()
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        req = requests.get('https://bepick.net/live/result/jw_ostrichrun', headers={
                                            "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                            # "Host": "ntry.com",
                                            # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                            "X-Requested-With": "XMLHttpRequest",
                                        }).json()

                                        await message.reply(embed=talmoembed('배팅완료',
                                                                            f'<@{message.author.id}>\n**```배팅완료\n\n{interaction.custom_id} / {str(amount)}\n\n{int(req["round"]) + 1}회차에 진행됩니다.```**'))
                                        con.close()
                                        break
                                    # else:
                                    #     embed = discord.Embed(title='보글게임즈', description="**배팅 실패**\n**```배팅은 본인만 가능합니다.```**", color=0x2f3136)
                                    #     embed.set_footer(text='보글게임즈')
                                    #     await interaction.respond(embed=embed)
                                    #     continue
                                else:
                                    await bet_msg.delete()
                                    con.close()

                            else:
                                con.close()
                                await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("배팅실패", "**```배팅이 마감되었습니다.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("배팅실패", "**```1000원이상부터 배팅이 가능합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("배팅실패", "**```가입되어 있지 않은 유저입니다.```**"))

    if message.content.startswith('.보글볼 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 1000):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 1000):
                if (amount <= user_info[1]):
                    req = requests.get(
                        "https://bepick.net/json/game/bubble_power.json?" + str(time.time()).split(".")[0], headers={
                            "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                            # "Host": "ntry.com",
                            # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                            "X-Requested-With": "XMLHttpRequest",
                        }).json()

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 30):
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                button_first_hole = Button(label="일홀", custom_id="일홀", style=ButtonStyle.blue)
                                button_first_zzak = Button(label="일짝", custom_id="일짝", style=ButtonStyle.red)
                                button_first_un = Button(label="일언", custom_id="일언", style=ButtonStyle.blue)
                                button_first_op = Button(label="일옵", custom_id="일옵", style=ButtonStyle.red)
                                button_pa_hole = Button(label="파홀", custom_id="파홀", style=ButtonStyle.blue)
                                button_pa_zzak = Button(label="파짝", custom_id="파짝", style=ButtonStyle.red)
                                button_pa_un = Button(label="파언", custom_id="파언", style=ButtonStyle.blue)
                                button_pa_op = Button(label="파옵", custom_id="파옵", style=ButtonStyle.red)

                                embed = discord.Embed(title="배팅하기",
                                                    description='**보글파워볼 배팅하기**\n**```배팅할 곳의 버튼을 클릭하여 배팅해주세요.```**\n**```diff\n+ The bet was successful.```**',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [button_first_hole, button_first_zzak, button_first_un, button_first_op],
                                    [button_pa_hole, button_pa_zzak, button_pa_un, button_pa_op],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('시간초과', "**```py\n버튼은 5초동안 누르실수있습니다. 다시 시도해주세요.```**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET boggle_bet_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET boggle_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        con.commit()
                                        con.close()
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        req = requests.get('https://bepick.net/live/result/bubble_power', headers={
                                            "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                            # "Host": "ntry.com",
                                            # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                            "X-Requested-With": "XMLHttpRequest",
                                        }).json()

                                        await message.reply(embed=talmoembed('배팅완료',
                                                                            f'<@{message.author.id}>\n**```배팅완료\n\n{interaction.custom_id} / {str(amount)}\n\n{int(req["round"]) + 1}회차에 진행됩니다.```**'))
                                        con.close()
                                        break
                                    # else:
                                    #     embed = discord.Embed(title='보글게임즈', description="**배팅 실패**\n**```배팅은 본인만 가능합니다.```**", color=0x2f3136)
                                    #     embed.set_footer(text='보글게임즈')
                                    #     await interaction.respond(embed=embed)
                                    #     continue

                            else:
                                con.close()
                                await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("배팅실패", "**```배팅이 마감되었습니다.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("배팅실패", "**```1000원이상부터 배팅이 가능합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("배팅실패", "**```가입되어 있지 않은 유저입니다.```**"))

    if message.content.startswith('.파워볼 '):
        await message.channel.send(embed=talmoembed("오류", "**```리틀뱅크에는 파워볼이 없습니다!```**"))

        # con = sqlite3.connect("./database/database.db")
        # cur = con.cursor()
        # cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        # user_info = cur.fetchone()

        # if (user_info == None):
        #     cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
        #         message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
        #         None,
        #         None, None, None, None, None, None, None, None, None, None, None, None))
        #     con.commit()
        #     con.close()

        # con = sqlite3.connect("./database/database.db")
        # cur = con.cursor()
        # cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        # user_info = cur.fetchone()

        # if not (user_info == None):
        #     if (amount >= 1000):
        #         if (amount <= user_info[1]):
        #             req = requests.get(
        #                 "https://bepick.net/json/game/nlotto_power.json?" + str(time.time()).split(".")[0], headers={
        #                     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
        #                     # "Host": "ntry.com",
        #                     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
        #                     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
        #                     "X-Requested-With": "XMLHttpRequest",
        #                 }).json()

        #             res = req['time_set']

        #             if not (int(res['nextTime']) <= 20):
        #                 if (user_info[12] == None):
        #                     if not (user_info[5] == 3):
        #                         button_first_hole = Button(label="일홀", custom_id="일홀", style=ButtonStyle.blue)
        #                         button_first_zzak = Button(label="일짝", custom_id="일짝", style=ButtonStyle.red)
        #                         button_first_un = Button(label="일언", custom_id="일언", style=ButtonStyle.blue)
        #                         button_first_op = Button(label="일옵", custom_id="일옵", style=ButtonStyle.red)
        #                         button_pa_hole = Button(label="파홀", custom_id="파홀", style=ButtonStyle.blue)
        #                         button_pa_zzak = Button(label="파짝", custom_id="파짝", style=ButtonStyle.red)
        #                         button_pa_un = Button(label="파언", custom_id="파언", style=ButtonStyle.blue)
        #                         button_pa_op = Button(label="파옵", custom_id="파옵", style=ButtonStyle.red)

        #                         embed = discord.Embed(title="배팅하기",
        #                                             description='**파워볼 배팅하기**\n**```배팅할 곳의 버튼을 클릭하여 배팅해주세요.```**\n**```diff\n+ The bet was successful.```**',
        #                                             color=0x2f3136)
        #                         embed.set_footer(text=서버이름)
        #                         bet_msg = await message.reply(embed=embed, components=
        #                         ActionRow(
        #                             [button_first_hole, button_first_zzak, button_first_un, button_first_op],
        #                             [button_pa_hole, button_pa_zzak, button_pa_un, button_pa_op],
        #                         )
        #                                                     )
        #                         while True:
        #                             if message.author.id == 1013479428958998528:
        #                                 interaction = await client.wait_for("button_click",
        #                                                                     check=lambda inter: inter.custom_id != "")
        #                             else:
        #                                 try:
        #                                     interaction = await client.wait_for("button_click",
        #                                                                         check=lambda
        #                                                                             inter: inter.custom_id != "",
        #                                                                         timeout=5)
        #                                 except asyncio.exceptions.TimeoutError:
        #                                     await message.reply(
        #                                         embed=talmoembed('시간초과', "**```py\n버튼은 5초동안 누르실수있습니다. 다시 시도해주세요.```**"))
        #                                     await bet_msg.delete()

        #                             if message.author.id == interaction.user.id:
        #                                 await bet_msg.delete()
        #                                 cur.execute("UPDATE users SET money = ? WHERE id == ?;",
        #                                             (user_info[1] - amount, interaction.user.id))
        #                                 con.commit()
        #                                 cur.execute("UPDATE users SET pwball_bet_pick = ? WHERE id == ?;",
        #                                             (interaction.custom_id, interaction.user.id))
        #                                 con.commit()
        #                                 cur.execute("UPDATE users SET pwball_bet_money = ? WHERE id == ?;",
        #                                             (amount, interaction.user.id))
        #                                 con.commit()
        #                                 con.close()
        #                                 # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
        #                                 # ress = req.json()['prevGame']
        #                                 req = requests.get('https://bepick.net/live/result/nlotto_power', headers={
        #                                     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
        #                                     # "Host": "ntry.com",
        #                                     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
        #                                     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
        #                                     "X-Requested-With": "XMLHttpRequest",
        #                                 }).json()

        #                                 await message.reply(embed=talmoembed('배팅완료',
        #                                                                     f'<@{message.author.id}>\n**```배팅완료\n\n{interaction.custom_id} / {str(amount)}\n\n{int(req["round"]) + 1}회차에 진행됩니다.```**'))
        #                                 con.close()
        #                                 break
        #                             # else:
        #                             #     embed = discord.Embed(title='보글게임즈', description="**배팅 실패**\n**```배팅은 본인만 가능합니다.```**", color=0x2f3136)
        #                             #     embed.set_footer(text='보글게임즈')
        #                             #     await interaction.respond(embed=embed)
        #                             #     continue

        #                     else:
        #                         con.close()
        #                         await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))
        #                 else:
        #                     con.close()
        #                     await message.channel.send(embed=talmoembed("배팅실패", "**```이미 배팅중입니다.```**"))

        #             else:
        #                 con.close()
        #                 await message.channel.send(embed=talmoembed("배팅실패", "**```배팅이 마감되었습니다.```**"))

        #         else:
        #             con.close()
        #             await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
        #     else:
        #         con.close()
        #         await message.channel.send(embed=talmoembed("배팅실패", "**```1000원이상부터 배팅이 가능합니다.```**"))
        # else:
        #     con.close()
        #     await message.channel.send(embed=talmoembed("배팅실패", "**```가입되어 있지 않은 유저입니다.```**"))

    if message.content.startswith('.이오스1분 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 1000):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 1000):
                if (amount <= user_info[1]):
                    req = requests.get("https://bepick.net/json/game/eosball1m.json?" + str(time.time()).split(".")[0],
                                    headers={
                                        "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        # "Host": "ntry.com",
                                        # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }).json()

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 20):
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                button_first_hole = Button(label="일홀", custom_id="일홀", style=ButtonStyle.blue)
                                button_first_zzak = Button(label="일짝", custom_id="일짝", style=ButtonStyle.red)
                                button_first_un = Button(label="일언", custom_id="일언", style=ButtonStyle.blue)
                                button_first_op = Button(label="일옵", custom_id="일옵", style=ButtonStyle.red)
                                button_pa_hole = Button(label="파홀", custom_id="파홀", style=ButtonStyle.blue)
                                button_pa_zzak = Button(label="파짝", custom_id="파짝", style=ButtonStyle.red)
                                button_pa_un = Button(label="파언", custom_id="파언", style=ButtonStyle.blue)
                                button_pa_op = Button(label="파옵", custom_id="파옵", style=ButtonStyle.red)

                                embed = discord.Embed(title="배팅하기",
                                                    description='**EOS1분파워볼 배팅하기**\n**```배팅할 곳의 버튼을 클릭하여 배팅해주세요.```**\n**```diff\n+ The bet was successful.```**',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [button_first_hole, button_first_zzak, button_first_un, button_first_op],
                                    [button_pa_hole, button_pa_zzak, button_pa_un, button_pa_op],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('시간초과', "**```py\n버튼은 5초동안 누르실수있습니다. 다시 시도해주세요.```**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET eos1_bet_pcik = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET eos1_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        con.commit()
                                        con.close()
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        req = requests.get('https://bepick.net/live/result/eosball1m', headers={
                                            "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                            # "Host": "ntry.com",
                                            # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                            "X-Requested-With": "XMLHttpRequest",
                                        }).json()

                                        await message.reply(embed=talmoembed('배팅완료',
                                                                            f'<@{message.author.id}>\n**```배팅완료\n\n{interaction.custom_id} / {str(amount)}\n\n{int(req["round"]) + 1}회차에 진행됩니다.```**'))
                                        con.close()
                                        break
                                    # else:
                                    #     embed = discord.Embed(title='보글게임즈', description="**배팅 실패**\n**```배팅은 본인만 가능합니다.```**", color=0x2f3136)
                                    #     embed.set_footer(text='보글게임즈')
                                    #     await interaction.respond(embed=embed)
                                    #     continue

                            else:
                                con.close()
                                await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("배팅실패", "**```배팅이 마감되었습니다.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("배팅실패", "**```1000원이상부터 배팅이 가능합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("배팅실패", "**```가입되어 있지 않은 유저입니다.```**"))
    if message.content.startswith('.이오스5분 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 1000):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 1000):
                if (amount <= user_info[1]):
                    req = requests.get("https://bepick.net/json/game/eosball5m.json?" + str(time.time()).split(".")[0],
                                    headers={
                                        "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        # "Host": "ntry.com",
                                        # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        "X-Requested-With": "XMLHttpRequest",
                                    }).json()

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 20):
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                button_first_hole = Button(label="일홀", custom_id="일홀", style=ButtonStyle.blue)
                                button_first_zzak = Button(label="일짝", custom_id="일짝", style=ButtonStyle.red)
                                button_first_un = Button(label="일언", custom_id="일언", style=ButtonStyle.blue)
                                button_first_op = Button(label="일옵", custom_id="일옵", style=ButtonStyle.red)
                                button_pa_hole = Button(label="파홀", custom_id="파홀", style=ButtonStyle.blue)
                                button_pa_zzak = Button(label="파짝", custom_id="파짝", style=ButtonStyle.red)
                                button_pa_un = Button(label="파언", custom_id="파언", style=ButtonStyle.blue)
                                button_pa_op = Button(label="파옵", custom_id="파옵", style=ButtonStyle.red)

                                embed = discord.Embed(title="배팅하기",
                                                    description='**EOS5분파워볼 배팅하기**\n**```배팅할 곳의 버튼을 클릭하여 배팅해주세요.```**\n**```diff\n+ The bet was successful.```**',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [button_first_hole, button_first_zzak, button_first_un, button_first_op],
                                    [button_pa_hole, button_pa_zzak, button_pa_un, button_pa_op],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('시간초과', "**```py\n버튼은 5초동안 누르실수있습니다. 다시 시도해주세요.```**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET eos5_bet_pcik = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET eos5_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        con.commit()
                                        con.close()
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        req = requests.get('https://bepick.net/live/result/eosball5m', headers={
                                            "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                            # "Host": "ntry.com",
                                            # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                            "X-Requested-With": "XMLHttpRequest",
                                        }).json()

                                        await message.reply(embed=talmoembed('배팅완료',
                                                                            f'<@{message.author.id}>\n**```배팅완료\n\n{interaction.custom_id} / {str(amount)}\n\n{int(req["round"]) + 1}회차에 진행됩니다.```**'))
                                        con.close()
                                        break
                                    # else:
                                    #     embed = discord.Embed(title='보글게임즈', description="**배팅 실패**\n**```배팅은 본인만 가능합니다.```**", color=0x2f3136)
                                    #     embed.set_footer(text='보글게임즈')
                                    #     await interaction.respond(embed=embed)
                                    #     continue

                            else:
                                con.close()
                                await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("배팅실패", "**```배팅이 마감되었습니다.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("배팅실패", "**```1000원이상부터 배팅이 가능합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("배팅실패", "**```가입되어 있지 않은 유저입니다.```**"))

    if message.content.startswith('.정보'):
        try:
            m = message.content.split(" ")[1]
            m = m.split('@')[1]
            m = m.split('>')[0]
            id = int(m)
        except Exception as e:
            id = message.author.id
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            con.close()
            await message.reply(
                embed=talmoembed('정보', f"```py\n보유하신 머니 : {str(user_info[1])}원\n\n현재 매수액 : {str(user_info[-2])}```"))
        else:
            con.close()
            await message.reply(embed=talmoembed('실패', "**```가입되있지않은 유저입니다.```**"))
    if message.content.startswith('.충전 '):
        log_id = 입출금로그
        log_ch = client.get_channel(int(log_id))
        if message.author.id in admin_id:
            try:
                user_id = message.mentions[0].id
                amount = int(message.content.split(" ")[2])
            except:
                con.close()
                await message.reply(embed=talmoembed('실패', "**```정확하게 명령어를 입력해주세요!```**"))
                return

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] + amount, user_id))

                con.commit()
                con.close()
                ktotal += int(amount)
                await message.reply(embed=talmoembed('충전성공',
                                                    f"```py\n{str(amount)}원 충전 성공\n\n{str(user_info[1])}원 -> {str(user_info[1] + amount)}원```"))
                await log_ch.send(f"<@{message.mentions[0].id}>님이 {amount}원을 충전하셨습니다")
            else:
                con.close()
                await message.channel.send(embed=talmoembed("충전실패", "**```가입되어 있지 않은 유저입니다.```**"))

    if message.content.startswith('.차감 '):
        if message.author.id in admin_id:
            try:
                user_id = message.mentions[0].id
                amount = int(message.content.split(" ")[2])
            except:
                con.close()
                await message.reply(embed=talmoembed('실패', "**```정확하게 명령어를 입력해주세요!```**"))
                return

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] - amount, user_id))
                con.commit()
                total -= int(amount)
                await message.reply(embed=talmoembed('차감성공',
                                                    f"```py\n{str(amount)}원 차감 성공\n\n{str(user_info[1])}원 -> {str(user_info[1] - amount)}원```"))
                res = getinfo(user_id)
                webhook = DiscordWebhook(
                    url=입출금로그웹훅,
                    username='환전로그',
                    avatar_url=f"https://cdn.discordapp.com/avatars/{user_id}/{res['avatar']}.webp?size=80",
                    content=f'<@{user_id}> 님이 {amount}원을 환전하셨습니다.')
                webhook.execute()
            else:
                con.close()
                await message.channel.send(embed=talmoembed("차감실패", "**```가입되어 있지 않은 유저입니다.```**"))

    if message.content.startswith('.강제충전 '):
        log_id = 입출금로그
        log_ch = client.get_channel(int(log_id))
        if message.author.id in admin_id:
            try:
                user_id = message.mentions[0].id
                amount = int(message.content.split(" ")[2])
            except:
                con.close()
                await message.reply(embed=talmoembed('실패', "**```정확하게 명령어를 입력해주세요!```**"))
                return

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] + amount, user_id))

                con.commit()
                await message.reply(embed=talmoembed('충전성공',
                                                    f"```py\n{str(amount)}원 강제충전 성공\n\n{str(user_info[1])}원 -> {str(user_info[1] + amount)}원```"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("충전실패", "**```가입되어 있지 않은 유저입니다.```**"))

    if message.content.startswith('.강제차감 '):
        if message.author.id in admin_id:
            try:
                user_id = message.mentions[0].id
                amount = int(message.content.split(" ")[2])
            except:
                con.close()
                await message.reply(embed=talmoembed('실패', "**```정확하게 명령어를 입력해주세요!```**"))
                return

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] - amount, user_id))
                con.commit()
                total -= int(amount)
                await message.reply(embed=talmoembed('차감성공',
                                                    f"```py\n{str(amount)}원 강제차감 성공\n\n{str(user_info[1])}원 -> {str(user_info[1] - amount)}원```"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("차감실패", "**```가입되어 있지 않은 유저입니다.```**"))

    if message.content.startswith('!블랙리스트 '):
        if message.author.id in admin_id:
            user_id = message.mentions[0].id

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                cur.execute("UPDATE users SET ban = ? WHERE id == ?;", (3, user_id))
                con.commit()
                con.close()
                await message.reply(embed=talmoembed('추가성공', "**```성공적으로 블랙리스트 추가를 완료하였습니다!```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("추가실패", "**```가입되어 있지 않은 유저입니다.```**"))

    if message.content.startswith('!화이트리스트 '):
        if message.author.id in admin_id:
            user_id = message.mentions[0].id

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                cur.execute("UPDATE users SET ban = ? WHERE id == ?;", (0, user_id))
                con.commit()
                con.close()
                await message.reply(embed=talmoembed('추가성공', "**```성공적으로 화이트리스트 추가를 완료하였습니다!```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("추가실패", "**```가입되어 있지 않은 유저입니다.```**"))
    if message.content.startswith("!수익"):
        if message.author.id in admin_id:

            log = ""

            id = 입출금로그
            channel = client.get_channel(int(id))
            msg=await message.reply("잠시 기다려주세요...")
            async for messaged in channel.history(limit=None):
                titiititit = str(messaged.created_at)
                titiititit = titiititit.split("-")[2]

                date = int(titiititit.split(" ")[0])
                hour = int(titiititit.split(" ")[1].split(":")[0])
                if int(hour) >= 15:
                    date += 1
                hour += 9
                if int(hour) >= 24:
                    hour -= 12
                if date>31:
                    date=1
                if messaged.content != None:
                    if date == int(datetime.datetime.now().day):
                        log += f"{messaged.content} ({date}일 {hour}시)\n"
                    if date!=int(datetime.datetime.now().day):
                        break

            list_basic=log.split("\n")
            list_a=[]
            list_b=[]
            for i in list_basic:
                if "충전" in i:
                    list_a.append(i)
            for i in list_basic:
                if "환전하" in i:
                    list_b.append(i)
            money=0
            mm=0
            for i in list_a:
                ii=i.split("원을")[0]
                numbers=ii.split("님이 ")[1]
                money+=int(numbers)
            for i in list_b:
                ii=i.split("원을")[0]
                numbers=ii.split("님이 ")[1]
                mm+=int(numbers)
            embed = discord.Embed(title="오늘 수익",
                                description=f"총 충전액 : {money}\n\n환전해준돈 : {round(mm*0.9)}\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n총 수익 : {money - round(mm*0.9)}",
                                color=0x2f3136)
            await msg.edit(content="", embed=embed)
        else:
            await message.reply(embed=talmoembed("권한없음", "관리자만 사용가능한 명령어입니다."))
        
    if message.content == '!명령어':
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        embed = discord.Embed(title="명령어",
                            description='**.정보**\n**```가입 및 정보를 확인 합니다.```**\n**.비트코인사다리 [ 금액 ]**\n**```비트코인사다리에 배팅을 합니다!```**\n**.보글사다리 [ 금액 ]**\n**```보글사다리에 배팅을 합니다!```**\n**.보글볼 [ 금액 ]**\n**```보글파워볼에 배팅합니다!```**\n**.와이룰렛 [ 금액 ]**\n**```와이룰렛에 배팅합니다!```**\n**.타조 [ 금액 ]**\n**```타조게임에 배팅합니다!```**\n**.이오스1분 [ 금액 ]**\n**```EOS 1분에 배팅합니다!```**\n**.이오스5분 [ 금액 ]**\n**```EOS 5분에 배팅합니다!```**\n**.홀짝 [ 홀/짝 ] [ 금액 ]**\n**```홀짝게임에 배팅합니다!```**\n**.용호 [ 용/호/무 ] [ 금액 ]**\n**```용호에 배팅합니다!```**\n**.바카라 [ 플/뱅/무 ] [ 금액 ]**\n**```바카라에 배팅합니다!```**\n**.룰렛 [ 검/빨/초 ] [ 금액 ]**\n**```룰렛에 배팅합니다!```**\n**!그래프 [ 금액 ]**\n**```그래프 게임에 배팅합니다!```**',
                            color=0x2f3136)
        embed.set_footer(text=서버이름)
        await message.channel.send(embed=embed)
    if message.guild is None:
        if message.author.bot:
            return
        else:
            embed = discord.Embed(colour=discord.Colour.blue(), timestamp=message.created_at)
            embed.add_field(name='전송자', value=message.author, inline=False)
            if message.attachments != []:
                for attach in message.attachments:
                    m = attach.url
                embed.set_image(url=m)
            else:
                embed.add_field(name='내용', value=message.content, inline=False)
            await client.get_channel(봇디엠로그).send(f"`{message.author.name}({message.author.id})`",
                                                embed=embed)
                                                 
            
    if message.content.startswith('!이벤트'):
        if message.author.id in admin_id:
            perc = message.content.split(" ")[1]
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (client.user.id,))
            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                            (perc, client.user.id))
            con.commit()
            con.close()
            await message.reply(f"> **이벤트 퍼센트가 `{perc}%` 추가로 변경되었습니다.**")

    if message.content.startswith('!자동졸업 '):
        if message.author.id in admin_id:
            magi = message.content.split(" ")[1]
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (client.user.id,))
            cur.execute("UPDATE users SET perc = ? WHERE id == ?;",
                            (magi, client.user.id))
            con.commit()
            con.close()
            await message.reply(f"> **자동졸업 금액이 `{magi}원` 으로 변경되었습니다.**")

    if message.content == "!용호":
        if message.author.id in admin_id:
            rs_pe = client.get_channel(용호회차)
            # pe_rs = await rs_pe.send(f"`1회차`가 진행되고있습니다.")
            round_rs = ''
            oplog = ''

        #if dt_on == 0:
            await message.channel.send(f"<#{용호채널}> 에 게임이 시작됩니다.")
            dt_on = 1
            dt_round = 0
            while True:
                dt_round += 1
                d_card = random.randint(1, 13)
                t_card = random.randint(1, 13)
                rs_ch = 용호유출픽
                await client.get_channel(rs_ch).send(
                    f"{dt_round}회차\n용" if d_card > t_card else f"{dt_round}회차\n호" if t_card > d_card else f"{dt_round}회차\n무승부")
                tim = 60
                dt_ch = client.get_channel(용호채널)
                # player = Button(label="용", custom_id="용", style=ButtonStyle.red)
                # banker = Button(label="호", custom_id="호", style=ButtonStyle.blue)
                # draw = Button(label="무승부", custom_id="용호무승부", style=ButtonStyle.green)
                bet_embed = discord.Embed(title=f"{dt_round}회차 배팅가능시간입니다.",
                                        description=f"용, 호, 또는 무승부에 배팅해주십시오.\n남은 배팅시간 : `{tim}`", color=0x2f3136)
                bet_embed.set_footer(text=서버이름)
                bet_msg = await dt_ch.send(embed=bet_embed)
                for i in range(0, 12):
                    await asyncio.sleep(5)
                    tim -= 5
                    bet_embed = discord.Embed(title=f"{dt_round}회차 배팅가능시간입니다.",
                                            description=f"용, 호, 또는 무승부에 배팅해주십시오.\n남은 배팅시간 : `{tim}`",
                                            color=0x2f3136)
                    bet_embed.set_footer(text=서버이름)
                    await bet_msg.delete()
                    bet_msg = await dt_ch.send(embed=bet_embed)
                close_embed = discord.Embed(title=f"{dt_round}회차 배팅이 마감되었습니다", description=f'''
```
🐉 용  ||  🐯 호

`{d_card}` //   `{t_card}`
```
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
🐉 용 : {d_card} {"✅" if d_card > t_card else ""}   {"< 승리! > X2배" if d_card > t_card else ""}\n
🐯 호 : {t_card}   {"✅" if d_card < t_card else ""}   {"< 승리! > X2배" if d_card < t_card else ""}\n
🟢무승부{"< 승리! > X11배" if d_card == t_card else ""}''', color=0x2f3136)
                await bet_msg.delete()
                bet_msg = await dt_ch.send(embed=close_embed, components="")
                bet_log = ""
                result = "용" if d_card > t_card else '호' if t_card > d_card else '무승부'
                conn = sqlite3.connect('./database/database.db')
                c = conn.cursor()
                list_a = list(c.execute("SELECT * FROM users"))
                for i in list_a:
                    if (i[18] == None):
                        continue
                    conn = sqlite3.connect('./database/database.db')
                    c = conn.cursor()
                    if int(d_card) > int(t_card):
                        배당 = 2
                    elif int(t_card) > int(d_card):
                        배당 = 2
                    else:
                        배당 = 11

                    if i[18] == result:

                        bet_log += (f"**<@{i[0]}> {i[18]} {round(i[19] * 배당)} 적중**\n")
                        
                        f = open(f"./bet_log/{i[0]}.txt", "a", encoding="utf-8-sig")
                        f.write(
                            f'''                
배팅게임 : 용호
배팅회차 : {dt_round}
배팅내역 : {i[18]}
배팅금 : {i[19]}
적중 / 미적중 : 적중
적중 금액 : {round(i[19] * 배당-1)}
남은 금액 : {i[1] + round(i[19] * 배당)}
======================
''')
                        f.close()
                        c.execute("UPDATE users SET money = money + ? where id=?", (round(i[19] * 배당), i[0],))
                    elif result == "무승부":

                        bet_log += (f"**<@{i[0]}> {i[18]} {round(i[19] // 2)} 무승부**\n")
                        
                        f = open(f"./bet_log/{i[0]}.txt", "a", encoding="utf-8-sig")
                        f.write(
                            f'''                
배팅게임 : 용호
배팅회차 : {dt_round}
배팅내역 : {i[18]}
배팅금 : {i[19]}
적중 / 미적중 : 무승부
적중 금액 : {round(i[19] // 2)-i[19]}
남은 금액 : {i[1] + round(i[19]+round(i[19] // 2))}
======================
''')
                        f.close()
                        c.execute("UPDATE users SET money = money + ? where id=?",
                                (round(i[19] // 2), i[0],))
                    else:

                        bet_log += (f"**<@{i[0]}> {i[18]} 미적중**\n")
                        f = open(f"./bet_log/{i[0]}.txt", "a", encoding="utf-8-sig")
                        f.write(
                            f'''                
배팅게임 : 용호
배팅회차 : {dt_round}
배팅내역 : {i[18]}
배팅금 : {i[19]}
적중 / 미적중 : 미적중
남은 금액 : {i[1]}
======================
''')
                        f.close()

                    c.execute("UPDATE users SET powerladder_bet_pick = ? where id=?", (None, i[0],))
                    c.execute("UPDATE users SET powerladder_bet_money = ? where id=?", (None, i[0],))
                    conn.commit()
                    conn.close()
                if result == "용":
                    result = f"{result} 🐉"
                elif result == "호":
                    result = f"{result} 🐯"
                else:
                    result = f"{result} 🟢"
                round_rs = f"\n\n`{dt_round}회차` -- **{result}**"
                doing_bet4 = []
                oplog = ''
                ch = client.get_channel(용호배팅내역)
                await ch.send(f"`{dt_round}회차`\n\n{bet_log}")
                await rs_pe.send(f"{round_rs}")
    if message.content.startswith('.용호 '):
        #if dt_on != 0:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if not user_info[5] == 3:
            if message.content.split(" ")[2] == "올인":
                if (int(user_info[1]) >= 1000):
                    amount = int(user_info[1])
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                try:
                    amount = int(message.content.split(" ")[2])
                except:
                    con.close()
                    await message.channel.send(embed=talmoembed("배팅실패", "**```금액은 정수만 배팅이 가능합니다.```**"))
                    return
            if not amount < 1000:
                if user_info[1] >= amount:
                    choice = message.content.split(" ")[1]
                    if choice == "용" or choice == "호" or choice == "무":
                        if not message.author.id in doing_bet4:
                            doing_bet4.append(message.author.id)
                            if user_info[1] >= 1000:

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                            (user_info[1] - int(amount), message.author.id))
                                if choice == "용":
                                    dt_total_d = dt_total_d + int(amount)
                                elif choice == "호":
                                    dt_total_t = dt_total_t + int(amount)
                                else:
                                    choice = "무승부"
                                cur.execute("UPDATE users SET powerladder_bet_pick = ? WHERE id == ?;",
                                            (choice, message.author.id))

                                cur.execute("UPDATE users SET powerladder_bet_money = ? WHERE id == ?;",
                                            (amount, message.author.id))
                                con.commit()
                                con.close()
                                await message.reply(
                                    f"**> {dt_round}회차 {choice}에 배팅이 완료되었습니다.\n\n잔액 : {user_info[1] - amount}**")

                            else:
                                con.close()
                                await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```이미 배팅중입니다.```**"))
                    else:
                        con.close()
                        await message.channel.send("**```용/호/무 중에서만 배팅해주세요.```**")
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("배팅실패", "**```1000원이상부터 배팅이 가능합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))
    #else:
        #!await message.channel.send(embed=talmoembed("배팅실패", "**```게임이 진행되고있지않습니다.```**"))

    if message.content == "!바카라":
        if message.author.id in admin_id:
            rs_pe = client.get_channel(바카라회차)
            # pe_rs = await rs_pe.send(f"`1회차`가 진행되고있습니다.")
            round_rs = ''
            # leng = 0
            oplog = ''

        #if bakara_on == 0:
            await message.channel.send(f"<#{바카라채널}> 에 게임이 시작됩니다.")
            bakara_on = 1
            bkr_round = 0
            while True:
                bkr_round += 1
                bkr_p = []
                bkr_b = []
                bkr_d = []
                p_add_card = 0
                b_add_card = 0
                player_card = random.randint(1, 13)
                banker_card = random.randint(1, 13)
                if player_card >= 10:
                    player_card = 0
                if banker_card >= 10:
                    banker_card = 0
                player_card2 = random.randint(1, 13)
                banker_card2 = random.randint(1, 13)
                if player_card2 >= 10:
                    player_card2 = 0
                if banker_card2 >= 10:
                    banker_card2 = 0
                rs_ch = 바카라유출픽
                p = (player_card + player_card2) % 10
                b = (banker_card + banker_card2) % 10
                if p <= 5:
                    p_add_card = random.randint(1, 13)
                    if p_add_card >= 10:
                        p_add_card = 0
                p = (p + p_add_card) % 10
                if b == 4 or b == 5:
                    if b < p:
                        b_add_card = random.randint(1, 13)
                        if b_add_card >= 10:
                            b_add_card = 0
                elif b <= 5:
                    b_add_card = random.randint(1, 13)
                    if b_add_card >= 10:
                        b_add_card = 0
                b = (b + b_add_card) % 10
                if p == b and p == 5:
                    p_add_card = random.randint(1, 13)
                    if p_add_card >= 10:
                        p_add_card = 0
                    p = (p + p_add_card) % 10
                await client.get_channel(rs_ch).send(
                    f"{bkr_round}회차\n플레이어" if p > b else f"{bkr_round}회차\n뱅커" if b > p else f"{bkr_round}회차\n무승부")
                ti = 60
                bkr_ch = client.get_channel(바카라채널)
                # player = Button(label="플레이어", custom_id="플레이어", style=ButtonStyle.blue)
                # banker = Button(label="뱅커", custom_id="뱅커", style=ButtonStyle.red)
                # draw = Button(label="무승부", custom_id="무승부", style=ButtonStyle.green)
                bet_embed = discord.Embed(title=f"{bkr_round}회차 배팅가능시간입니다.",
                                        description=f"플레이어, 뱅커, 또는 무승부에 배팅해주십시오.\n남은 배팅시간 : {ti}", color=0x2f3136)
                bet_embed.set_footer(text=서버이름)
                bet_msg = await bkr_ch.send(embed=bet_embed)
                for i in range(0, 12):
                    await asyncio.sleep(5)
                    ti -= 5
                    bet_embed = discord.Embed(title=f"{bkr_round}회차 배팅가능시간입니다.",
                                            description=f"플레이어, 뱅커, 또는 무승부에 배팅해주십시오.\n남은 배팅시간 : {ti}",
                                            color=0x2f3136)
                    bet_embed.set_footer(text=서버이름)
                    await bet_msg.delete()
                    bet_msg = await bkr_ch.send(embed=bet_embed)
                close_embed = discord.Embed(title=f"{bkr_round}회차 배팅이 마감되었습니다", description=f'''
🔵플레이어  ||  🔴뱅커

        {player_card}   |  {player_card2}   |  {p_add_card if p_add_card != 0 else ""}  //   {banker_card}   |  {banker_card2}   |  {b_add_card if b_add_card != 0 else ""}
🔵플레이어 : {p} {"✅" if p > b else ""}   {"< 승리! > X2배" if p > b else ""}\n
🔴뱅커 : {b}   {"✅" if p < b else ""}   {"< 승리! > X1.95배" if p < b else ""}\n
🟢무승부{"< 승리! > X9배" if p == b else ""}''', color=0x2f3136)
                await bet_msg.delete()
                bet_msg = await bkr_ch.send(embed=close_embed, components="")
                bet_log = ""
                result = "플레이어" if p > b else '뱅커' if b > p else '무승부'
                conn = sqlite3.connect('./database/database.db')
                c = conn.cursor()
                list_a = list(c.execute("SELECT * FROM users"))
                for i in list_a:
                    if (i[24] == None):
                        # print("none")
                        continue
                    conn = sqlite3.connect('./database/database.db')
                    c = conn.cursor()
                    if int(p) > int(b):
                        배당 = 2
                    elif int(b) > int(p):
                        배당 = 1.95
                    else:
                        배당 = 9

                    if i[24] == result:

                        bet_log += (f"**<@{i[0]}> {i[24]} {round(i[25] * 배당)} 적중**\n")
                        f = open(f"./bet_log/{i[0]}.txt", "a", encoding="utf-8-sig")
                        f.write(
                                f'''                
배팅게임 : 바카라
배팅회차 : {bkr_round}
배팅내역 : {i[24]}
배팅금 : {i[25]}
적중 / 미적중 : 적중
적중 금액 : {round(i[25] * 배당-1)}
남은 금액 : {i[1] + round(i[25] * 배당)}
======================
''')
                        f.close()
                        c.execute("UPDATE users SET money = money + ? where id=?", (round(i[25] * 배당), i[0],))
                    elif result == "무승부":
                        f = open(f"./bet_log/{i[0]}.txt", "a", encoding="utf-8-sig")
                        f.write(
                                f'''                
배팅게임 : 바카라
배팅회차 : {bkr_round}
배팅내역 : {i[24]}
배팅금 : {i[25]}
적중 / 미적중 : 무승부
적중 금액 : 0
남은 금액 : {i[1]+ round(i[25])}
======================
''')
                        f.close()
                        bet_log += (f"**<@{i[0]}> {i[24]} {round(i[25])} 무승부**\n")
                        c.execute("UPDATE users SET money = money + ? where id=?",
                                (round(i[25] * 1), i[0],))
                    else:
                        f = open(f"./bet_log/{i[0]}.txt", "a", encoding="utf-8-sig")
                        f.write(
                            f'''                
배팅게임 : 바카라
배팅회차 : {bkr_round}
배팅내역 : {i[24]}
배팅금 : {i[25]}
적중 / 미적중 : 미적중
남은 금액 : {i[1]}
======================
''')
                        f.close()

                        bet_log += (f"**<@{i[0]}> {i[24]} 미적중**\n")

                    c.execute("UPDATE users SET rotoladder_bet_pick = ? where id=?", (None, i[0],))
                    c.execute("UPDATE users SET rotoladder_bet_money = ? where id=?", (None, i[0],))
                    conn.commit()
                    conn.close()
                if result == "플레이어":
                    result = f"{result} 🔵"
                elif result == "뱅커":
                    result = f"{result} 🔴"
                else:
                    result = f"{result} 🟢"
                round_rs = f"\n\n`{bkr_round}회차` -- **{result}**"
                doing_bet2 = []
                oplog = ''
                ch = client.get_channel(바카라배팅내역)
                await ch.send(f"`{bkr_round}회차`\n\n{bet_log}")
                await rs_pe.send(f"{round_rs}")
                    
    if message.content.startswith('.바카라 '):
        #if bakara_on != 0:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if not user_info[5] == 3:
            if message.content.split(" ")[2] == "올인":
                if (int(user_info[1]) >= 1000):
                    amount = int(user_info[1])
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                try:
                    amount = int(message.content.split(" ")[2])
                except:
                    con.close()
                    await message.channel.send(embed=talmoembed("배팅실패", "**```금액은 정수만 배팅이 가능합니다.```**"))
                    return
            if not amount < 1000:
                if user_info[1] >= amount:
                    choice = message.content.split(" ")[1]
                    if choice == "플" or choice == "뱅" or choice == "무":
                        if not message.author.id in doing_bet2:
                            doing_bet2.append(message.author.id)
                            if user_info[1] >= 1000:

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                            (user_info[1] - int(amount), message.author.id))
                                if choice == "플":
                                    choice = "플레이어"
                                    bkr_total_p = bkr_total_p + int(amount)
                                elif choice == "뱅":
                                    choice = "뱅커"
                                    bkr_total_b = bkr_total_b + int(amount)
                                else:
                                    choice = "무승부"
                                cur.execute("UPDATE users SET rotoladder_bet_pick = ? WHERE id == ?;",
                                            (choice, message.author.id))
                                cur.execute("UPDATE users SET rotoladder_bet_money = ? WHERE id == ?;",
                                            (amount, message.author.id))
                                con.commit()
                                con.close()
                                await message.reply(
                                    f"**> {bkr_round}회차 {choice}에 배팅이 완료되었습니다.\n\n잔액 : {user_info[1] - amount}**")

                            else:
                                con.close()
                                await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```이미 배팅중입니다.```**"))
                    else:
                        con.close()
                        await message.channel.send("**```플/뱅/무 중에서만 배팅해주세요.```**")
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("배팅실패", "**```1000원이상부터 배팅이 가능합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))

#         if message.content == "!바카라":
#             if message.author.id in admin_id:
#                 rs_pe = client.get_channel(바카라회차)
#                 pe_rs = await rs_pe.send(f"`1회차`가 진행되고있습니다.")
#                 round_rs = ''
#                 leng = 0

#                 if bakara_on == 0:
#                     await message.channel.send(f"<#{바카라채널}> 에 게임이 시작됩니다.")
#                     bakara_on = 1
#                     bkr_round = 0
#                     while True:
#                         bkr_round += 1
#                         p_add_card = 0
#                         b_add_card = 0
#                         player_card = random.randint(1, 13)
#                         banker_card = random.randint(1, 13)
#                         p_1=""
#                         p_2 = ""
#                         p_3 = "None"
#                         b_1 = ""
#                         b_2 = ""
#                         b_3 = "None"
#                         bkr_p = []
#                         bkr_b = []
#                         bkr_p_p = []
#                         bkr_b_p = []
#                         bkr_d = []

#                         # 플레이어
#                         if player_card >= 10:
#                             picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                             person=random.choice(["K", "J", "Q", "10"])
#                             p_1=person+picture
#                             player_card=0
#                         elif player_card == 1:
#                             picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                             p_1="A"+picture
#                         else:
#                             picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                             p_1 = str(player_card) + picture

#                         # 뱅커

#                         if banker_card >= 10:
#                             picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                             person = random.choice(["K", "J", "Q", "10"])
#                             b_1 = person + picture
#                             banker_card = 0
#                         elif banker_card == 1:
#                             picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                             b_1="A"+picture
#                         else:
#                             picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                             b_1 = str(banker_card) + picture

#                         player_card2 = random.randint(1, 13)
#                         banker_card2 = random.randint(1, 13)
#                         # 플레이어
#                         if player_card2 >= 10:
#                             picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                             person = random.choice(["K", "J", "Q", "10"])
#                             p_2 = person + picture
#                             player_card2 = 0
#                         elif player_card2 == 1:
#                             picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                             p_2 = "A" + picture
#                         else:
#                             picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                             p_2 = str(player_card2) + picture

#                         # 뱅커

#                         if banker_card2 >= 10:
#                             picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                             person = random.choice(["K", "J", "Q", "10"])
#                             b_2 = person + picture
#                             banker_card2 = 0
#                         elif banker_card2 == 1:
#                             picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                             b_2 = "A" + picture
#                         else:
#                             picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                             b_2 = str(banker_card2) + picture

#                         rs_ch = 바카라유출픽
#                         p = (player_card + player_card2) % 10
#                         b = (banker_card + banker_card2) % 10
#                         if p <= 5:
#                             p_add_card = random.randint(1, 13)
#                             if p_add_card >= 10:
#                                 picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                                 person = random.choice(["K", "J", "Q", "10"])
#                                 p_3 = person + picture
#                                 p_add_card = 0
#                             elif p_add_card == 1:
#                                 picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                                 p_3 = "A" + picture
#                             else:
#                                 picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                                 p_3 = str(p_add_card) + picture
#                         p = (p + p_add_card) % 10
#                         if b == 4 or b == 5:
#                             if b < p:
#                                 b_add_card = random.randint(1, 13)
#                                 if b_add_card >= 10:
#                                     picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                                     person = random.choice(["K", "J", "Q", "10"])
#                                     b_3 = person + picture
#                                     b_add_card = 0
#                                 elif b_add_card == 1:
#                                     picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                                     b_3 = "A" + picture
#                                 else:
#                                     picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                                     b_3 = str(b_add_card) + picture
#                         elif b <= 5:
#                             b_add_card = random.randint(1, 13)
#                             if b_add_card >= 10:
#                                 picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                                 person = random.choice(["K", "J", "Q", "10"])
#                                 b_3 = person + picture
#                                 b_add_card = 0
#                             elif b_add_card == 1:
#                                 picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                                 b_3 = "A" + picture
#                             else:
#                                 picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                                 b_3 = str(b_add_card) + picture

#                         b = (b + b_add_card) % 10
#                         if p == b and p == 5:
#                             p_add_card = random.randint(1, 13)
#                             if p_add_card >= 10:
#                                 picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                                 person = random.choice(["K", "J", "Q", "10"])
#                                 p_3 = person + picture
#                                 p_add_card = 0
#                             elif p_add_card == 1:
#                                 picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                                 p_3 = "A" + picture
#                             else:
#                                 picture = random.choice(["_clo", "_hea", "_dia", "_spa"])
#                                 p_3 = str(p_add_card) + picture
#                             p = (p + p_add_card) % 10
#                         bkrpp(f"{bkr_round}회차\n플레이어" if p > b else f"{bkr_round}회차\n뱅커" if b > p else f"{bkr_round}회차\n무승부").execute()
#                         cardcount=random.randint(0, 11)
#                         if cardcount<=3:
#                             카드수=1
#                         elif cardcount<=6:
#                             카드수 = 2
#                         elif cardcount<=8:
#                             카드수 = 3
#                         elif cardcount<=10:
#                             카드수 = 4
#                         else:
#                             카드수 = 5
#                         cardelist=[]
#                         for i in range(카드수):
#                             bae = random.randint(1, 10)
#                             if bae <= 4:
#                                 bae = "X2"
#                             elif bae <= 7:
#                                 bae = "X3"
#                             elif bae <= 9:
#                                 bae = "X5"
#                             else:
#                                 bae = "X8"
#                             card=random.randint(1, 13)
#                             picture=random.choice(["clo", "hea", "dia", "spa"])
#                             if card==1:
#                                 tmp=f"<:A_{picture}:"
#                                 ori=f" A_{picture} {bae} ⚡"
#                                 f = open(f"./card.txt", "r", encoding="utf-8-sig")
#                                 s = f.read()
#                                 s=s.split("\n")
#                                 for i in s:
#                                     if tmp in i:
#                                         cardelist.append(i + ori)
#                                 f.close()
#                             elif card==11:
#                                 tmp = f"<:J_{picture}:"
#                                 ori = f" J_{picture} {bae} ⚡"
#                                 f = open(f"./card.txt", "r", encoding="utf-8-sig")
#                                 s = f.read()
#                                 s = s.split("\n")
#                                 for i in s:
#                                     if tmp in i:
#                                         cardelist.append(i + ori)
#                                 f.close()
#                             elif card==12:
#                                 tmp = f"<:Q_{picture}:"
#                                 ori = f" Q_{picture} {bae} ⚡"
#                                 f = open(f"./card.txt", "r", encoding="utf-8-sig")
#                                 s = f.read()
#                                 s = s.split("\n")
#                                 for i in s:
#                                     if tmp in i:
#                                         cardelist.append(i + ori)
#                                 f.close()
#                             elif card==13:
#                                 tmp = f"<:K_{picture}:"
#                                 ori = f" K_{picture} {bae} ⚡"
#                                 f = open(f"./card.txt", "r", encoding="utf-8-sig")
#                                 s = f.read()
#                                 s = s.split("\n")
#                                 for i in s:
#                                     if tmp in i:
#                                         cardelist.append(i + ori)
#                                 f.close()
#                             else:
#                                 tmp = f"<:{card}_{picture}:"
#                                 ori = f" {card}_{picture} {bae} ⚡"
#                                 f = open(f"./card.txt", "r", encoding="utf-8-sig")
#                                 s = f.read()
#                                 s = s.split("\n")
#                                 for i in s:
#                                     if tmp in i:
#                                         cardelist.append(i + ori)
#                                 f.close()
#                         pp_11 = p_1.split("_")[0]
#                         pp_22 = p_2.split("_")[0]
#                         bb_11 = b_1.split("_")[0]
#                         bb_22 = b_2.split("_")[0]
#                         if pp_11== pp_22:
#                             p_pea = 1
#                         else:
#                             p_pea=0
#                         if bb_11 == bb_22:
#                             b_pea = 1
#                         else:
#                             b_pea = 0
#                         await client.get_channel(rs_ch).send(
#                             f"{bkr_round}회차\n플레이어" if p > b else f"{bkr_round}회차\n뱅커" if b > p else f"{bkr_round}회차\n무승부")
#                         await client.get_channel(rs_ch).send(cardelist)
#                         ti = 60
#                         bkr_ch = client.get_channel(바카라채널)
#                         bet_embed = discord.Embed(title=f"⚡ {bkr_round}회차 배팅가능시간입니다. ⚡",
#                                                 description=f"**> 플레이어, 뱅커, 또는 무승부에 `배팅`해주십시오.\n> \n> 플페(플레이어페어), 뱅페(뱅커페어)에도 `배팅`가능하십니다.\n\n> 남은 배팅시간 : `{ti}`**",
#                                                 color=0x2f3136)
#                         bet_embed.set_footer(text="수수료 20%")
#                         bet_msg = await bkr_ch.send(embed=bet_embed)
#                         플배당 = 1
#                         뱅배당 = 1
#                         무배당 = 0
#                         for i in cardelist:
#                             if p_1 in str(i):
#                                 bae = i.split(" ")[2]
#                                 bae = bae.replace("⚡", "")
#                                 bae = bae.replace(" ", "")
#                                 p_1=f"{p_1} ⚡ {bae}"
#                                 await client.get_channel(rs_ch).send(f"{i}, {bae}만큼을 더했습니다.")
#                                 bae=bae.replace("X", "")
#                                 플배당=플배당*int(bae)
#                             if p_2 in str(i):
#                                 bae = i.split(" ")[2]
#                                 bae = bae.replace("⚡", "")
#                                 bae = bae.replace(" ", "")
#                                 p_2=f"{p_2} ⚡ {bae}"
#                                 await client.get_channel(rs_ch).send(f"{i}, {bae}만큼을 더했습니다.")
#                                 bae=bae.replace("X", "")
#                                 플배당=플배당*int(bae)
#                             if str(p_3) in str(i):
#                                 bae = i.split(" ")[2]
#                                 bae = bae.replace("⚡", "")
#                                 bae = bae.replace(" ", "")
#                                 p_3=f"{p_3} ⚡ {bae}"
#                                 await client.get_channel(rs_ch).send(f"{i}, {bae}만큼을 더했습니다.")
#                                 bae=bae.replace("X", "")
#                                 플배당=플배당*int(bae)
#                             #뱅커
#                             if b_1 in str(i):
#                                 bae = i.split(" ")[2]
#                                 bae = bae.replace("⚡", "")
#                                 bae = bae.replace(" ", "")
#                                 b_1=f"{b_1} ⚡ {bae}"
#                                 await client.get_channel(rs_ch).send(f"{i}, {bae}만큼을 더했습니다.")
#                                 bae=bae.replace("X", "")
#                                 뱅배당=뱅배당*int(bae)
#                             if b_2 in str(i):
#                                 bae = i.split(" ")[2]
#                                 bae = bae.replace("⚡", "")
#                                 bae = bae.replace(" ", "")
#                                 b_2=f"{b_2} ⚡ {bae}"
#                                 await client.get_channel(rs_ch).send(f"{i}, {bae}만큼을 더했습니다.")
#                                 bae=bae.replace("X", "")
#                                 뱅배당=뱅배당*int(bae)
#                             if str(b_3) in str(i):
#                                 bae = i.split(" ")[2]
#                                 bae = bae.replace("⚡", "")
#                                 bae = bae.replace(" ", "")
#                                 b_3=f"{b_3} ⚡ {bae}"
#                                 await client.get_channel(rs_ch).send(f"{i}, {bae}만큼을 더했습니다.")
#                                 bae=bae.replace("X", "")
#                                 뱅배당=뱅배당*int(bae)
#                         if p==b:
#                             무배당=뱅배당*플배당

#                         for i in range(0, 12):
#                             await asyncio.sleep(5)
#                             ti -= 5
#                             bet_embed = discord.Embed(title=f"⚡ {bkr_round}회차 배팅가능시간입니다. ⚡",
#                                                     description=f"**> 플레이어, 뱅커, 또는 무승부에 `배팅`해주십시오.\n> \n> 플페(플레이어페어), 뱅페(뱅커페어)에도 `배팅`가능하십니다.\n\n> 남은 배팅시간 : `{ti}`**",
#                                                     color=0x2f3136)
#                             bet_embed.set_footer(text="수수료 20%")
#                             await bet_msg.edit(embed=bet_embed)
#                         ct=0

#                         while True:
#                             # try:
#                                 ct+=1
#                                 close_embed = discord.Embed(title=f"{bkr_round}회차 배팅이 마감되었습니다", description=f'''
#         ⚡ `Lightning Card` ⚡
#         `ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ`
#         {cardelist[0]} {", "+cardelist[1] if 카드수>=2 else ""} {", "+cardelist[2] if 카드수>=3 else ""} {", "+cardelist[3] if 카드수>=4 else ""} {", "+cardelist[4] if 카드수==5 else ""}
#         `ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ`
#         ```
# 🔵플레이어  ||  🔴뱅커

# {p_1} {",  "+str(p_2) if ct >= 3 else ""} {",  "+str(p_3)  if ct >= 5 and  p_add_card != 0 else ""}  //   {b_1 if ct >= 2 else ""} {",  "+str(b_2) if ct >= 4 else ""} {",  "+str(b_3) if ct >= 6 and  b_add_card != 0 else ""}
#         ```
#             ```
# 🔵플레이어 : {p if ct==6 else ""} {"✅" if p > b and ct==6 else ""}   {f"< 승리! > X{플배당+1}배" if p > b and ct==6 else ""}\n
# 🔵페어 : {"✅" if ct==6 and  pp_11== pp_22 else ""} {f"< 승리! > X{플배당*9}배" if ct==6 and pp_11== pp_22 else ""}\n
# 🔴뱅커 : {b if ct==6 else ""}   {"✅" if p < b and ct==6 else ""}   {f"< 승리! > X{뱅배당+0.95}배" if p < b and ct==6 else ""}\n
# 🔴페어 : {"✅" if ct==6 and bb_11== bb_22 else ""} {f"< 승리! > X{뱅배당*9}배" if ct==6 and bb_11== bb_22 else ""}\n
# 🟢무승부{f"< 승리! > X{무배당+4}배" if p == b and ct==6 else ""}```''', color=0x2f3136)
#                                 close_embed.set_footer(text="수수료 20%")
#                                 await bet_msg.edit(embed=close_embed)
#                                 await asyncio.sleep(1)
#                                 if ct==6:
#                                     break
#                             # except:
#                             #     pass
#                         result = "플레이어" if p > b else '뱅커' if b > p else '무승부'

#                         conn = sqlite3.connect('./database/database.db')
#                         c = conn.cursor()
#                         text=""
#                         if result == "플레이어":
#                             for i in bkr_p:
#                                 con = sqlite3.connect("./database/database.db")
#                                 cur = con.cursor()
#                                 cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
#                                 user_info = cur.fetchone()
#                                 user = client.get_user(i)
#                                 new_money = int(f'{(user_info[31] * (플배당+1)):.0f}')
#                                 text += f"`{user}: 플레이어에 {user_info[31]}원 -> {new_money}원 (적중)`\n"
#                                 cur.execute("UPDATE users SET money = ? WHERE id == ?;",
#                                             (user_info[1] + new_money, i))
#                                 cur.execute("UPDATE users SET bkr_p_bet_pick = ? where id=?", (None, i,))
#                                 cur.execute("UPDATE users SET bkr_p_bet_money = ? where id=?", (None, i,))
#                                 con.commit()
#                                 con.close()
#                             for i in bkr_b:
#                                 con = sqlite3.connect("./database/database.db")
#                                 cur = con.cursor()
#                                 cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
#                                 user_info = cur.fetchone()
#                                 user = client.get_user(i)
#                                 new_money = 0
#                                 text += f"`{user}: 뱅커에 {user_info[35]}원 -> {new_money}원 (미적중)`\n"
#                                 cur.execute("UPDATE users SET bkr_b_bet_pick = ? where id=?", (None, i,))
#                                 cur.execute("UPDATE users SET bkr_b_bet_money = ? where id=?", (None, i,))
#                                 con.commit()
#                                 con.close()
#                             for i in bkr_d:
#                                 con = sqlite3.connect("./database/database.db")
#                                 cur = con.cursor()
#                                 cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
#                                 user_info = cur.fetchone()
#                                 user = client.get_user(i)
#                                 new_money = 0
#                                 text += f"`{user}: 무승부에 {user_info[39]}원 -> {new_money}원 (미적중)`\n"
#                                 cur.execute("UPDATE users SET bkr_d_bet_pick = ? where id=?", (None, i,))
#                                 cur.execute("UPDATE users SET bkr_d_bet_money = ? where id=?", (None, i,))
#                                 con.commit()
#                                 con.close()
#                         elif result == "뱅커":
#                             for i in bkr_p:
#                                 con = sqlite3.connect("./database/database.db")
#                                 cur = con.cursor()
#                                 cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
#                                 user_info = cur.fetchone()
#                                 user = client.get_user(i)
#                                 new_money = 0
#                                 text += f"`{user}: 플레이어에 {user_info[31]}원 -> {new_money}원 (미적중)`\n"
#                                 cur.execute("UPDATE users SET bkr_p_bet_pick = ? where id=?", (None, i,))
#                                 cur.execute("UPDATE users SET bkr_p_bet_money = ? where id=?", (None, i,))
#                                 con.commit()
#                                 con.close()
#                             for i in bkr_b:
#                                 con = sqlite3.connect("./database/database.db")
#                                 cur = con.cursor()
#                                 cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
#                                 user_info = cur.fetchone()
#                                 user = client.get_user(i)
#                                 new_money = int(f'{(user_info[35] * (뱅배당+0.95)):.0f}')
#                                 text += f"`{user}: 뱅커에 {user_info[35]}원 -> {new_money}원 (적중)`\n"
#                                 cur.execute("UPDATE users SET money = ? WHERE id == ?;",
#                                             (user_info[1] + new_money, i))
#                                 cur.execute("UPDATE users SET bkr_b_bet_pick = ? where id=?", (None, i,))
#                                 cur.execute("UPDATE users SET bkr_b_bet_money = ? where id=?", (None, i,))
#                                 con.commit()
#                                 con.close()
#                             for i in bkr_d:
#                                 con = sqlite3.connect("./database/database.db")
#                                 cur = con.cursor()
#                                 cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
#                                 user_info = cur.fetchone()
#                                 user = client.get_user(i)
#                                 new_money = 0
#                                 text += f"`{user}: 무승부에 {user_info[39]}원 -> {new_money}원 (미적중)`\n"
#                                 cur.execute("UPDATE users SET bkr_d_bet_pick = ? where id=?", (None, i,))
#                                 cur.execute("UPDATE users SET bkr_d_bet_money = ? where id=?", (None, i,))
#                                 con.commit()
#                                 con.close()
#                         else:
#                             for i in bkr_p:
#                                 con = sqlite3.connect("./database/database.db")
#                                 cur = con.cursor()
#                                 cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
#                                 user_info = cur.fetchone()
#                                 user = client.get_user(i)
#                                 new_money = user_info[31]
#                                 text += f"`{user}: 플레이어에 {user_info[31]}원 -> {new_money}원 (무승부)`\n"
#                                 cur.execute("UPDATE users SET money = ? WHERE id == ?;",
#                                             (user_info[1] + new_money, i))
#                                 cur.execute("UPDATE users SET bkr_p_bet_pick = ? where id=?", (None, i,))
#                                 cur.execute("UPDATE users SET bkr_p_bet_money = ? where id=?", (None, i,))
#                                 con.commit()
#                                 con.close()
#                             for i in bkr_b:
#                                 con = sqlite3.connect("./database/database.db")
#                                 cur = con.cursor()
#                                 cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
#                                 user_info = cur.fetchone()
#                                 user = client.get_user(i)
#                                 new_money =user_info[35]
#                                 text += f"`{user}: 뱅커에 {user_info[35]}원 -> {new_money}원 (무승부)`\n"
#                                 cur.execute("UPDATE users SET money = ? WHERE id == ?;",
#                                             (user_info[1]+new_money, i))
#                                 cur.execute("UPDATE users SET bkr_b_bet_pick = ? where id=?", (None, i,))
#                                 cur.execute("UPDATE users SET bkr_b_bet_money = ? where id=?", (None, i,))
#                                 con.commit()
#                                 con.close()
#                             for i in bkr_d:
#                                 con = sqlite3.connect("./database/database.db")
#                                 cur = con.cursor()
#                                 cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
#                                 user_info = cur.fetchone()
#                                 user = client.get_user(i)
#                                 new_money = int(f'{(user_info[39] * (무배당 + 4)):.0f}')
#                                 text += f"`{user}: 무승부에 {user_info[37]}원 -> {new_money}원 (적중)`\n"
#                                 cur.execute("UPDATE users SET money = ? WHERE id == ?;",
#                                             (user_info[1] + new_money, i))
#                                 cur.execute("UPDATE users SET bkr_d_bet_pick = ? where id=?", (None, i,))
#                                 cur.execute("UPDATE users SET bkr_d_bet_money = ? where id=?", (None, i,))
#                                 con.commit()
#                                 con.close()
#                         if p_pea==1:
#                             for i in bkr_p_p:
#                                 con = sqlite3.connect("./database/database.db")
#                                 cur = con.cursor()
#                                 cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
#                                 user_info = cur.fetchone()
#                                 user = client.get_user(i)
#                                 new_money = int(f'{(user_info[33] * 플배당*9):.0f}')
#                                 text += f"`{user}: 플레이어페어에 {user_info[33]}원 -> {new_money}원 (적중)`\n"
#                                 cur.execute("UPDATE users SET money = ? WHERE id == ?;",
#                                             (user_info[1] + new_money, i))
#                                 cur.execute("UPDATE users SET bkr_p_p_bet_pick = ? where id=?", (None, i,))
#                                 cur.execute("UPDATE users SET bkr_p_p_bet_money = ? where id=?", (None, i,))
#                                 con.commit()
#                                 con.close()
#                         else:
#                             for i in bkr_p_p:
#                                 con = sqlite3.connect("./database/database.db")
#                                 cur = con.cursor()
#                                 cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
#                                 user_info = cur.fetchone()
#                                 user = client.get_user(i)
#                                 new_money = 0
#                                 text += f"`{user}: 플레이어페어에 {user_info[33]}원 -> {new_money}원 (미적중)`\n"
#                                 cur.execute("UPDATE users SET bkr_p_p_bet_pick = ? where id=?", (None, i,))
#                                 cur.execute("UPDATE users SET bkr_p_p_bet_money = ? where id=?", (None, i,))
#                                 con.commit()
#                                 con.close()
#                         if b_pea==1:
#                             for i in bkr_b_p:
#                                 con = sqlite3.connect("./database/database.db")
#                                 cur = con.cursor()
#                                 cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
#                                 user_info = cur.fetchone()
#                                 user = client.get_user(i)
#                                 new_money = int(f'{(user_info[37] * 뱅배당*9):.0f}')
#                                 text += f"`{user}: 뱅커페어에 {user_info[37]}원 -> {new_money}원 (적중)`\n"
#                                 cur.execute("UPDATE users SET money = ? WHERE id == ?;",
#                                             (user_info[1] + new_money, i))
#                                 cur.execute("UPDATE users SET bkr_b_p_bet_pick = ? where id=?", (None, i,))
#                                 cur.execute("UPDATE users SET bkr_b_p_bet_money = ? where id=?", (None, i,))
#                                 con.commit()
#                                 con.close()
#                         else:
#                             for i in bkr_b_p:
#                                 con = sqlite3.connect("./database/database.db")
#                                 cur = con.cursor()
#                                 cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
#                                 user_info = cur.fetchone()
#                                 user = client.get_user(i)
#                                 new_money = 0
#                                 text += f"`{user}: 뱅커페어에 {user_info[37]}원 -> {new_money}원 (미적중)`\n"
#                                 cur.execute("UPDATE users SET bkr_b_p_bet_pick = ? where id=?", (None, i,))
#                                 cur.execute("UPDATE users SET bkr_b_p_bet_money = ? where id=?", (None, i,))
#                                 con.commit()
#                                 con.close()
#                         if result == "플레이어":
#                             result = f"{result} 🔵"
#                             if 플배당>1:
#                                 result = f"플레이어 🔵 ⚡⚡"
#                         elif result == "뱅커":
#                             result = f"{result} 🔴"
#                             if 뱅배당>1:
#                                 result = f"뱅커 🔴 ⚡⚡"
#                         else:
#                             result = f"{result} 🟢"
#                             if 무배당>4:
#                                 result = f"무승부 🟢 ⚡⚡"
#                         leng += 1
#                         if leng >= 50:
#                             round_rs = "**🎨결과값 초기화🎨**"
#                             leng = 0
#                         round_rs += f"\n\n`{bkr_round}회차` -- **{result}**"
#                         ch = client.get_channel(바카라배팅내역)
#                         await ch.send(f"`{bkr_round}회차`\n\n{text}")
#                         await pe_rs.edit(f"{round_rs}")
#         if message.content.startswith('.바카라 '):
#             if bakara_on != 0:
#                 con = sqlite3.connect("./database/database.db")
#                 cur = con.cursor()
#                 cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
#                 user_info = cur.fetchone()
#                 amount = int(message.content.split(" ")[2])
#                 if not user_info[5] == 3:
#                     if not amount < 1000:
#                         if user_info[1] >= amount+amount*0.2:
#                             choice = message.content.split(" ")[1]
#                             if choice == "플" or choice == "뱅" or choice == "무" or choice == "플페" or choice == "뱅페":
#                                 if user_info[1] >= 1000:
#                                     if ti > 10:
#                                         cur.execute("UPDATE users SET money = ? WHERE id == ?;",
#                                                     (user_info[1] -  round(int(amount+amount*0.2)), message.author.id))
#                                         if choice == "플":
#                                             bkr_p.append(message.author.id)
#                                             choice = "플레이어"
#                                             cur.execute("UPDATE users SET bkr_p_bet_pick = ? WHERE id == ?;",
#                                                         (choice, message.author.id))
#                                             cur.execute("UPDATE users SET bkr_p_bet_money = ? WHERE id == ?;",
#                                                         (amount, message.author.id))
#                                         elif choice == "뱅":
#                                             bkr_b.append(message.author.id)
#                                             choice = "뱅커"
#                                             cur.execute("UPDATE users SET bkr_b_bet_pick = ? WHERE id == ?;",
#                                                         (choice, message.author.id))
#                                             cur.execute("UPDATE users SET bkr_b_bet_money = ? WHERE id == ?;",
#                                                         (amount, message.author.id))
#                                         elif choice == "무":
#                                             bkr_d.append(message.author.id)
#                                             choice = "무승부"
#                                             cur.execute("UPDATE users SET bkr_d_bet_pick = ? WHERE id == ?;",
#                                                         (choice, message.author.id))
#                                             cur.execute("UPDATE users SET bkr_d_bet_money = ? WHERE id == ?;",
#                                                         (amount, message.author.id))
#                                         elif choice == "플페":
#                                             bkr_p_p.append(message.author.id)
#                                             choice = "플레이어페어"
#                                             cur.execute("UPDATE users SET bkr_p_p_bet_pick = ? WHERE id == ?;",
#                                                         (choice, message.author.id))
#                                             cur.execute("UPDATE users SET bkr_p_p_bet_money = ? WHERE id == ?;",
#                                                         (amount, message.author.id))
#                                         elif choice == "뱅페":
#                                             bkr_b_p.append(message.author.id)
#                                             choice = "뱅커페어"
#                                             cur.execute("UPDATE users SET bkr_b_p_bet_pick = ? WHERE id == ?;",
#                                                         (choice, message.author.id))
#                                             cur.execute("UPDATE users SET bkr_b_p_bet_money = ? WHERE id == ?;",
#                                                         (amount, message.author.id))
#                                         con.commit()
#                                         con.close()
#                                         await message.reply(
#                                             f"**> {bkr_round}회차 {choice}에 {round(int(amount+amount*0.2))}원 배팅이 완료되었습니다.\n\n잔액 : {user_info[1] - round(int(amount+amount*0.2))}**")
#                                     else:
#                                         con.close()
#                                         await message.channel.send(embed=talmoembed("배팅실패", "**```배팅이 마감되었습니다.```**"))
#                                 else:
#                                     con.close()
#                                     await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
#                             else:
#                                 con.close()
#                                 await message.channel.send("**```플/뱅/무/플페/뱅페 중에서만 배팅해주세요.```**")
#                         else:
#                             con.close()
#                             await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족하거나 수수료를 지불할 보유금이 부족합니다.```**"))
#                     else:
#                         con.close()
#                         await message.channel.send(embed=talmoembed("배팅실패", "**```1000원이상부터 배팅이 가능합니다.```**"))
#                 else:
#                     con.close()
#                     await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))
#             else:
#                 await message.channel.send(embed=talmoembed("배팅실패", "**```게임이 진행되고있지않습니다.```**"))
    if message.content.startswith('.코인 '):
        # if coin_on != 0:
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if not user_info[5] == 3:
            if message.content.split(" ")[1] == "올인":
                if (int(user_info[1]) >= 1000):
                    amount = int(user_info[1])
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                try:
                    amount = int(message.content.split(" ")[1])
                except:
                    con.close()
                    await message.channel.send(embed=talmoembed("배팅실패", "**```금액은 정수만 배팅이 가능합니다.```**"))
                    return
            if not amount < 1000:
                if user_info[1] >= amount:
                    if not message.author.id in doing_bet3:
                        doing_bet3.append(message.author.id)
                        if user_info[1] >= 1000:
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] - int(amount), message.author.id))
                            con.commit()
                            cur.execute("UPDATE users SET coin_bet_money = ? WHERE id == ?;",
                                        (amount, message.author.id))
                            con.commit()
                            cur.execute("UPDATE users SET perc = ? WHERE id == ?;",
                                        (random.randint(-100, 100), message.author.id))
                            con.commit()
                            con.close()
                            await message.reply(f"**> {amount} 매수가 완료되었습니다.\n\n잔액 : {user_info[1] - amount}**")

                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
                    else:
                        con.close()
                        await message.channel.send("**```이미 매수중입니다.```**")
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send("**```1000원이상부터 매수가 가능합니다.```**")
        else:
            con.close()
            await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))
    #else:
        #await message.channel.send(embed=talmoembed("배팅실패", "**```게임이 진행되고있지않습니다.```**"))

    if message.content.startswith('.돈빼기'):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if not user_info[5] == 3:
            await message.reply(
                f"> `{user_info[-2]}`원을 성공적으로 회수하였습니다.\n> \n> {user_info[1]}원 -> {user_info[1] + user_info[-2]}원")
            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                        (user_info[1] + user_info[-2], message.author.id))
            con.commit()
            cur.execute("UPDATE users SET coin_bet_money = ? WHERE id == ?;",
                        (0, message.author.id))
            con.commit()
            con.close()
            doing_bet3.remove(message.author.id)
        else:
            con.close()
            await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))

        if message.content == "!경마":
            if message.author.id in admin_id:
                rs_pe = client.get_channel(경마회차)
                # pe_rs = await rs_pe.send(f"`1회차`가 진행되고있습니다.")
                round_rs = ''
                # leng = 0
                # bet_msg = await client.get_channel(경마채널).send(f"start")
                #if km_on == 0:
                await message.channel.send(f"<#{경마채널}> 에 게임이 시작됩니다.")
                km_on = 1
                km_round = 0
                while True:
                    h1_op_on = 0
                    h2_op_on = 0
                    h3_op_on = 0
                    h4_op_on = 0
                    og1 = 60
                    og2 = 60
                    og3 = 60
                    og4 = 60
                    km_round += 1
                    ttii = 60
                    horse_1 = ' ' * og1
                    horse_2 = ' ' * og2
                    horse_3 = ' ' * og3
                    horse_4 = ' ' * og4
                    bet_embed = f'''
{km_round}회차 배팅가능시간입니다. **배당 X3.95**

잘 달릴것같은 말에 배팅해주세요.

**
🏁{horse_1}🏇 ( 1 )
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
🏁{horse_2}🏇 ( 2 )
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
🏁{horse_3}🏇 ( 3 )
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
🏁{horse_4}🏇 ( 4 )
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
남은시간 : {ttii}
**'''
                    bet_msg = await client.get_channel(경마채널).send(bet_embed)
                    for i in range(0, 12):
                        await asyncio.sleep(5)
                        ttii -= 5
                        bet_embed = f'''
{km_round}회차 배팅가능시간입니다. **배당 X3.95**

잘 달릴것같은 말에 배팅해주세요.

**
🏁{horse_1}🏇 ( 1 )
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
🏁{horse_2}🏇 ( 2 )
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
🏁{horse_3}🏇 ( 3 )
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
🏁{horse_4}🏇 ( 4 )
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
남은시간 : {ttii}
**'''
                        await bet_msg.delete()
                        bet_msg = await client.get_channel(경마채널).send(bet_embed)
                        if ttii == 0:
                            break

                    while True:
                        await asyncio.sleep(1)
                        if h1_op_on != 1:
                            h1_go = random.randint(0, 1)
                        if h2_op_on != 1:
                            h2_go = random.randint(0, 1)
                        if h3_op_on != 1:
                            h3_go = random.randint(0, 1)
                        if h4_op_on != 1:
                            h4_go = random.randint(0, 1)

                        if h1_go == 1:
                            og1 -= 4
                        if h2_go == 1:
                            og2 -= 4
                        if h3_go == 1:
                            og3 -= 4
                        if h4_go == 1:
                            og4 -= 4
                        horse_1 = ' ' * og1
                        horse_2 = ' ' * og2
                        horse_3 = ' ' * og3
                        horse_4 = ' ' * og4
                        bet_embed = f'''
{km_round}회차 배팅가능시간입니다. **배당 X3.95**

잘 달릴것같은 말에 배팅해주세요.

**
🏁{horse_1}🏇 ( 1 )
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
🏁{horse_2}🏇 ( 2 )
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
🏁{horse_3}🏇 ( 3 )
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
🏁{horse_4}🏇 ( 4 )
ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
**'''
                        await bet_msg.edit(bet_embed)

                        if og1 == 0:
                            if not (og1 == og2 or og1 == og3 or og1 == og4):
                                km_result = "1"
                            else:
                                km_result = '무승부'
                            break
                        elif og2 == 0:
                            if not (og2 == og1 or og2 == og3 or og2 == og4):
                                km_result = "2"
                            else:
                                km_result = '무승부'
                            break
                        elif og3 == 0:
                            if not (og3 == og2 or og3 == og1 or og3 == og4):
                                km_result = "3"
                            else:
                                km_result = '무승부'
                            break
                        elif og4 == 0:
                            if not (og4 == og2 or og4 == og1 or og4 == og3):
                                km_result = "4"
                            else:
                                km_result = '무승부'
                            break
                    bet_log = ""
                    conn = sqlite3.connect('./database/database.db')
                    c = conn.cursor()
                    list_a = list(c.execute("SELECT * FROM users"))
                    for i in list_a:
                        if (i[20] == None):
                            # print("none")
                            continue
                        conn = sqlite3.connect('./database/database.db')
                        c = conn.cursor()
                        배당 = 3.95

                        if i[20] == km_result:

                            bet_log += (f"**<@{i[0]}> {i[20]}번 {round(i[21] * 배당)} 적중**\n")
                            f = open(f"./bet_log/{i[0]}.txt", "a", encoding="utf-8-sig")
                            f.write(
                                f'''                
배팅게임 : 경마
배팅회차 : {km_round}
배팅내역 : {i[20]}
배팅금 : {i[21]}
적중 / 미적중 : 적중
적중 금액 : {round(i[21] * 배당-1)}
남은 금액 : {i[1] + round(i[21] * 배당)}
======================
''')
                            f.close()
                            c.execute("UPDATE users SET money = money + ? where id=?", (round(i[21] * 배당), i[0],))
                        elif km_result == '무승부':
                            f = open(f"./bet_log/{i[0]}.txt", "a", encoding="utf-8-sig")
                            f.write(
                                f'''                
배팅게임 : 경마
배팅회차 : {km_round}
배팅내역 : {i[20]}
배팅금 : {i[21]}
적중 / 미적중 : 무승부
적중 금액 : 0
남은 금액 : {i[1] + round(i[21])}
======================
''')
                            f.close()
                            bet_log += (f"**<@{i[0]}> {i[20]}번 {i[21]}원 무승부**\n")
                            c.execute("UPDATE users SET money = money + ? where id=?",
                                    (round(i[21] * 1), i[0],))
                        else:
                            f = open(f"./bet_log/{i[0]}.txt", "a", encoding="utf-8-sig")
                            f.write(
                                f'''                
배팅게임 : 경마
배팅회차 : {km_round}
배팅내역 : {i[20]}
배팅금 : {i[21]}
적중 / 미적중 : 미적중
남은 금액 : {i[1]}
======================
''')
                            f.close()

                            bet_log += (f"**<@{i[0]}> {i[20]}번 {i[21]}원 미적중**\n")

                        c.execute("UPDATE users SET ad_bet_pick = ? where id=?", (None, i[0],))
                        c.execute("UPDATE users SET ad_bet_money = ? where id=?", (None, i[0],))
                        conn.commit()
                        conn.close()
                    doing_bet5 = []
                    if km_result == "1":
                        km_result = f"🏇 :one: "
                    elif km_result == "2":
                        km_result = f"🏇 :two: "
                    elif km_result == "3":
                        km_result = f"🏇 :three: "
                    elif km_result == "4":
                        km_result = f"🏇 :four:"
                    else:
                        km_result = "`무승부` ‼‼‼‼"
                    round_rs += f"\n\n`{km_round}회차` -- **{km_result}**"
                    ch = client.get_channel(경마배팅내역)
                    await ch.send(f"`{km_round}회차`\n\n{bet_log}")
                    await rs_pe.send(f"{round_rs}")
                    await bet_msg.delete()

        if message.content.startswith('.경마 '):
            if km_on != 0:
                con = sqlite3.connect("./database/database.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                user_info = cur.fetchone()
                if not user_info[5] == 3:
                    if message.content.split(" ")[2] == "올인":
                        if (int(user_info[1]) >= 1000):
                            amount = int(user_info[1])
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
                    else:
                        try:
                            amount = int(message.content.split(" ")[2])
                        except:
                            con.close()
                            await message.channel.send(embed=talmoembed("배팅실패", "**```금액은 정수만 배팅이 가능합니다.```**"))
                            return
                    if not amount < 1000:
                        if user_info[1] >= amount:
                            if ttii > 10:
                                choice = message.content.split(" ")[1]
                                if user_info[1] >= 1000:
                                    if not message.author.id in doing_bet5:
                                        doing_bet5.append(message.author.id)
                                        if choice == "1":
                                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                        (user_info[1] - amount, message.author.id))
                                            cur.execute("UPDATE users SET ad_bet_pick = ? WHERE id == ?;",
                                                        (choice, message.author.id))
                                            cur.execute("UPDATE users SET ad_bet_money = ? WHERE id == ?;",
                                                        (amount, message.author.id))
                                            con.commit()
                                            con.close()
                                            await message.channel.send(
                                                f"**> {km_round}회차 {choice}번에 배팅이 완료되었습니다.\n\n잔액 : {user_info[1] - amount}**")
                                        elif choice == "2":
                                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                        (user_info[1] - amount, message.author.id))
                                            cur.execute("UPDATE users SET ad_bet_pick = ? WHERE id == ?;",
                                                        (choice, message.author.id))
                                            cur.execute("UPDATE users SET ad_bet_money = ? WHERE id == ?;",
                                                        (amount, message.author.id))
                                            con.commit()
                                            con.close()
                                            await message.channel.send(
                                                f"**> {km_round}회차 {choice}번에 배팅이 완료되었습니다.\n\n잔액 : {user_info[1] - amount}**")
                                        elif choice == "3":
                                            hz_z.append(message.author.id)
                                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                        (user_info[1] - amount, message.author.id))
                                            cur.execute("UPDATE users SET ad_bet_pick = ? WHERE id == ?;",
                                                        (choice, message.author.id))
                                            cur.execute("UPDATE users SET ad_bet_money = ? WHERE id == ?;",
                                                        (amount, message.author.id))
                                            con.commit()
                                            con.close()
                                            await message.channel.send(
                                                f"**> {km_round}회차 {choice}번에 배팅이 완료되었습니다.\n\n잔액 : {user_info[1] - amount}**")
                                        elif choice == "4":
                                            hz_z.append(message.author.id)
                                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                        (user_info[1] - amount, message.author.id))
                                            cur.execute("UPDATE users SET ad_bet_pick = ? WHERE id == ?;",
                                                        (choice, message.author.id))
                                            cur.execute("UPDATE users SET ad_bet_money = ? WHERE id == ?;",
                                                        (amount, message.author.id))
                                            con.commit()
                                            con.close()
                                            await message.channel.send(
                                                f"**> {km_round}회차 {choice}번에 배팅이 완료되었습니다.\n\n잔액 : {user_info[1] - amount}**")
                                        else:
                                            con.close()
                                            await message.channel.send("**```1/2/3/4 중에서만 배팅해주세요.```**")
                                    else:
                                        con.close()
                                        await message.channel.send(embed=talmoembed("배팅실패", "**```이미 배팅중입니다.```**"))
                                else:
                                    con.close()
                                    await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))

                            else:
                                con.close()
                                await message.channel.send(embed=talmoembed("배팅실패", "**```배팅이 마감되었습니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("보유금액부족", "**```보유 금액이 부족합니다.```**"))
                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("배팅실패", "**```1000원이상부터 배팅이 가능합니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=talmoembed("배팅실패", "**```졸업되거나 차단된 유저십니다.```**"))
#             else:
#                 await message.channel.send(embed=talmoembed("배팅실패", "**```게임이 진행되고있지않습니다.```**"))


@client.event
async def on_button_click(interaction):
    global doing_bet
    global ktotal
    global mtotal
    global bkr_p
    global bkr_b
    global bkr_d
    global 충전중
    global doing_bet2
    global p
    global b
    global p_add_card
    global b_add_card
    global player_card
    global banker_card
    global player_card2
    global banker_card2
    global bkr_round
    global bakara_on
    global bkr_total_p
    global bkr_total_b
    global doing_bet3
    
    global dt_round
    global dt_total_d
    global dt_total_t
    global doing_bet3
    global d_card
    global t_card
    global dt_on

    con = sqlite3.connect("./database/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
    user_info = cur.fetchone()

    if (user_info == None):
        cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
            interaction.user.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
            None,
            None, None, None, None, None, None, None, None, None, None, None, None, None, None))
        con.commit()
        con.close()
    con.close()
    if interaction.component.custom_id == "문상충전":
        if 충전중 == 0:
            충전중 = 1
            user_id = interaction.user.id
            print(interaction.user.name)

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()
            if not int(user_info[5]) >= 3:

                if not (user_info == None):
                    try:
                        await client.get_user(user_id).send("**```문화상품권 핀번호를 `-`를 포함해서 입력해주세요!```**")
                        await interaction.respond(content="**```DM을 확인해주세요```**")
                    except:
                        await interaction.respond(content="**```DM이 막혀있습니다```**")
                        충전중 = 0
                        print("충전끝")

                    def check(msg):
                        return (isinstance(msg.channel, discord.channel.DMChannel) and (
                                len(msg.content) == 21 or len(msg.content) == 19))

                    try:
                        munsang_pin = await client.wait_for("message", timeout=60, check=check)
                    except asyncio.TimeoutError:
                        try:
                            await client.get_user(user_id).send("**```\n시간이 초과되었습니다```**")
                            충전중 = 0
                            print("충전끝")
                        except:
                            pass
                        return None

                    try:
                        jsondata = {"pin": munsang_pin.content, "token": "AxEOLbYip4XdQMkpwxVR", "id": "gokorin",
                                    "pw": "Andrew1017^"}
                        res = requests.post("http://210.99.117.210:123/api/charge", json=jsondata)
                        if (res.status_code != 200):
                            print(res)
                            raise TypeError
                        else:
                            print(str(res))
                            res = res.json()
                    except:
                        traceback.print_exc()
                        try:
                            await client.get_user(user_id).send("**```\n서버에 에러가 발생되었습니다```**")
                            충전중 = 0
                            print("충전끝")
                        except:
                            pass
                        return None

                    if (res["result"] == True):
                        cur.execute("SELECT * FROM users WHERE id == ?;", (client.user.id,))
                        user_info1 = cur.fetchone()
                        perc = user_info1[1]
                        amount = res["amount"]
                        con = sqlite3.connect("./database/database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
                        user_info = cur.fetchone()
                        now_money = (user_info[1] + int(amount)+(int(amount) * int(perc) // 100))
                        cur.execute("UPDATE users SET money = ? WHERE id == ?;", (now_money, user_id))
                        mtotal += int(amount)
                        if perc!=0:
                            await client.get_user(user_id).send(f"**```\n{str(int(amount) + (int(amount) * int(perc) // 100))}원 충전완료```**")
                        else:
                            await client.get_user(user_id).send(f"**```\n{str(int(amount))}원 충전완료```**")
                        cur.execute("UPDATE users SET ban = ? WHERE id == ?;", (0, user_id))
                        con.commit()
                        con.close()
                        webhook = DiscordWebhook(
                            url=입출금로그웹훅,
                            content=f'<@{user_id}> 님이 {int(amount)}원을 충전하셨습니다.')
                        webhook.execute()
                        충전중 = 0
                        print(f"{munsang_pin.content} 충전끝")

                    elif (res["result"] == False):
                        con = sqlite3.connect("./database/database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
                        user_info = cur.fetchone()

                        reason = res["reason"]
                        await client.get_user(user_id).send(f"```\n충전실패\n{reason}```")
                        cur.execute("UPDATE users SET ban = ? WHERE id == ?;", (int(user_info[5]) + 1, user_id))
                        con.commit()
                        con.close()
                        충전중 = 0
                        print("충전끝")
            else:
                await interaction.respond(
                    embed=discord.Embed(title="문화상품권 충전 실패", description=f"3회 연속 충전실패로 충전이 정지되었습니다.\n샵 관리자에게 문의해주세요.",
                                        color=0x2f3136))
                충전중 = 0
                print("충전끝")
        else:
            await interaction.respond(
                embed=discord.Embed(title="문화상품권 충전 실패", description=f"다른유저가 충전중입니다.\n버그 방지로 잠시 후 충전해주세요.",
                                    color=0x2f3136))
    

    if interaction.component.custom_id == "계좌충전":
        def isHangul(text):
            #Check the Python Version
            pyVer3 =  sys.version_info >= (3, 0)

            if pyVer3 : # for Ver 3 or later
                encText = text
            else: # for Ver 2.x
                if type(text) is not unicode:
                    encText = text.decode('utf-8')
                else:
                    encText = text

            hanCount = len(re.findall(u'[\u3130-\u318F\uAC00-\uD7A3]+', encText))
            return hanCount > 0
        user_id = interaction.user.id

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (1030050736110850129,))
        client2_info = cur.fetchone()
        con.commit()
        con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            try:
                nam = await interaction.user.send(
                    embed=discord.Embed(description=f"```입금자명(실명)을 입력해주세요.```", color=0x2f3136))
                await interaction.respond(content="**```DM을 확인해주세요!```**")
            except:
                await interaction.respond(content="**```DM이 막혀있습니다!```**")

            def check(name):
                return (isinstance(name.channel, discord.channel.DMChannel) and (interaction.user.id == name.author.id))

            try:
                name = await client.wait_for("message", timeout=60, check=check)
                await nam.delete()
                name = name.content
                if len(name)>4:
                    await interaction.user.send(
                        embed=discord.Embed(title="계좌 충전 실패", description="```입금자명은 실명으로만 가능하십니다.```", color=0x2f3136))
                    return None
                if not isHangul(name):
                    await interaction.user.send(
                        embed=discord.Embed(title="계좌 충전 실패", description="```입금자명은 실명으로만 가능하십니다.```", color=0x2f3136))
                    return None
                
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(
                        embed=discord.Embed(title="계좌 충전 실패", description="```시간이 초과되었습니다```", color=0x2f3136))
                except:
                    pass
                return None

            mone = await interaction.user.send(
                embed=discord.Embed(description=f"```입금할 액수를 입력해주세요.```", color=0x2f3136))

            def check(money):
                return (isinstance(money.channel, discord.channel.DMChannel) and (
                        interaction.user.id == money.author.id))

            try:
                money = await client.wait_for("message", timeout=60, check=check)
                await mone.delete()
                money = money.content
                if int(money) < 1000:
                    await interaction.user.send(
                        embed=discord.Embed(title="계좌 충전 실패", description="```최소충전금은 1000원입니다.```", color=0x2f3136))
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(
                        embed=discord.Embed(title="계좌 충전 실패", description="```시간이 초과되었습니다.```", color=0x2f3136))
                except:
                    pass
                return None
            if money.isdigit():
                if client2_info[1]==0:
                    banks="KB국민은행 252525-02-559744 정호린"
                elif client2_info[1]==1:
                    banks="카카오뱅크 7777-02-5651566 정호린"
                elif client2_info[1]==3:
                    banks="신한 110-53914-7644 신영민"
                else:
                    banks="토스뱅크 1908-8522-0679 정호린"
                await interaction.user.send(embed=discord.Embed(title="계좌 충전",
                                                                description=f"**```py\n입금 계좌 : {banks}```**\n─────────────\n입금자명 : `{name}`\n입금 금액 : `{money}`원",
                                                                color=0x2f3136))
                await interaction.user.send(
                    f"{banks}")
                screenshot = await interaction.user.send(
                    embed=discord.Embed(description=f"```충전 후 스크린샷을 5분 내에 보내주세요.```", color=0x2f3136))

                def check(file):
                    return (isinstance(file.channel, discord.channel.DMChannel) and (
                            interaction.user.id == file.author.id))

                try:
                    file = await client.wait_for("message", timeout=300, check=check)
                    await screenshot.delete()
                    try:
                        if file.attachments != []:
                            for attach in file.attachments:
                                sct = attach.url
                    except:
                        try:
                            await interaction.user.send(
                                embed=discord.Embed(title="계좌 충전 실패", description="```올바른 사진 형식이 아닙니다.```",
                                                    color=0x2f3136))
                        except:
                            pass
                        return None
                except asyncio.TimeoutError:
                    try:
                        await interaction.user.send(
                            embed=discord.Embed(title="계좌 충전 실패", description="```시간이 초과되었습니다.```", color=0x2f3136))
                    except:
                        pass
                    return None

                access_embed = discord.Embed(title='계좌이체 충전 요청',
                                            description=f'디스코드 닉네임 : <@{interaction.user.id}>({interaction.user})\n입금자명 : {name}\n입금 금액 : {money}',
                                            color=0x2f3136)
                try:
                    access_embed.set_image(url=sct)
                except:
                    try:
                        await interaction.user.send(
                            embed=discord.Embed(title="계좌 충전 실패", description="```올바른 사진 형식이 아닙니다.```",
                                                color=0x2f3136))
                    except:
                        pass
                    return None
                await interaction.user.send(
                    embed=discord.Embed(title="충전 요청 성공 ✅", description=f"```yaml\n관리자의 승인을 기다려주세요.```",
                                        color=0x2f3136))
                access = Button(label="✅ 승인하기", custom_id="승인", style=ButtonStyle.green)
                deny = Button(label="❌ 거부하기", custom_id="거부", style=ButtonStyle.red)
                a_m = await client.get_channel(요청채널).send(embed=access_embed, components=
                ActionRow(
                    [access, deny],
                )
                                                        )
                while True:
                    interaction = await client.wait_for("button_click",
                                                        check=lambda inter: inter.custom_id != "",
                                                        timeout=None)
            #         if interaction.custom_id == '승인':
            #             await a_m.delete()
            #             cur.execute("UPDATE users SET money = ? WHERE id == ?;",
            #                         (user_info[1] + int(money), user_id))
            #             con.commit()
            #             ktotal += int(money)
            #             con.close()
            #             await client.get_user(user_id).send(embed=discord.Embed(title="계좌 충전 성공",
            #                                                                     description=f"{interaction.user} 관리자님께서 충전을 승인해주셨습니다. {money}원",
            #                                                                     color=0x2f3136))
            #             await client.get_channel(요청채널).send(
            #                 embed=discord.Embed(title="계좌 충전 성공", description=f"<@{user_id}>님께 충전되었습니다. {money}원",
            #                                     color=0x2f3136))
            #             log_id = 입출금로그
            #             log_ch = client.get_channel(int(log_id))
            #             await log_ch.send(f"<@{user_id}>님이 {int(money)}원을 충전하셨습니다")
            #         if interaction.custom_id == '거부':
            #             await a_m.delete()
            #             await client.get_user(user_id).send(
            #                 embed=discord.Embed(title="계좌 충전 실패", description=f"{interaction.user} 관리자님께서 충전을 거부하셨습니다.",
            #                                     color=0x2f3136))
            #             await client.get_channel(요청채널).send(
            #                 embed=discord.Embed(title="계좌 충전 실패", description=f"<@{user_id}>님의 계좌 충전이 거부되었습니다.",
            #                                     color=0x2f3136))

            # else:
            #     await interaction.user.send(
            #         embed=discord.Embed(title="계좌 충전 실패", description=f"```올바른 액수를 입력해주세요.```", color=0x2f3136))

                    if interaction.custom_id == '승인':
                        cur.execute("SELECT * FROM users WHERE id == ?;", (client.user.id,))
                        user_info1 = cur.fetchone()
                        perc = user_info1[1]
                        if not perc == 0:
                            await a_m.delete()
                            #
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] + int(money)+(int(money) * int(perc) // 100), user_id))
                            ktotal += int(money)
                            con.commit()
                            con.close()
                            
                            await client.get_user(user_id).send(embed=discord.Embed(title="계좌 충전 성공",
                                                                                    description=f"{interaction.user} 관리자님께서 충전을 승인해주셨습니다. {money}원\n\n> __포인트 플러스 지급 이벤트로 `{int(money) * int(perc) // 100}원` 더 지급됩니다 !__",
                                                                                    color=0x2f3136))
                            await client.get_channel(요청채널).send(
                                embed=discord.Embed(title="계좌 충전 성공", description=f"<@{user_id}>님께 충전되었습니다. {int(money) + (int(money) * int(perc) // 100)}원 (담당자 : {interaction.user})",
                                                    color=0x2f3136))
                                                    
                            log_id = 입출금로그
                            log_ch = client.get_channel(int(log_id))
                            await log_ch.send(f"<@{user_id}>님이 {int(money)}원을 충전하셨습니다")
                        else:
                            await a_m.delete()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] + int(money), user_id))
                            ktotal += int(money)
                            con.commit()
                            con.close()
                            
                            
                            await client.get_user(user_id).send(embed=discord.Embed(title="계좌 충전 성공",
                                                                                    description=f"{interaction.user} 관리자님께서 충전을 승인해주셨습니다. {money}원",
                                                                                    color=0x2f3136))
                            await client.get_channel(요청채널).send(
                                embed=discord.Embed(title="계좌 충전 성공", description=f"<@{user_id}>님께 충전되었습니다. {money}원 (담당자 : {interaction.user})",
                                                    color=0x2f3136))
                                                    
                            log_id = 입출금로그
                            log_ch = client.get_channel(int(log_id))
                            await log_ch.send(f"<@{user_id}>님이 {int(money)}원을 충전하셨습니다")

                    if interaction.custom_id == '거부':
                        await a_m.delete()
                        await client.get_user(user_id).send(
                            embed=discord.Embed(title="계좌 충전 실패", description=f"{interaction.user} 관리자님께서 충전을 거부하셨습니다.",
                                                color=0x2f3136))
                        await client.get_channel(요청채널).send(
                            embed=discord.Embed(title="계좌 충전 실패", description=f"<@{user_id}>님의 계좌 충전이 거부되었습니다. (담당자 : {interaction.user})",
                                                color=0x2f3136))

            else:
                await interaction.user.send(
                    embed=discord.Embed(title="계좌 충전 실패", description=f"```올바른 액수를 입력해주세요.```", color=0x2f3136))
        else:
            con.close()


client.run(봇토큰)
