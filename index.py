# -*- coding: utf-8 -*-
import datetime
import toss
import urllib.request
from re import T
import traceback
import culture
from jmunja import smssend
import string
import collections
import discord, sqlite3, os, random, asyncio, requests, json, time, math, func, re
from Setting import *
from discord_webhook import DiscordEmbed, DiscordWebhook
from discord_buttons_plugin import ButtonType
from discord_components import DiscordComponents, ComponentsBot, Select, SelectOption, Button, ButtonStyle, ActionRow
from rolling_m import get_rolling, get_bet, get_chung, add_bet, write_chung, write_rolling, calculate_rolling, add_bet,write_bet, add_chung1

intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)

user_luck = {}
data = {}

eventlabel = f"오픈기념 매충 100% (롤링 500%)"
eventvalue = f"2-500-{eventlabel}"

banks=계좌번호
uid = uid1
upw = upw1
subject = subject1
callback = callback1
bonus_selection = [SelectOption(label="보너스 없음 (롤링 100%)",value="1-100-보너스 없음(롤링 100%)"),
                   SelectOption(label="카지노 25% 보너스 (롤링 200%)",value="1.25-200-카지노 25% 보너스(롤링 200%)"),
                   SelectOption(label="미니게임 25% 보너스 (롤링 200%)",value="1.25-200-미니게임 25% 보너스(롤링 200%)"),
                   SelectOption(label="에볼루션 30% 보너스 (롤링 250%)",value="1.3-250-미니게임 30% 보너스(롤링 250%)"),
                   SelectOption(label=f"{eventlabel}",value=f"{eventvalue}")]

bank_selection = [SelectOption(label="NH농협",value="NH농협"),
                   SelectOption(label="카카오뱅크",value="카카오뱅크"),
                   SelectOption(label="KB국민은행",value="KB국민은행"),
                   SelectOption(label="신한은행",value="신한은행"),
                   SelectOption(label="우리은행",value="우리은행"),
                   SelectOption(label="토스뱅크",value="토스뱅크"),
                   SelectOption(label="IBK기업",value="IBK기업"),
                   SelectOption(label="하나은행",value="하나은행"),
                   SelectOption(label="새마을",value="새마을"),
                   SelectOption(label="부산은행",value="부산은행"),
                   SelectOption(label="대구은행",value="대구은행"),
                   SelectOption(label="케이뱅크",value="케이뱅크"),
                   SelectOption(label="신협은행",value="신협은행"),
                   SelectOption(label="우체국",value="우체국"),
                   SelectOption(label="SC제일",value="SC제일"),
                   SelectOption(label="경남은행",value="경남은행"),
                   SelectOption(label="광주은행",value="광주은행"),
                   SelectOption(label="수협은행",value="수협은행"),
                   SelectOption(label="전북은행",value="전북은행"),
                   SelectOption(label="저축은행",value="저축은행"),
                   SelectOption(label="제주은행",value="제주은행"),
                   SelectOption(label="씨티",value="씨티")]
#복사하고 label 은 선택할때 뜨는거
#value는 항상 배수-롤링-메시지(label이랑 똑같이 하면 좋음) ㅣ 여기서 배수는 백분율 아님, 실제 지급되는 돈의 배수임 ex) 1000원 충전, 60% 추가 지급 선택 -- 배수를 1.6
admin_id = 관리자
bakara_on = 0
lbakara_on = 0
hz_on = 0
coin1_on = 0
lotto_on = 0
hz_h = []
hz_z = []
coinbet = []
bkr_p = []
bkr_b = []
bkr_d = []
lbkr_p = []
lbkr_b = []
lbkr_d = []
doing_bet = []
doing_bet2 = []
doing_bet3 = []
doing_bet7 = []
doing_bet77 = []
doing_betcoin = []
event1 = 2
event2 = 1
rolling = 500
doing_bet4 = []
moneytotal = 0
ktotal = 0
mtotal = 0
충전중 = 0
t = 0
ti = 0
tim = 0
timm = 0
timmm = 0
ticoin = 0
amount=0
lbkramount=0
count=0
using=0
bjusing=0
livebet=0
ttii = 0
r_t=0
coin_on = 1
dt_on = 0
km_on = 0
doing_bet5 = []
# 룰렛 ㅡㅡㅡㅡ
rl_on=0
doing_bet6 = []

common = '일반문의-'

charge = '충전문의-'

qs = '환전문의-'

purchase = '버그문의-'

bozi = '배팅채널-'

card_shape = ["♠️","♥️","♦️","♣"]
card_list = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

def reset_rolling_stat(id):
    write_chung(id,0)
    write_rolling(id,0)
    write_bet(id,0)

def pick_a_card():
    random_shape = random.choice(card_shape)
    random_card = random.choice(card_list)
    if random_card == "A":
        return [1,random_shape]
    elif random_card == "J":
        return [11,random_shape]
    elif random_card == "Q":
        return [12,random_shape]
    elif random_card == "K":
        return [13,random_shape]
    else:
        return [int(random_card),random_shape]


def roulette_color(number):
    red = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]

    if number == 0:
        return "green"
    elif number in red:
        return "red"
    elif not number in red and number != 0:
        return "black"




def deal(deck):
    hand = []
    random.shuffle(deck)
    for i in range(2):
        
        card = deck.pop()
        if card == 11:
            card = 'J'
        if card == 12:
            card = 'Q'
        if card == 13:
            card = 'K'
        if card == 14:
            card = 'A'
        a = ['스페이드', '다이아', '클로버', '하트']
        c = random.choice(a)
        hand.append(f"{a} {card}")
    return hand
# Adds cards to  hand
def draw(deck, hand):
    card = deck.pop()
    if card == 11:
        card = 'J'
    if card == 12:
        card = 'Q'
    if card == 13:
        card = 'K'
    if card == 14:
        card = 'A'
    hand.append(card)

# Calculates the total of a hand
def total(hand):
    total = 0
    # Creates a hidden hand that sorts itself
    calchand = []
    for card in hand:
        calchand.append(card)
    # Put face cards to number to sort them to maintain elasticity of ACE
    for i in range(len(calchand)):
        if calchand[i] == 'J' or calchand[i] == 'Q' or calchand[i] == 'K':
            calchand[i] = 99
        if calchand[i]  == 'A':
            calchand[i] = 100
    calchand.sort()
    # Calculate the total of the hand
    for card in calchand:
        if card == 99:
            total += 10
        elif card == 100:
            if total >= 11:
                total += 1
            else:
                total += 11
        else:
            total += card
    return total

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
        "CREATE TABLE users (id INTEGER, money INTEGER, boggle_bet_pick TEXT, boggle_bet_money INTEGER, is_bet INTEGER, ban INTEGER, ladder_bet_pick TEXT, ladder_bet_money INTEGER, wllet_bet_pick TEXT, wllet_bet_money INTEGER, owrun_bet_pick TEXT, owrun_bet_money INTEGER, eos1_bet_pcik TEXT, eos1_bet_money INTEGER, pwball_bet_pick TEXT, pwball_bet_money INTEGER, eos5_bet_pcik TEXT, eos5_bet_money INTEGER, powerladder_bet_pick TEXT, powerladder_bet_money INTEGER, ad_bet_pick TEXT, ad_bet_money INTEGER, rotoball_bet_pick TEXT, rotoball_bet_money INTEGER, rotoladder_bet_pick TEXT, rotoladder_bet_money INTEGER, hz_bet_pick TEXT, hz_bet_money INTEGER, coin_bet_money INTEGER, perc INTEGER, eos2_bet_pick TEXT, eos2_bet_money, eos3_bet_pick TEXT, eos3_bet_money, eos4_bet_pick TEXT, eos4_bet_money, strongladder_pick TEXT, strongladder_money INTEGER, kino_ladder_pick TEXT, kino_ladder_money INTEGER, bet_amount INTEGER, bet_money INTEGER, lightbkr_bet_pick TEXT, lightbkr_bet_money INTEGER, alphapw_bet_pick TEXT, alphapw_bet_money INTEGER, strongball_pick TEXT, strongball_money INTEGER, jumangi_pick TEXT, jumangi_money INTEGER, bangu_pick TEXT, bangu_money INTEGER, bingo_pick TEXT, bingo_money INTEGER, mega_pick TEXT, mega_money INTEGER, nextb_pick TEXT, nextb_money INTEGER, nextling_pick TEXT, nextling_money INTEGER, nextladder_pick TEXT, nextladder_money INTEGER, nextball_pick TEXT, nextball_money INTEGER, pwladder_pick TEXT, pwladder_money INTEGER, evobkrA_pick TEXT, evobkrA_money INTEGER, evokoreabkrA_pick TEXT, evokoreabkrA_money INTEGER, evodt_pick TEXT, evodt_money INTEGER, evosicbo_pick TEXT, evosicbo_money INTEGER, evorl_pick TEXT, evorl_money INTEGER, evobkrB_pick TEXT, evobkrB_money INTEGER, evokoreabkrB_pick TEXT, evokoreabkrB_money INTEGER, evoft_pick TEXT, evoft_money INTEGER, evosoccer_pick TEXT, evosoccer_money INTEGER)")
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
        await client.change_presence(activity=discord.Streaming(name=f'{len(client.users)}명과 함께', url='https://www.twitch.tv/pornhub'))
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Streaming(name='리치랜드!', url='https://www.twitch.tv/pornhub'))
        await asyncio.sleep(5)
        await client.change_presence(activity=discord.Streaming(name='문상/계좌/코인 도박장', url='https://www.twitch.tv/pornhub'))
        await asyncio.sleep(5)

@client.event
async def on_message(message):
    if message.guild is None:
        if message.author.bot:
            return
        else:
            embed = discord.Embed(colour=discord.Colour.blue(), timestamp=message.created_at)
            embed.add_field(name='전송자', value=message.author, inline=False)
            embed.add_field(name='내용', value=message.content, inline=False)
            embed.set_footer(text=f'봇 DM LOG.')
            await client.get_channel(1115616339852271673).send(f"`{message.author.name}({message.author.id})`", embed=embed)
    global ktotal
    global moneytotal
    global mtotal
    global bakara_on
    global lbakara_on
    global lotto_on
    global hz_on
    global coin1_on
    global dt_on
    global livebet
    global hz_h
    global coinbet
    global eventvalue
    global eventlabel
    global hz_z
    global bkr_p
    global bkr_b
    global timm
    global timmm
    global bkr_d
    global doing_bet
    global doing_bet2
    global doing_bet7
    global doing_betcoin
    global p
    global b
    global p_add_card
    global b_add_card
    global player_card
    global banker_card
    global player_card2
    global banker_card2
    global bkr_round
    global lbkr_round
    global t
    global ti
    global tim
    global ticoin
    global hz_round
    global doing_bet3
    global coin_on
    global doing_bet4
    global d_card
    global t_card
    global dt_round
    global coin_round
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
    global lotto_round
    global r_t
    global doing_bet6
    global doing_bet77
    global rl_on
    global number1
    global color
    global banks
    global 충전중
    lowered_text = message.content.lower()
    refined_text = re.sub(r'[^\w\s]','', lowered_text)

    conn = sqlite3.connect('passwords.db')
    co = conn.cursor()
    co.execute('''CREATE TABLE IF NOT EXISTS passwords
                (channel_id INTEGER, password TEXT)''')

    def check_invite(string:str):
        number_of_g = string.find("g")
        number_of_G = string.find("G")
        invite_exist = string.find("invite")
        if number_of_G + number_of_g > 2:
            return True
        else:
            if invite_exist == -1:
                return False
            else:
                return True

    def talmoembed(embedtitle, description):
        return discord.Embed(title=embedtitle, description=description, color=0x34c6eb)
    def failembed(embedtitle, description):
        return discord.Embed(title=embedtitle, description=description, color=0xff0000)

    def betingembed(embedtitle, description):
        return discord.Embed(title=embedtitle, description=description, color=0x00ff00)

    if message.author.bot:
        return

    con = sqlite3.connect("./database/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
    user_info = cur.fetchone()

    if (user_info == None):
        cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
            message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
        con.commit()
        con.close()
    con.close()

    splited_msg = message.content.split(" ")

    if message.content.startswith("!코드생성 "):
        if message.author.id in admin_id:
            try:
                gen_amount = int(message.content.split(" ")[1])
                gen_money_amount = int(message.content.split(" ")[2])
            except:
                return
            codes = []
            con = sqlite3.connect("db.db")
            cur = con.cursor()
            for _ in range(gen_amount):
                code1 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                code2 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                code3 = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                code = f"{code1}-{code2}-{code3}"
                codes.append(code)
                cur.execute("INSERT INTO codes Values(?, ?);", (code, gen_money_amount))
                con.commit()
            con.close()
            if len("\n".join(codes)) < 2000:
                await message.reply(embed=talmoembed("🎲 생성 완료", "**생성이 완료되었습니다.\nDM을 확인해주세요.**"))
                await message.author.send("\n".join(codes))
            else:
                await message.reply(embed=talmoembed("🎲 생성 실패", "**글자 초과입니다.**"))
        else:
            await message.reply(embed=talmoembed("🎲 생성 실패", "**슈퍼짱짱 도그보만 사용가능한 명령어입니다.**"))
    

    if message.content.startswith("!삭제"):
        if message.author.id in admin_id:
            try:
                code = int(message.content.split(" ")[1])
            except:
                return
            conz = sqlite3.connect("./db.db")
            curz = conz.cursor()
            curz.execute(f"SELECT * FROM codes WHERE code == ?;", (code,))
            codeinfo = curz.fetchone()
            conz.close()
            if codeinfo != None:
                conz = sqlite3.connect("db.db")
                curz = conz.cursor()
                curz.execute("DELETE FROM codes WHERE code == ?;", (code,))
                conz.commit()
                conz.close()
                await message.reply(embed=talmoembed("🎲 삭제 완료", f"**{code} 코드가 삭제되었습니다.**"))
            else:
                await message.reply(embed=talmoembed("🎲 삭제 실패", "**존재하지 않는 코드입니다.**"))

        else:
            await message.reply(embed=talmoembed("🎲 삭제 실패", "**슈퍼짱짱 관리자만 사용가능한 명령어입니다.**"))

    if message.content.startswith(".충전 "):
        await message.delete()
        code = message.content.split(" ")[1]
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if (user_info == None):
            cur.execute(
                "INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                    message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        conz = sqlite3.connect("./db.db")
        curz = conz.cursor()
        curz.execute(f"SELECT * FROM codes WHERE code == ?;", (code,))
        codeinfo = curz.fetchone()
        conz.close()
        if codeinfo != None:
            amount = codeinfo[1]
            
            conz = sqlite3.connect("db.db")
            curz = conz.cursor()
            curz.execute("DELETE FROM codes WHERE code == ?;", (code,))
            conz.commit()
            conz.close()
            bonus_m = await message.channel.send(embed=talmoembed("🎲 충전", f"<@{message.author.id}>\n**선택하실 보너스를 선택해주세요.**"),
                                                  components=[Select(placeholder="선택하실 보너스를 입력해주세요",
                                                            options=bonus_selection,custom_id="충전 보너스")])
            
            def check(bonus):
                return (message.author.id == bonus.author.id) and (bonus.custom_id == "충전 보너스")
            bonus_amplier = 0
            bonus_rolling = 0
            try:
                bonus = await client.wait_for("select_option", timeout=60, check=check)
                bonus_split = bonus.values[0].split("-")
                bonus_amplier = float(bonus_split[0])
                bonus_rolling = int(bonus_split[1])
                await bonus_m.delete()
            except asyncio.TimeoutError:
                try:
                    await message.channel.send(embed=talmoembed("🎲 충전", f"<@{message.author.id}>\n**시간 초과되었습니다.**"))
                except:
                    pass
                return None
            write_bet(message.author.id,0)
            write_rolling(message.author.id,bonus_rolling)
            add_chung1(message.author.id,float(amount)*bonus_amplier)
            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                        (user_info[1] + float(amount)*bonus_amplier, message.author.id))
            con.commit()
            ktotal += int(amount)
            con.close()
            nojum = math.floor(float(amount)*(bonus_amplier-1))
            await message.channel.send(embed=discord.Embed(title="📥 충전 성공",
                                                                    description=f"<@{message.author.id}>\n{amount}원이 충전되었습니다.\n\n**`보너스 이벤트로 인하여 {nojum}원이 추가로 지급되었습니다.`\n\n불이익을 당하지 않게 반드시 이용약관을 읽어주세요.**",
                                                                    color=0x2f3136))
            await client.get_channel(요청채널).send(
                embed=discord.Embed(title="라이센스 충전 성공", description=f"<@{message.author.id}>님께 충전되었습니다. {amount}원\n\n보너스 이벤트 {nojum}원\n\n선택한 보너스 : {bonus_split}",
                                    color=0x2f3136))
            log_id = 출금로그
            log_ch = client.get_channel(int(log_id))
            await log_ch.send(f"<@{message.author.id}>님이 {int(amount)}원을 충전하셨습니다! [보너스 이벤트 {nojum}원 추가지급]")
            
            log_id = 환전액로그
            log_ch = client.get_channel(int(log_id))
            await log_ch.send(f"<@{message.author.id}>님이 {int(money)}원을 충전하셨습니다! [보너스 이벤트 {nojum}원 추가지급]")

            guild = client.get_guild(int(1103334101043396669))
            user = message.author.id
            name = message.author.name
            member = message.author
            log = ""

            id = 환전액로그
            channel = client.get_channel(int(id))
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
            number = int(money)
            if number < 0 or number >= 1500000:
                return
            elif number < 3000:
                return
            elif number < 15000:
                role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 1')
            elif number < 50000:
                role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 2')
            elif number < 150000:
                role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 3')
            elif number < 350000:
                role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 4')
            elif number < 800000:
                role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 5')
            elif number < 1500000:
                role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 6')
            else:
                role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 7')

            if not role is None and not role in member.roles:
                await member.add_roles(role)
                await message.author.send(f"RICHLAND 잔액 {number}원 누적 충전으로 인해 {role.name} 등급을 부여 받았습니다.")
            
        else:
            await message.channel.send(embed=talmoembed("🎲 라이센스 충전", f"<@{message.author.id}>\n**입력하신 라이센스가 이미 사용되었거나 존재하지 않습니다.**"))


    if message.content.startswith("!내역"):
        if message.author.id in admin_id:
            try:
                user = message.mentions[0].id
                await message.reply(file=discord.File(f"./bet_log/{user}.txt"))
                os.remove(f"./bet_log/{user}.txt")
            except:
                await message.reply(embed=talmoembed("🎲 내역 없음", "**해당 유저는 아직 내역이 기록되있지 않습니다.**"))
        else:
            await message.reply(embed=talmoembed("🎲 권한 없음", "**관리자만 사용가능한 명령어입니다.**"))

    if message.content.startswith('!계좌변경 '):
        if message.author.id in admin_id:
            op=message.content.split(" ")[1]
            if message.content.split(" ")[1] == "기업" or message.content.split(" ")[1] == "신한" or message.content.split(" ")[1] == "이재호" or message.content.split(" ")[1] == "허찬민" or message.content.split(" ")[1] == "리브":
                color = message.content.split(" ")[1]
                if message.content.split(" ")[1] == "기업":
                    banks="IBK기업은행 4801-2973-097411"
                elif message.content.split(" ")[1] == "신한":
                    banks="신한은행 5621-2527-348756"
                elif message.content.split(" ")[1] == "허찬민":
                    banks="토스뱅크 1908-8773-1982"
                elif message.content.split(" ")[1] == "리브":
                    banks="KB국민은행 252525-02-828972"
                else:
                    banks="토스뱅크 1908-5496-4466"
                await message.reply(f"> **계좌번호가 `{banks}` 으로 변경되었습니다.**")

        else:
            await message.reply(embed=talmoembed("🎲 권한 없음", "**관리자만 사용가능한 명령어입니다.**"))
    

    if message.content.startswith("!수수료"):
        if message.author.id in admin_id:
            try:
                percent = float(message.content.split(" ")[1])
                amount = float(message.content.split(" ")[2])
            except:
                await message.reply(embed=talmoembed("🎲 실패", "**명령어를 다시 입력해주세요.\n!수수료 퍼센트 금액**"))
            if percent >= 0 and percent <= 100:
                result = amount * (100-percent) / 100
                await message.reply(embed=talmoembed("수수료 계산완료",f"{amount}에서 {percent}% 수수료 뺀 가격은 {result} 입니다."))
            else:
                await message.reply(embed=talmoembed("🎲 실패", "**퍼센트는 0보다 크고 100보다 작아야합니다.**"))

        else:
            await message.reply(embed=talmoembed("🎲 권한 없음", "**관리자만 사용가능한 명령어입니다.**"))
    if message.content.startswith(".조회"):
        if message.author.guild_permissions.administrator:
            user = message.mentions[0].id
            name = message.mentions[0].name
            log = ""

            id = 환전액로그
            channel = client.get_channel(int(id))
            sex= await message.reply("잠시 기다려주세요...")
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
            await sex.delete()
            embed = discord.Embed(title=f"{name}님의 정보입니다.", description=f"```d\n{name}님의 충전액 : {money}\n{name}님의 환전액 : {mm}\n\n총 수익 : {mm-money}```",
                                color=0x00ff00)
            await message.reply(embed=embed)
    if message.content.startswith("!조회"):
        user = message.author.id
        name = message.author.name
        log = ""

        id = 환전액로그
        channel = client.get_channel(int(id))
        n1g = await message.reply("잠시 기다려주세요...")
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
        await n1g.delete()

        guild = client.get_guild(int(1103334101043396669))
        member = message.author
        
        embed = discord.Embed(title=f"{name}님의 정보입니다.", description=f"```d\n{name}님의 충전액 : {money}\n{name}님의 환전액 : {mm}\n\n총 수익 : {mm-money}```",
                            color=0x00ff00)
        await message.reply(embed=embed)
        
        number = int(money)
        if number < 0 or number >= 1500000:
            return
        elif number < 3000:
            return
        elif number < 15000:
            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 1')
        elif number < 50000:
            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 2')
        elif number < 150000:
            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 3')
        elif number < 350000:
            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 4')
        elif number < 800000:
            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 5')
        elif number < 1500000:
            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 6')
        else:
            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV ')

        if not role is None and not role in member.roles:
            await member.add_roles(role)
            await message.author.send(f"{role.name} 등급을 부여 받았습니다.")


    if (message.content == '!충전'):
        await message.delete()
        if message.author.id in admin_id:
            charge_embed = discord.Embed(title="잔액 충전/입금", description="원하시는 충전수단을 선택해주세요.", color=0x34c6eb)
            account = Button(label="계좌 이체", custom_id="sex", style=ButtonStyle.blue)
            account1 = Button(label="문화 상품권", custom_id="culturelanddeposit", style=ButtonStyle.red)
            coin = Button(label="코인", custom_id="coin", style=ButtonStyle.green)
            await client.get_channel(충전채널).send(embed=charge_embed, components=
            ActionRow(
                [account, account1, coin],
            )
                                                )
    if (message.content == '!출금'):
        await message.delete()
        if message.author.id in admin_id:
            charge_embed = discord.Embed(title="잔액 환전/출금", description="원하시는 출금수단을 선택해주세요.", color=0x34c6eb)
            account = Button(label="계좌 이체", custom_id="bankwithdraw", style=ButtonStyle.blue)
            account1 = Button(label="문화 상품권", custom_id="culturewithdraw", style=ButtonStyle.red)
            coin = Button(label="코인", custom_id="coinwithdraw", style=ButtonStyle.green)
            await client.get_channel(출금채널).send(embed=charge_embed, components=
            ActionRow(
                [account, account1, coin],
            )
                                                )
    if (message.content == '!등급'):
        await message.delete()
        if message.author.id in admin_id:
            coin123123 = Button(label="✅", custom_id="등급받기", style=ButtonStyle.green)
            await message.channel.send("등급을 받으시려면 아래 버튼을 눌러주세요.", components=
            ActionRow(
                [coin123123],
            )
                                                )

        
    
    if (message.content == '!개인배팅'):
        await message.delete()
        if message.author.id in admin_id:
            charge_embed = discord.Embed(title="**개인 배팅 채널**", description="**```yaml\n아래 버튼을 눌러 개인배팅 채널을 생성/참가 하세요.```**", color=0x34c6eb)
            accoun1t = Button(label="생성", custom_id="zzz", style=ButtonStyle.red)
            accou1n1t = Button(label="참가", custom_id="zz11z", style=ButtonStyle.blue)
            await client.get_channel(1115616338262630476).send(embed=charge_embed, components=
            ActionRow(
                [accoun1t, accou1n1t],
            )
                                                )
    
    # if message.content == "!티켓": #!티켓 명령어
    #     if message.author.id in admin_id:
    #         await message.delete() #메시지 자동으로 삭제 #관리자라면 작동하기
    #         embed = discord.Embed(title="**리치랜드 고객센터**", description="문의를 할려면 아래 버튼을 눌러주세요", color=0x010101)
    #         await message.channel.send(
    #                 embed=embed,
    #                     components = [
    #                         ActionRow(
    #                             Button(style=ButtonStyle.grey,label=" 일반문의",custom_id="ticket"),
    #                             Button(style=ButtonStyle.red,label="❗ 오류 제보",custom_id="q"),
    #                         )
    #                     ]
    #                 )

#     if message.content == "!하이로우":
#         if message.author.id in admin_id:
#             rs_pe = client.get_channel(하이로우회차)
#             # pe_rs = await rs_pe.send(f"`1회차`가 진행되고있습니다.")
#             round_rs = ''
#             if rl_on == 0:
#                 await message.channel.send(f"<#{하이로우채널}> 에 게임이 시작됩니다.")
#                 rl_on = 1
#                 rl_round = 0
#                 while True:
#                     rl_round += 1
#                     if rl_round == 500:
#                         rl_round = 1
#                     else:
#                         pass
#                     hiloemoji = ""
#                     cardemoji = ""
#                     cardcolor = ""
#                     cardzz = ""
#                     cardhmm = ""
#                     hilo = ""
#                     cardnum = ""
#                     number1 = random.randint(0, 36)
#                     rs_ch = 하이로우유출픽
#                     xx = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']
#                     cardnum = random.choice(xx)
#                     cardmo = ['스페이드', '다이아', '클로버', '하트', '스페이드', '다이아', '클로버', '하트', '스페이드', '다이아', '클로버', '하트', '스페이드', '다이아', '클로버', '하트', '스페이드', '다이아', '클로버', '하트', '스페이드', '다이아', '클로버', '하트', '스페이드', '다이아', '클로버', '하트', 'JOKER']
#                     cardzz = random.choice(cardmo)
#                     if cardzz == '스페이드' or cardzz == '클로버':
#                         cardcolor = "BLACK"
#                     elif cardzz == '다이아' or cardzz == '하트':
#                         cardcolor = "RED"
#                     elif cardzz == 'JOKER':
#                         cardcolor = "JOKER"
                    
#                     if int(cardnum) <= 7:
#                         hilo = "LO"
#                     elif int(cardnum) > 7:
#                         hilo = "HI"
#                     else:
#                         pass
                    
#                     if cardnum == '3' or cardnum == '4' or cardnum == '5' or cardnum == '6' or cardnum == '7' or cardnum == '8':
#                         cardhmm = "three"
#                     elif cardnum == '1' or cardnum == '11' or cardnum == '12' or cardnum == '13':
#                         cardhmm = "JQKA"
#                     else:
#                         cardhmm = "None"
#                         pass
                    
#                     if cardcolor == "JOKER":
#                         cardnum == " ⚡"
#                     else:
#                         pass
#                     await client.get_channel(rs_ch).send(
#                         f"{rl_round}회차\n{cardzz} {cardnum}\n{cardhmm}\n{cardcolor}")
#                     r_t = 30
#                     rl_ch = client.get_channel(하이로우채널)
#                     bet_embed = discord.Embed(title=f"{rl_round}회차 배팅가능시간입니다.",
#                                             description=f"하이, 로우, 레드, 블랙 등에 배팅해주십시오.\n남은 배팅시간 : `{r_t}` ", color=0x34c6eb)
#                     bet_embed.set_footer(text=서버이름)
#                     bet_msg = await rl_ch.send(embed=bet_embed)
#                     for i in range(0, 30):
#                         await asyncio.sleep(0.9)
#                         r_t -= 1
#                         bet_embed = discord.Embed(title=f"{rl_round}회차 배팅가능시간입니다.",
#                                                 description=f"하이, 로우, 레드, 블랙 등에 배팅해주십시오.\n남은 배팅시간 : `{r_t}` ", color=0x34c6eb)
#                         bet_embed.set_footer(text=서버이름)
#                         await bet_msg.edit(embed=bet_embed)
#                     if cardnum == "1":
#                         cardnum = "A"
#                     elif cardnum == "11":
#                         cardnum = "J"
#                     elif cardnum == "12":
#                         cardnum = "Q"
#                     elif cardnum == "13":
#                         cardnum = "K"
#                     else:
#                         pass
#                     close_embed = discord.Embed(title=f"{rl_round}회차 배팅이 마감되었습니다", description=f'''

# 카드 결과

# `{cardzz} {cardnum}`

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
# :arrow_up: 하이 HI : {"✅" if hilo == "HI" else ""}   {"< 승리! > X1.95배" if hilo == "HI" else ""}\n
# :arrow_down: 로우 LO : {"✅" if hilo == "LO" else ""}   {"< 승리! > X1.95배" if hilo == "LO" else ""}\n
# :red_circle: 레드 RED : {"✅" if cardcolor == "RED" else ""}   {"< 승리! > X1.97배" if cardcolor == "RED" else ""}\n
# :black_circle: 블랙 BLACK : {"✅" if cardcolor == "BLACK" else ""}   {"< 승리! > X1.97배" if cardcolor == "BLACK" else ""}\n
# :star: 3~8 : {"✅" if cardhmm == "three" else ""}   {"< 승리! > X1.6배" if cardhmm == "three" else ""}\n
# :crown: JQKA : {"✅" if cardhmm == "JQKA" else ""}   {"< 승리! > X2.4배" if cardhmm == "JQKA" else ""}\n
# :black_joker: 조커 JOKER : {"✅" if cardcolor == "JOKER" else ""}   {"< 승리! > X20배" if cardcolor == "JOKER" else ""}\n
#                             ''', color=0xff0000)
#                     await bet_msg.delete()
#                     bet_msg = await rl_ch.send(embed=close_embed)

#                     bet_log = ""
#                     conn = sqlite3.connect('./database/database.db')
#                     c = conn.cursor()
#                     list_a = list(c.execute("SELECT * FROM users"))
#                     for i in list_a:
#                         if (i[28] == None):
#                             continue
#                         conn = sqlite3.connect('./database/database.db')
#                         c = conn.cursor()
#                         if hilo == "HI" or hilo == "LO":
#                             배당 = 1.95
#                         elif cardcolor == "RED" or cardcolor == "BLACK":
#                             배당 = 1.97
#                         elif cardhmm == "three":
#                             배당 = 1.6
#                         elif cardhmm == "JQKA":
#                             배당 = 2.4
#                         else:
#                             배당 = 20

#                         if i[28] == hilo or i[28] == cardcolor or i[28] == cardhmm:

#                             bet_log += (f"**<@{i[0]}> {i[28]} {round(i[29] * 배당)} 적중**\n")
#                             c.execute("UPDATE users SET money = money + ? where id=?", (round(i[29] * 배당), i[0],))
#                         else:

#                             bet_log += (f"**<@{i[0]}> {i[28]} 미적중**\n")

#                         c.execute("UPDATE users SET rl_bet_pick = ? where id=?", (None, i[0],))
#                         c.execute("UPDATE users SET rl_bet_money = ? where id=?", (None, i[0],))
#                         conn.commit()
#                         conn.close()
#                     if hilo == "HI":
#                         hiloemoji = "🔼"
#                     elif hilo == "LO":
#                         hiloemoji = "🔽"
#                     if cardcolor == "BLACK":
#                         cardemoji = "⚫"
#                     elif cardcolor == "RED":
#                         cardemoji = "🔴"
#                     elif cardcolor == "JOKER":
#                         cardemoji = "🃏"
#                     color = f"{hilo} {hiloemoji} | {cardcolor} {cardemoji}"
#                     round_rs = f"\n\n`{rl_round}회차` -- **{color.upper()}**"
#                     doing_bet6 = []
#                     ch = client.get_channel(하이로우배팅내역)
#                     await ch.send(f"`{rl_round}회차`\n\n{bet_log}")
#                     await rs_pe.send(f"{round_rs}")

#     if message.content.startswith('.하이로우 '):
#         if rl_on != 0:
#             con = sqlite3.connect("./database/database.db")
#             cur = con.cursor()
#             cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
#             user_info = cur.fetchone()
#             if not user_info[5] == 3:
#                 if message.content.split(" ")[2] == "올인":
#                     if (int(user_info[1]) >= 500):
#                         amount = int(user_info[1])
#                     else:
#                         con.close()
#                         await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
#                 else:
#                     try:
#                         amount = int(message.content.split(" ")[2])
#                     except:
#                         con.close()
#                         await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**금액은 정수만 배팅이 가능합니다.**"))
#                         return
#                 if not amount < 500:
#                     if user_info[1] >= amount:
#                         choice = message.content.split(" ")[1]
#                         if choice == "하이" or choice == "로우" or choice == "빨" or choice == "검" or choice == "3~8" or choice == "JQKA" or choice == "조커":
#                             if not message.author.id in doing_bet6:
#                                 doing_bet6.append(message.author.id)
#                                 if user_info[1] >= 500:

#                                     cur.execute("UPDATE users SET money = ? WHERE id == ?;",
#                                                 (user_info[1] - int(amount), message.author.id))
#                                     if choice == "하이":
#                                         choice="HI"
#                                     elif choice == "로우":
#                                         choice = "LO"
#                                     elif choice == "빨":
#                                         choice = "RED"
#                                     elif choice == "검":
#                                         choice = "BLACK"
#                                     elif choice == "3~8":
#                                         choice = "3~8"
#                                     elif choice == "JQKA":
#                                         choice = "JQKA"
#                                     elif choice == "조커":
#                                         choice = "JOKER"
#                                     cur.execute("UPDATE users SET rl_bet_pick = ? WHERE id == ?;",
#                                                 (choice, message.author.id))

#                                     cur.execute("UPDATE users SET rl_bet_money = ? WHERE id == ?;",
#                                                 (amount, message.author.id))
#                                     con.commit()
#                                     cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
#                                                 (amount, message.author.id))
#                                     con.commit()
#                                     add_bet(message.author.id,amount)
#                                     con.close()
#                                     await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**> {rl_round}회차 하이로우 {choice.upper()}에 배팅이 완료되었습니다.\n\n`{int(r_t)}초` 뒤 진행됩니다.\n\n잔액 : `{user_info[1] - amount}`\n배팅금 : `{amount}`**"))

#                                 else:
#                                     con.close()
#                                     await message.channel.send(
#                                         embed=talmoembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
#                             else:
#                                 con.close()
#                                 await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))
#                         else:
#                             con.close()
#                             await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**하이/로우/빨/검/3~8/JQKA/조커 중에서만 배팅해주세요.**"))
#                     else:
#                         con.close()
#                         await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
#                 else:
#                     con.close()
#                     await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
#             else:
#                 con.close()
#                 await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
#         else:
#             await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```게임이 진행중이지 않습니다.```**"))


    if message.content.startswith('.즉석룰렛 레드 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[2] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[2])

        if (user_info == None):
            cur.execute(
                "INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                    message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    if not (user_info[5] == 3):
                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                    (user_info[1] - amount, message.author.id))
                        con.commit()
                        con.close()

                        number1 = random.randint(0, 36)
                        number2 = random.randint(0, 100)
                        color = func.roulette_color(number1)

                        if color == "red":
                            if number2 >= 53:
                                bet_list = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]
                                number1 = random.choice(bet_list)
                                color = func.roulette_color(number1)
                            else:
                                bet_list = [15, 4, 2, 17, 6, 13, 11, 8, 10, 25, 33, 20, 31, 22, 29, 28, 35, 26]
                                number1 = random.choice(bet_list)
                                color = func.roulette_color(number1)

                        if color == "red":
                            is_hit = "적중"
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                            user_info = cur.fetchone()

                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (round(user_info[1] + (amount * 1.95)), message.author.id,))
                            con.commit()
                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                        (amount, message.author.id))
                            con.commit()
                            add_bet(message.author.id,amount)

                            con.close()
                            await message.reply(embed=talmoembed("배팅완료",
                                                                f"**배팅완료\n번호 : {str(number1)}, 색깔 : {color.upper()}, {is_hit}\n\n잔액 : {round(user_info[1] + (amount * 1.95))}**"))
                        else:
                            is_hit = "미적중"

                            con.close()
                            await message.reply(embed=talmoembed("배팅완료",
                                                                f"**배팅완료\n번호 : {str(number1)}, 색깔 : {color.upper()}, {is_hit}\n\n잔액 : {user_info[1] - amount}**"))
                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.즉석룰렛 블랙 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[2] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[2])

        if (user_info == None):
            cur.execute(
                "INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                    message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    if not (user_info[5] == 3):
                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                    (user_info[1] - amount, message.author.id))
                        con.commit()
                        con.close()

                        number1 = random.randint(0, 36)
                        number2 = random.randint(0, 100)

                        color = func.roulette_color(number1)

                        if color == "black":
                            if number2 >= 53:
                                bet_list = [15, 4, 2, 17, 6, 13, 11, 8, 10, 25, 33, 20, 31, 22, 29, 28, 35, 26]
                                number1 = random.choice(bet_list)
                                color = func.roulette_color(number1)
                            else:
                                bet_list = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]
                                number1 = random.choice(bet_list)
                                color = func.roulette_color(number1)

                        if color == "black":
                            is_hit = "적중"
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                            user_info = cur.fetchone()

                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (round(user_info[1] + (amount * 1.95)), message.author.id,))
                            con.commit()
                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                        (amount, message.author.id))
                            con.commit()
                            add_bet(message.author.id,amount)

                            con.close()
                            await message.reply(embed=talmoembed("배팅완료",
                                                                f"**배팅완료\n번호 : {str(number1)}, 색깔 : {color.upper()}, {is_hit}\n\n잔액 : {round(user_info[1] + (amount * 1.95))}**"))
                        else:
                            is_hit = "미적중"

                            con.close()
                            await message.reply(embed=talmoembed("배팅완료",
                                                                f"**배팅완료\n번호 : {str(number1)}, 색깔 : {color.upper()}, {is_hit}\n\n잔액 : {user_info[1] - amount}**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.즉석룰렛 그린 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[2] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[2])

        if (user_info == None):
            cur.execute(
                "INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                    message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    if not (user_info[5] == 3):
                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                    (user_info[1] - amount, message.author.id))
                        con.commit()
                        con.close()

                        number1 = random.randint(0, 36)

                        color = func.roulette_color(number1)

                        if color == "green":
                            is_hit = "적중"
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                            user_info = cur.fetchone()

                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (round(user_info[1] + (amount * 8)), message.author.id,))
                            con.commit()
                            add_bet(message.author.id,amount)

                            
                            
                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                        (amount, message.author.id))
                            con.commit()

                            con.close()
                            await message.reply(embed=talmoembed("배팅완료",
                                                                f"**배팅완료\n번호 : {str(number1)}, 색깔 : {color.upper()}, {is_hit}\n\n잔액 : {round(user_info[1] + (amount * 8))}**"))
                        else:
                            is_hit = "미적중"

                            con.close()
                            await message.reply(embed=talmoembed("배팅완료",
                                                                f"**배팅완료\n번호 : {str(number1)}, 색깔 : {color.upper()}, {is_hit}\n\n잔액 : {user_info[1] - amount}**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))


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
            await message.channel.send(embed=talmoembed("**🎲 조회 실패**", "**```관리자만 사용 가능한 명령어입니다.```**"))
            
    # if message.content.startswith('!초대'):
    #     ms = (message.content.split(" ")[1])
    #     sv = client.get_guild(int(ms))
    #     channel = sv.text_channels[0]
    #     invite = await channel.create_invite(max_age=0, max_uses=0)
    #     await message.author.send(f'초대링크 발급해왔습니다\n{invite}')

    if message.content.startswith('.비트코인사다리 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    # req = requests.get("https://bepick.net/json/game/btc_ladder.json?" + str(time.time()).split(".")[0],
                    #                 headers={
                    #                     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #                     # "Host": "ntry.com",
                    #                     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                    #                     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #                     "X-Requested-With": "XMLHttpRequest",
                    #                 }).json()

                    url = 'https://bepick.net/json/game/btc_ladder.json?'

                    # User Agent 설정
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # URL에서 JSON 데이터 가져오기
                    req = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(req)

                    # 응답 데이터 읽기
                    data = response.read()

                    # JSON 데이터를 파이썬 객체로 변환
                    req = json.loads(data)

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

                                embed = discord.Embed(title="✅ 비트코인사다리 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
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
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
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
                                        add_bet(message.author.id,amount)
                                        seconds = int(res["nextTime"])-5
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"

                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/btc_ladder', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        url = 'https://bepick.net/live/result/btc_ladder'

                                        # User Agent 설정
                                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                                        # URL에서 JSON 데이터 가져오기
                                        req = urllib.request.Request(url, headers=headers)
                                        response = urllib.request.urlopen(req)

                                        # 응답 데이터 읽기
                                        data = response.read()

                                        # JSON 데이터를 파이썬 객체로 변환
                                        req = json.loads(data)
                                        roundmsg = int(req["round"]) + 1
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{roundmsg}회차 비트코인사다리 / {interaction.custom_id}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))
    
    if message.content.startswith('.파워사다리 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    # req = requests.get("https://bepick.net/json/game/ntry_pwladder.json?" + str(time.time()).split(".")[0],
                    #                 headers={
                    #                     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #                     # "Host": "ntry.com",
                    #                     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                    #                     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #                     "X-Requested-With": "XMLHttpRequest",
                    #                 }).json()

                    url = 'https://bepick.net/json/game/ntry_pwladder.json?'

                    # User Agent 설정
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # URL에서 JSON 데이터 가져오기
                    req = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(req)

                    # 응답 데이터 읽기
                    data = response.read()

                    # JSON 데이터를 파이썬 객체로 변환
                    req = json.loads(data)

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

                                embed = discord.Embed(title="✅ 파워사다리 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
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
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET pwladder_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET pwladder_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        con.commit()
                                        con.commit()
                                        add_bet(message.author.id,amount)
                                        seconds = int(res["nextTime"])-5
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"
                                        con.close()
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/ntry_pwladder', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        url = 'https://bepick.net/live/result/ntry_pwladder'

                                        # User Agent 설정
                                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                                        # URL에서 JSON 데이터 가져오기
                                        req = urllib.request.Request(url, headers=headers)
                                        response = urllib.request.urlopen(req)

                                        # 응답 데이터 읽기
                                        data = response.read()

                                        # JSON 데이터를 파이썬 객체로 변환
                                        req = json.loads(data)
                                        roundmsg = int(req["round"]) + 1
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{roundmsg}회차 파워사다리 / {interaction.custom_id}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.보글사다리 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    # req = requests.get(
                    #     "https://bepick.net/json/game/bubble_ladder3.json?" + str(time.time()).split(".")[0],
                    #     headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         # "Host": "ntry.com",
                    #         # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()

                    url = 'https://bepick.net/json/game/bubble_ladder3.json?'

                    # User Agent 설정
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # URL에서 JSON 데이터 가져오기
                    req = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(req)

                    # 응답 데이터 읽기
                    data = response.read()

                    # JSON 데이터를 파이썬 객체로 변환
                    req = json.loads(data)

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

                                embed = discord.Embed(title="✅ 보글사다리 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
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
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        add_bet(message.author.id,amount)
                                        cur.execute("UPDATE users SET rotoball_bet_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET rotoball_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        con.commit()
                                        con.close()
                                        seconds = int(res["nextTime"])-5
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/bubble_ladder3', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        url = 'https://bepick.net/live/result/bubble_ladder3'

                                        # User Agent 설정
                                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                                        # URL에서 JSON 데이터 가져오기
                                        req = urllib.request.Request(url, headers=headers)
                                        response = urllib.request.urlopen(req)

                                        # 응답 데이터 읽기
                                        data = response.read()

                                        # JSON 데이터를 파이썬 객체로 변환
                                        req = json.loads(data)
                                        roundmsg1 = int(req["round"]) + 1
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{roundmsg1}회차 보글사다리 / {interaction.custom_id}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.와이룰렛 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    # req = requests.get("https://bepick.net/json/game/y_roulette.json?" + str(time.time()).split(".")[0],
                    #                 headers={
                    #                     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #                     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #                     "X-Requested-With": "XMLHttpRequest",
                    #                 }).json()

                    url = 'https://bepick.net/json/game/y_roulette.json?'

                    # User Agent 설정
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # URL에서 JSON 데이터 가져오기
                    req = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(req)

                    # 응답 데이터 읽기
                    data = response.read()

                    # JSON 데이터를 파이썬 객체로 변환
                    req = json.loads(data)

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

                                embed = discord.Embed(title="✅ 와이룰렛 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
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
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
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
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        seconds = int(res["nextTime"])-5
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"
                                        add_bet(message.author.id,amount)
                                        con.commit()
                                        con.close()
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/y_roulette', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        url = 'https://bepick.net/live/result/y_roulette'

                                        # User Agent 설정
                                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                                        # URL에서 JSON 데이터 가져오기
                                        req = urllib.request.Request(url, headers=headers)
                                        response = urllib.request.urlopen(req)

                                        # 응답 데이터 읽기
                                        data = response.read()

                                        # JSON 데이터를 파이썬 객체로 변환
                                        req = json.loads(data)
                                        roundmsg2 = int(req["round"]) + 1
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{roundmsg2}회차 와이룰렛 / {interaction.custom_id}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.타조 '):
        owpick = ""
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    # req = requests.get(
                    #     "https://bepick.net/json/game/jw_ostrichrun.json?" + str(time.time()).split(".")[0], headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()

                    url = 'https://bepick.net/json/game/jw_ostrichrun.json?'

                    # User Agent 설정
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # URL에서 JSON 데이터 가져오기
                    req = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(req)

                    # 응답 데이터 읽기
                    data = response.read()

                    # JSON 데이터를 파이썬 객체로 변환
                    req = json.loads(data)

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 15):
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                owrunright = Button(label="우", custom_id="우", style=ButtonStyle.blue)
                                owrunleft = Button(label="좌", custom_id="좌", style=ButtonStyle.red)

                                embed = discord.Embed(title="✅ 타조게임 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
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
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        if interaction.custom_id == "우":
                                            owpick = "우"
                                        elif interaction.custom_id == "좌":
                                            owpick = "좌"
                                        else:
                                            owlist = ["좌", "우"]
                                            owpick = random.choice(owlist)
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET owrun_bet_pick = ? WHERE id == ?;",
                                                    (owpick, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET owrun_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        seconds = int(res["nextTime"])-5
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"
                                        add_bet(message.author.id,amount)
                                        con.close()
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/jw_ostrichrun', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        url = 'https://bepick.net/live/result/jw_ostrichrun'

                                        # User Agent 설정
                                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                                        # URL에서 JSON 데이터 가져오기
                                        req = urllib.request.Request(url, headers=headers)
                                        response = urllib.request.urlopen(req)

                                        # 응답 데이터 읽기
                                        data = response.read()

                                        # JSON 데이터를 파이썬 객체로 변환
                                        req = json.loads(data)
                                        roundmsg3 = int(req["round"]) + 1
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{roundmsg3}회차 타조게임 / {owpick}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue
                                else:
                                    await bet_msg.delete()

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.주사위 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    diceone = Button(label="1", custom_id="1", style=ButtonStyle.red)
                    dicetwo = Button(label="2", custom_id="2", style=ButtonStyle.blue)
                    dicethree = Button(label="3", custom_id="3", style=ButtonStyle.red)
                    dicefour = Button(label="4", custom_id="4", style=ButtonStyle.blue)
                    dicefive = Button(label="5", custom_id="5", style=ButtonStyle.red)
                    dicesix = Button(label="6", custom_id="6", style=ButtonStyle.blue)
                    dicelol = Button(label="홀수", custom_id="홀", style=ButtonStyle.green)
                    dicexd = Button(label="짝수", custom_id="짝", style=ButtonStyle.green)

                    embed = discord.Embed(title="주사위 배팅",
                                            description='아래 버튼을 눌러 `주사위` 게임에 배팅해 주세요.',
                                            color=0x34c6eb)
                    embed.set_footer(text=서버이름)
                    bet_msg = await message.reply(embed=embed, components=
                    ActionRow(
                        [diceone, dicetwo, dicethree],
                        [dicefour, dicefive, dicesix],
                        [dicelol, dicexd],
                    )
                                                    )
                    while True:
                        try:
                            interaction = await client.wait_for("button_click",
                                                                check=lambda inter: inter.custom_id != "",
                                                                timeout=5)
                        except asyncio.exceptions.TimeoutError:
                            return

                        if message.author.id == interaction.user.id:
                            await bet_msg.delete()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] - amount, interaction.user.id))
                            con.commit()
                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                        (amount, message.author.id))
                            con.commit()
                            add_bet(message.author.id,amount)
                            con.close()
                            a = ['1', '2', '3', '4', '5', '6']
                            c = random.choice(a)
                            짝 = ['2', '4', '6']
                            홀 = ['1', '3', '5']
                            if c in 짝:
                                holchak = "짝"
                            else:
                                holchak = "홀"
                            
                            if c == '1':
                                sajin = "https://clipartspub.com/images/dice-clipart-one-2.png"
                            elif c == '2':
                                sajin = "https://webstockreview.net/images/dice-clipart-two-2.png"
                            elif c == '3':
                                sajin = "https://th.bing.com/th/id/R.5f5268ee3fd1b61604d70553c5a81409?rik=PWMrthQW9PNAYA&riu=http%3a%2f%2fclipground.com%2fimages%2fnumber-3-dice-clipart-black-and-white-1.png&ehk=2ZtbPtF7szHeGMFY5F0wuNu7OFxFENomHHpSc178zeg%3d&risl=&pid=ImgRaw&r=0"
                            elif c == '4':
                                sajin = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Dice-4-b.svg/1024px-Dice-4-b.svg.png"
                            elif c == '5':
                                sajin = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Dice-5-b.svg/1024px-Dice-5-b.svg.png"
                            elif c == '6':
                                sajin = "https://clipground.com/images/dice-clipart-1-6-1.png"

                            if interaction.custom_id == c:
                                ohshittt = await message.reply("주사위를 굴리고 있어요..! 두구두구 :game_die:")
                                await asyncio.sleep(3)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"{message.author} 승리",color=0x00ff00, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"{c}", inline=True)
                                embed.add_field(name=f"배팅 내역", value=f"{interaction.custom_id}", inline=True)
                                embed.set_thumbnail(url=sajin)
                                await message.channel.send(embed=embed)
                                con = sqlite3.connect("./database/database.db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                user_info = cur.fetchone()

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 5.75)), message.author.id))
                                con.commit()
                            elif interaction.custom_id == holchak:
                                
                                ohshittt = await message.reply("주사위를 굴리고 있어요..! 두구두구 :game_die:")
                                await asyncio.sleep(3)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"{message.author} 승리",color=0x00ff00, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"{c}", inline=True)
                                embed.add_field(name=f"배팅 내역", value=f"{interaction.custom_id}", inline=True)
                                embed.set_thumbnail(url=sajin)
                                await message.channel.send(embed=embed)
                                con = sqlite3.connect("./database/database.db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                user_info = cur.fetchone()

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 1.95)), message.author.id))
                                con.commit()
                            else:
                                ohshittt = await message.reply("주사위를 굴리고 있어요..! 두구두구 :game_die:")
                                await asyncio.sleep(3)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"{message.author} 패배.",color=0xff0000, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"{c}", inline=True)
                                embed.add_field(name=f"배팅 내역", value=f"{interaction.custom_id}", inline=True)
                                embed.set_thumbnail(url=sajin)
                                await message.channel.send(embed=embed)


                else:
                    await message.channel.send(embed=discord.Embed(title="**🎲 배팅 실패**", description="**```보유 금액이 부족합니다.```**", color=0xff0000))
                    con.close()
                    
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.그래프 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        
        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    stop = Button(label="멈추기", custom_id="finish", style=ButtonStyle.red)
                    

                    def check(m):
                        return m.custom_id == "finish" and m.channel == message.channel and message.author.id == m.user.id
                    
                    base_msg = discord.Embed(title="📈그래프 시작📉",color=discord.Color.blue(),timestamp=message.created_at)
                    base_msg.add_field(name="\u200b",value=f"{amount}원 배팅 완료.")
                    
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                (user_info[1] - amount, message.author.id))
                    con.commit()
                    sent_msg = await message.reply(embed=base_msg)
                    success_chance = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0]
                    amplier = 0
                    def graph_roll():
                        random_choice = random.choice(success_chance)
                        if random_choice == 0:
                            return False
                        elif random_choice == 1:
                            return True
                    await asyncio.sleep(1)
                    temp_break = False
                    if graph_roll() == True:
                        amplier = 1
                        result_msg = discord.Embed(title="📈그래프📉",color=discord.Color.blue(),timestamp=message.created_at)
                        result_msg.add_field(name="배수",value=f"{amplier} 배")
                        result_msg.add_field(name="현재 승리금",value=f"{math.floor(amount*amplier)}")
                        await sent_msg.edit(embed=result_msg, components=
                            ActionRow(
                                [stop],
                            ))
                    else:
                        amplier = 0
                        await sent_msg.delete()
                        final_msg = discord.Embed(title="그래프 종료",color=discord.Color.red(),timestamp=message.created_at)
                        final_msg.add_field(name="결과",value=f"실패")
                        final_msg.add_field(name="배수",value=f"0 배")
                        final_msg.add_field(name="승리금",value=f"0")
                        await sent_msg.channel.send(embed=final_msg)
                        temp_break = True
                        return
                    while True:
                        if temp_break == True:
                            break
                        try:
                            interaction = await client.wait_for("button_click", check=check,timeout=1)
                            await sent_msg.delete()
                            final_msg = discord.Embed(title="그래프 종료",color=discord.Color.green(),timestamp=message.created_at)
                            final_msg.add_field(name="결과",value=f"성공")
                            final_msg.add_field(name="배수",value=f"{round(amplier,2)} 배")
                            final_msg.add_field(name="승리금",value=f"{amount*round(amplier,2)}")
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                            user_info = cur.fetchone()

                            cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * amplier)), message.author.id))
                            con.commit()
                            await sent_msg.channel.send(embed=final_msg)
                            break
                        except asyncio.TimeoutError:
                            if graph_roll() == True:
                                amplier += 0.05
                                result_msg = discord.Embed(title="📈그래프📉",color=discord.Color.blue(),timestamp=message.created_at)
                                result_msg.add_field(name="배수",value=f"{round(amplier,2)} 배")
                                result_msg.add_field(name="현재 승리금",value=f"{math.floor(amount*round(amplier,2))}")
                                await sent_msg.edit(embed=result_msg, components=
                                    ActionRow(
                                        [stop],
                                    ))
                            else:
                                temp_break = True
                                await sent_msg.delete()
                                final_msg = discord.Embed(title="그래프 종료",color=discord.Color.red(),timestamp=message.created_at)
                                final_msg.add_field(name="결과",value=f"실패")
                                final_msg.add_field(name="최대 배수",value=f"{round(amplier,2)} 배")
                                final_msg.add_field(name="배수",value=f"0배")
                                final_msg.add_field(name="승리금",value=f"0")
                                amplier = 0
                                await sent_msg.channel.send(embed=final_msg)
                                break

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.동전 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    diceone = Button(label="앞면", custom_id="앞", style=ButtonStyle.red)
                    dicetwo = Button(label="뒷면", custom_id="뒷", style=ButtonStyle.blue)
                    dicethree = Button(label="세우기", custom_id="세", style=ButtonStyle.green)

                    embed = discord.Embed(title="동전 던지기 배팅",
                                            description='아래 버튼을 눌러 `동전 던지기` 게임에 배팅해 주세요.',
                                            color=0x34c6eb)
                    embed.set_footer(text=서버이름)
                    bet_msg = await message.reply(embed=embed, components=
                    ActionRow(
                        [diceone, dicetwo, dicethree],
                    )
                                                    )
                    while True:
                        try:
                            interaction = await client.wait_for("button_click",
                                                                check=lambda inter: inter.custom_id != "",
                                                                timeout=5)
                        except asyncio.exceptions.TimeoutError:
                            return

                        if message.author.id == interaction.user.id:
                            await bet_msg.delete()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] - amount, interaction.user.id))
                            con.commit()
                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                        (amount, message.author.id))
                            con.commit()
                            con.close()
                            add_bet(message.author.id,amount)
                            dongjun = ['앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷','앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷','앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷','앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷','앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷','앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷','앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷','앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷','앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '앞', '뒷', '세']
                            dongjunresult = random.choice(dongjun)

                            if interaction.custom_id == dongjunresult:
                                if dongjunresult == "세":
                                    con = sqlite3.connect("./database/database.db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                    user_info = cur.fetchone()
                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 800)), message.author.id))
                                    con.commit()
                                    ohshittt = await message.reply("띵! :coin:")
                                    await asyncio.sleep(3)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"{message.author} 승리",color=0x00ff00, timestamp=message.created_at)
                                    embed.add_field(name=f"결과", value=f"세우기 ⚡ 800x", inline=True)
                                    embed.add_field(name=f"배팅 내역", value=f"세우기", inline=True)
                                    embed.add_field(name=f"배팅 금액", value=f"{math.floor(amount)}", inline=True)
                                    embed.add_field(name=f"적중 금액", value=f"{math.floor(amount*1.95)}", inline=True)
                                    embed.add_field(name=f"잔액", value=f"{user_info[1]}", inline=True)
                                    embed.set_thumbnail(url="https://upload.inven.co.kr/upload/2014/04/24/bbs/i1819284067.jpg?MW=800")
                                    await message.channel.send(embed=embed)
                                else:
                                    con = sqlite3.connect("./database/database.db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                    user_info = cur.fetchone()

                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 1.95)), message.author.id))
                                    con.commit()
                                    con = sqlite3.connect("./database/database.db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                    user_info = cur.fetchone()
                                    ohshittt = await message.reply("띵! :coin:")
                                    await asyncio.sleep(3)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"{message.author} 승리",color=0x00ff00, timestamp=message.created_at)
                                    embed.add_field(name=f"결과", value=f"{dongjunresult}면 ⚡ 1.95", inline=True)
                                    embed.add_field(name=f"배팅 내역", value=f"{interaction.custom_id}면", inline=True)
                                    embed.add_field(name=f"배팅 금액", value=f"{math.floor(amount)}", inline=True)
                                    embed.add_field(name=f"적중 금액", value=f"{math.floor(amount*1.95)}", inline=True)
                                    embed.add_field(name=f"잔액", value=f"{user_info[1]}", inline=True)
                                    await message.channel.send(embed=embed)
                            elif interaction.custom_id != dongjunresult:
                                if dongjunresult == "세":
                                    con = sqlite3.connect("./database/database.db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                    user_info = cur.fetchone()
                                    ohshittt = await message.reply("띵! :coin:")
                                    await asyncio.sleep(3)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"{message.author} 패배",color=0xff0000, timestamp=message.created_at)
                                    embed.add_field(name=f"결과", value=f"세우기 ⚡ 800x", inline=True)
                                    embed.add_field(name=f"배팅 내역", value=f"{interaction.custom_id}면", inline=True)
                                    embed.add_field(name=f"배팅 금액", value=f"{math.floor(amount)}", inline=True)
                                    embed.add_field(name=f"적중 금액", value=f"0", inline=True)
                                    embed.add_field(name=f"잔액", value=f"{user_info[1]}", inline=True)
                                    embed.set_thumbnail(url="https://upload.inven.co.kr/upload/2014/04/24/bbs/i1819284067.jpg?MW=800")
                                    await message.channel.send(embed=embed)
                                else:
                                    con = sqlite3.connect("./database/database.db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                    user_info = cur.fetchone()
                                    ohshittt = await message.reply("띵! :coin:")
                                    await asyncio.sleep(3)
                                    await ohshittt.delete()
                                    if interaction.custom_id == "앞":
                                        hmm = "앞면"
                                    elif interaction.custom_id == "뒷":
                                        hmm = "뒷면"
                                    else:
                                        hmm = "세우기"
                                    embed = discord.Embed(title=f"{message.author} 패배",color=0xff0000, timestamp=message.created_at)
                                    embed.add_field(name=f"결과", value=f"{dongjunresult}면", inline=True)
                                    embed.add_field(name=f"배팅 내역", value=f"{hmm}", inline=True)
                                    embed.add_field(name=f"배팅 금액", value=f"{math.floor(amount)}", inline=True)
                                    embed.add_field(name=f"적중 금액", value=f"0", inline=True)
                                    embed.add_field(name=f"잔액", value=f"{user_info[1]}", inline=True)
                                    await message.channel.send(embed=embed)
                                    
                            
                                    

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))


    if message.content.startswith('.총게임 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    ga1 = Button(label="좌", custom_id="좌", style=ButtonStyle.red)
                    ba1 = Button(label="우", custom_id="우", style=ButtonStyle.blue)
                    bo1 = Button(label="위", custom_id="위", style=ButtonStyle.red)
                    ba12 = Button(label="아래", custom_id="아래", style=ButtonStyle.blue)

                    embed = discord.Embed(title="총 피하기 배팅",
                                            description='아래 버튼을 눌러 `총 피하기` 게임에 배팅해 주세요.',
                                            color=0x34c6eb)
                    embed.set_footer(text=서버이름)
                    bet_msg = await message.reply(embed=embed, components=
                    ActionRow(
                        [ga1, ba1, bo1, ba12],
                    )
                                                    )
                    while True:
                        try:
                            interaction = await client.wait_for("button_click",
                                                                check=lambda inter: inter.custom_id != "",
                                                                timeout=5)
                        except asyncio.exceptions.TimeoutError:
                            
                            return

                        if message.author.id == interaction.user.id:
                            await bet_msg.delete()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] - amount, interaction.user.id))
                            con.commit()
                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                            con.commit()
                            con.close()
                            if interaction.custom_id == "좌":
                                gun = ['좌','우','위', '아래']
                                c = random.choice(gun)
                                if not (c == '좌'):
                                    ohshittt = await message.reply("탕.. 탕탕! :gun:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"총을 피했어요!",color=0x00ff00, timestamp=message.created_at)
                                    embed.add_field(name=f"총", value=f"{c}", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"{interaction.custom_id}", inline=True)
                                    embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=True)
                                    embed.add_field(name=f"적중 금액", value=f"{amount * 1.2}", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.reply(embed=embed)
                                    con = sqlite3.connect("./database/database.db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                    user_info = cur.fetchone()

                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 1.2)), message.author.id))
                                    con.commit()
                                    break
                                else:
                                    ohshittt = await message.reply("탕.. 탕탕! :gun:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"총에 맞았어요..",color=0xff0000, timestamp=message.created_at)
                                    embed.add_field(name=f"총", value=f"{c}", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"{interaction.custom_id}", inline=True)
                                    embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.reply(embed=embed)
                                    break

                            if interaction.custom_id == "우":
                                gun = ['좌','우','위', '아래']
                                c = random.choice(gun)
                                if not (c == '우'):
                                    ohshittt = await message.reply("탕.. 탕탕! :gun:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"총을 피했어요!",color=0x00ff00, timestamp=message.created_at)
                                    embed.add_field(name=f"총", value=f"{c}", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"{interaction.custom_id}", inline=True)
                                    embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=True)
                                    embed.add_field(name=f"적중 금액", value=f"{amount * 1.2}", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.reply(embed=embed)
                                    con = sqlite3.connect("./database/database.db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                    user_info = cur.fetchone()

                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 1.2)), message.author.id))
                                    con.commit()
                                    break
                                else:
                                    ohshittt = await message.reply("탕.. 탕탕! :gun:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"총에 맞았어요..",color=0xff0000, timestamp=message.created_at)
                                    embed.add_field(name=f"총", value=f"{c}", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"{interaction.custom_id}", inline=True)
                                    embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.reply(embed=embed)
                                    break

                            if interaction.custom_id == "위":
                                gun = ['좌','우','위', '아래']
                                c = random.choice(gun)
                                if not (c == '위'):
                                    ohshittt = await message.reply("탕.. 탕탕! :gun:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"총을 피했어요!",color=0x00ff00, timestamp=message.created_at)
                                    embed.add_field(name=f"총", value=f"{c}", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"{interaction.custom_id}", inline=True)
                                    embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=True)
                                    embed.add_field(name=f"적중 금액", value=f"{amount * 1.2}", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.reply(embed=embed)
                                    con = sqlite3.connect("./database/database.db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                    user_info = cur.fetchone()

                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 1.2)), message.author.id))
                                    con.commit()
                                    break
                                else:
                                    ohshittt = await message.reply("탕.. 탕탕! :gun:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"총에 맞았어요..",color=0xff0000, timestamp=message.created_at)
                                    embed.add_field(name=f"총", value=f"{c}", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"{interaction.custom_id}", inline=True)
                                    embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.reply(embed=embed)
                                    break

                            if interaction.custom_id == "아래":
                                gun = ['좌','우','위', '아래']
                                c = random.choice(gun)
                                if not (c == '아래'):
                                    ohshittt = await message.reply("탕.. 탕탕! :gun:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"총을 피했어요!",color=0x00ff00, timestamp=message.created_at)
                                    embed.add_field(name=f"총", value=f"{c}", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"{interaction.custom_id}", inline=True)
                                    embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=True)
                                    embed.add_field(name=f"적중 금액", value=f"{amount * 1.2}", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.reply(embed=embed)
                                    con = sqlite3.connect("./database/database.db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                    user_info = cur.fetchone()

                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 1.2)), message.author.id))
                                    con.commit()
                                    break
                                else:
                                    ohshittt = await message.reply("탕.. 탕탕! :gun:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"총에 맞았어요..",color=0xff0000, timestamp=message.created_at)
                                    embed.add_field(name=f"총", value=f"{c}", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"{interaction.custom_id}", inline=True)
                                    embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.reply(embed=embed)
                                    break

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))


    if message.content.startswith('.야바위 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    oneba = Button(label="1번", custom_id="1", style=ButtonStyle.red)
                    twoba = Button(label="2번", custom_id="2", style=ButtonStyle.blue)
                    thrba = Button(label="3번", custom_id="3", style=ButtonStyle.green)

                    embed = discord.Embed(title="야바위 배팅",
                                            description='아래 버튼을 눌러 `야바위` 게임에 참여해 주세요.',
                                            color=0x34c6eb)
                    embed.set_footer(text=서버이름)
                    bet_msg = await message.reply(embed=embed, components=
                    ActionRow(
                        [oneba, twoba, thrba],
                    )
                                                    )
                    while True:
                        try:
                            interaction = await client.wait_for("button_click",
                                                                check=lambda inter: inter.custom_id != "",
                                                                timeout=5)
                        except asyncio.exceptions.TimeoutError:
                            
                            return

                        if message.author.id == interaction.user.id:
                            await bet_msg.delete()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] - amount, interaction.user.id))
                            con.commit()
                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                            con.commit()
                            con.close()
                            yabawhiresult = ['1', '2', '3']
                            result = random.choice(yabawhiresult)
                            if interaction.custom_id == result:
                                ohshittt = await message.reply("어디에 공이 있을까요! :wave:")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"적중!",color=0x00ff00, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"**```{result}번째 컵```**", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}번째 컵```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"{math.floor(amount*2.75)}", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                con = sqlite3.connect("./database/database.db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                user_info = cur.fetchone()

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 2.75)), message.author.id))
                                con.commit()
                                break
                            else:
                                ohshittt = await message.reply("어디에 공이 있을까요! :wave:")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"미적중!",color=0xff0000, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"**```{result}번째 컵```**", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}번째 컵```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"0", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                break



                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))


    if message.content.startswith('.가상축구 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    awayteam = ['포항 스틸러스', '제주 유나이티드', 'FC 서울', '울산 현대', '부산 아이파크', '성남 FC', '전북 현대 모터스', '수원 삼성 블루윙즈', '전남 드래곤즈', '인천 유나이티드', '대전 하나 시티즌', '대구 FC', '강원 FC', '경남 FC', '광주 FC', '수원 FC']
                    away = random.choice(awayteam)
                    hometeam = ['상주 상무', '강원 FC B', '거제시민축구단', '고양 해피니스 FC', '당진시민축구단', '대구 FC B', '대전 하나 시티즌 B', '서울 노원 유나이티드 FC', '서울 중랑 축구단', '세종 바네스 FC', '여주 FC', '전주시민축구단', '진주시민축구단', '평창 유나이티드 FC', '평택 시티즌 FC']
                    home = random.choice(hometeam)
                    point1 = ['0', '1',  '1',  '1',  '2',  '2',  '3',  '4', '0', '0']
                    point2 = ['0', '0', '1',  '1',  '0',  '2', '5', '2',  '3',  '1', '4', '1', '1']
                    awaypoint = random.choice(point1)
                    homepoint = random.choice(point2)
                    if int(awaypoint) > int(homepoint):
                        win = "원정"
                    elif int(awaypoint) < int(homepoint):
                        win = "홈"
                    else:
                        win = "무승부"
                    ga1 = Button(label="원정팀 x2.0", custom_id="원정", style=ButtonStyle.blue)
                    ba1 = Button(label="홈팀 x1.95", custom_id="홈", style=ButtonStyle.grey)
                    bo1 = Button(label="무승부 x3.5", custom_id="무승부", style=ButtonStyle.green)

                    embed = discord.Embed(title="가상축구 배팅",
                                            description=f'아래 버튼을 눌러 `가상 축구` 게임에 배팅해 주세요.\n`원정팀 {away}` vs `{home} 홈팀`',
                                            color=0x34c6eb)
                    embed.set_footer(text=서버이름)
                    bet_msg = await message.reply(embed=embed, components=
                    ActionRow(
                        [ga1, ba1, bo1],
                    )
                                                    )
                    while True:
                        try:
                            interaction = await client.wait_for("button_click",
                                                                check=lambda inter: inter.custom_id != "",
                                                                timeout=15)
                        except asyncio.exceptions.TimeoutError:
                            
                            return

                        if message.author.id == interaction.user.id:
                            await bet_msg.delete()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] - amount, interaction.user.id))
                            con.commit()
                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                            con.commit()
                            add_bet(message.author.id,amount)
                            con.close()
                            if amount >= 15000 and win == "원정":
                                ohshittt = await message.reply("슛..! :soccer:")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                
                                point1 = ['1',  '1',  '1',  '2',  '2',  '3',  '4']
                                ezlol = random.choice(point1)
                                embed = discord.Embed(title=f"미적중!",color=0xff0000, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"**```원정 {away} 0 : {ezlol} {home} 홈```**", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"0", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                break
                            elif amount >= 15000 and win == "홈":
                                ohshittt = await message.reply("슛..! :soccer:")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                
                                point1 = ['1',  '1',  '1',  '2',  '2',  '3',  '4']
                                ezlol = random.choice(point1)
                                embed = discord.Embed(title=f"미적중!",color=0xff0000, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"**```원정 {away} {ezlol} : 0 {home} 홈```**", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"0", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                break
                            elif amount >= 15000 and win == "무승부":
                                ohshittt = await message.reply("슛..! :soccer:")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                
                                point1 = ['1',  '1',  '1',  '2',  '2',  '3',  '4']
                                ezlol = random.choice(point1)
                                embed = discord.Embed(title=f"미적중!",color=0xff0000, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"**```원정 {away} {ezlol} : 0 {home} 홈```**", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"0", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                break



                            if interaction.custom_id == "원정" and win == "원정":
                                ohshittt = await message.reply("슛..! :soccer:")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"적중!",color=0x00ff00, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"**```원정 {away} {awaypoint} : {homepoint} {home} 홈```**", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"{math.floor(amount*2)}", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                con = sqlite3.connect("./database/database.db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                user_info = cur.fetchone()

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 2)), message.author.id))
                                con.commit()
                                break
                            elif interaction.custom_id == "홈" and win == "홈":
                                ohshittt = await message.reply("슛..! :soccer:")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"적중!",color=0x00ff00, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"**```원정 {away} {awaypoint} : {homepoint} {home} 홈```**", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"{math.floor(amount*1.95)}", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                con = sqlite3.connect("./database/database.db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                user_info = cur.fetchone()

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 1.95)), message.author.id))
                                con.commit()
                                break
                            elif interaction.custom_id == "무승부" and win == "무승부":
                                ohshittt = await message.reply("슛..! :soccer:")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"적중!",color=0x00ff00, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"**```원정 {away} {awaypoint} : {homepoint} {home} ⚡ 3.5x```**", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"{math.floor(amount*3.5)}", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                con = sqlite3.connect("./database/database.db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                user_info = cur.fetchone()

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 3.5)), message.author.id))
                                con.commit()
                                break
                            else:
                                ohshittt = await message.reply("슛..! :soccer:")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"미적중!",color=0xff0000, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"**```원정 {away} {awaypoint} : {homepoint} {home} 홈```**", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{amount}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"0", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                break

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))



    if message.content.startswith('.라이트닝타조 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    ga1 = Button(label="좌", custom_id="좌", style=ButtonStyle.red)
                    ba1 = Button(label="우", custom_id="우", style=ButtonStyle.blue)

                    embed = discord.Embed(title=":zap: 라이트닝 타조 배팅",
                                            description='아래 버튼을 눌러 `라이트닝 타조` 게임에 배팅해 주세요.',
                                            color=0x34c6eb)
                    embed.set_footer(text="수수료 20%")
                    bet_msg = await message.reply(embed=embed, components=
                    ActionRow(
                        [ga1, ba1],
                    )
                                                    )
                    while True:
                        try:
                            interaction = await client.wait_for("button_click",
                                                                check=lambda inter: inter.custom_id != "",
                                                                timeout=5)
                        except asyncio.exceptions.TimeoutError:
                            return

                        if message.author.id == interaction.user.id:
                            await bet_msg.delete()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] - amount, interaction.user.id))
                            con.commit()
                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount*0.8, message.author.id))
                            con.commit()
                            add_bet(message.author.id,amount)
                            con.close()
                            
                            if interaction.custom_id == "좌":
                                lr = ['좌', '우', '우']
                            elif interaction.custom_id == "우":
                                lr = ['우', '좌', '좌']
                            
                            lg = ['노', '노', '노', '노', '노', '노', '노', '노', '노','노', '노', '노','노', '노', '라', '노','노', '노', '노', '노','노', '노', '노', '노','노']
                            c = random.choice(lr)
                            d = random.choice(lg)
                            betnodot = math.floor(amount*0.8)
                            betlgdot = math.floor(amount*6.4)
                            if amount >= 10000 and interaction.custom_id == c and c == "좌":
                                ohshittt = await message.reply("타조가 어디로 갈까요? 🦄")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"미적중!",color=0xff0000, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"**```우```**", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{betnodot}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"0", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                break
                            elif amount >= 10000 and interaction.custom_id == c and c == "우":
                                ohshittt = await message.reply("타조가 어디로 갈까요? 🦄")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"미적중!",color=0xff0000, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"**```좌```**", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{betnodot}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"0", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                break

                            if interaction.custom_id == c and d == '라':
                                ohshittt = await message.reply("타조가 어디로 갈까요? 🦄")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"적중!",color=0x00ff00, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"```{c} ⚡ 8x```", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{betnodot}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"{betlgdot}", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                con = sqlite3.connect("./database/database.db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                user_info = cur.fetchone()

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 6.4)), message.author.id))
                                con.commit()
                                break
                            if interaction.custom_id == c and d == '노':
                                ohshittt = await message.reply("타조가 어디로 갈까요? 🦄")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"적중!",color=0x00ff00, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"```{c}```", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{betnodot}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"{betnodot}", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                con = sqlite3.connect("./database/database.db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                user_info = cur.fetchone()

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 1.8)), message.author.id))
                                con.commit()
                                break
                            
                            if not (interaction.custom_id == c) and d == '노':
                                ohshittt = await message.reply("타조가 어디로 갈까요? 🦄")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"미적중!",color=0xff0000, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"```{c}```", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{betnodot}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"0", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                break
                            if not (interaction.custom_id == c) and d == '라':
                                ohshittt = await message.reply("타조가 어디로 갈까요? 🦄")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"미적중!",color=0xff0000, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"```{c} ⚡ 8x```", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{betnodot}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"0", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                break

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))


    if message.content.startswith('.라이트닝용호 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    ga1 = Button(label="용", custom_id="용", style=ButtonStyle.red)
                    ba1 = Button(label="호", custom_id="호", style=ButtonStyle.blue)
                    ga11 = Button(label="무승부", custom_id="무", style=ButtonStyle.green)
                    ba11 = Button(label="적절한 무승부", custom_id="적무", style=ButtonStyle.green)
                    x5_card = pick_a_card()
                    x5_card1 = pick_a_card()

                    embed = discord.Embed(title=":zap: 라이트닝 용호 배팅",
                                            description=f'아래 버튼을 눌러 `라이트닝 용호` 게임에 배팅해 주세요.\n라이트닝 카드: `{x5_card}` `{x5_card1}`',
                                            color=0x34c6eb)
                    embed.set_footer(text="수수료 20%")
                    bet_msg = await message.reply(embed=embed, components=
                    ActionRow(
                        [ga1, ba1],
                        [ga11, ba11],
                    )
                                                    )
                    while True:
                        try:
                            interaction = await client.wait_for("button_click",
                                                                check=lambda inter: inter.custom_id != "",
                                                                timeout=5)
                        except asyncio.exceptions.TimeoutError:

                            return

                        if message.author.id == interaction.user.id:
                            await bet_msg.delete()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] - amount, interaction.user.id))
                            con.commit()
                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount*0.8, message.author.id))
                            con.commit()
                            add_bet(message.author.id,amount)
                            con.close()
                            amount = amount
                            bet_pyeon = interaction.custom_id
                            
                            the_charge = amount*4/5
                            yong_card = pick_a_card()
                            ho_card = pick_a_card()
                            amplier = 0
                            win_pyeon = ""
                            given_money = 0
                            if yong_card[0] > ho_card[0]:
                                win_pyeon = "용"
                            elif yong_card[0] < ho_card[0]:
                                win_pyeon = "호"
                            elif yong_card[0] == ho_card[0]:
                                win_pyeon = "무"
                            elif yong_card == ho_card:
                                win_pyeon = "적무"
                            if bet_pyeon == win_pyeon:
                                if win_pyeon == "용":
                                    if yong_card == x5_card or yong_card == x5_card1:
                                        amplier = 5
                                    elif yong_card == x5_card and yong_card == x5_card1:
                                        amplier = 50
                                    else:
                                        amplier = 2
                                elif win_pyeon == "호":
                                    if ho_card == x5_card or ho_card == x5_card1:
                                        amplier = 5
                                    elif ho_card == x5_card and ho_card == x5_card1:
                                        amplier = 50
                                    else:
                                        amplier = 2
                                elif win_pyeon == "무":
                                    if yong_card == x5_card or yong_card == x5_card1:
                                        amplier = 225
                                    elif yong_card == x5_card and yong_card == x5_card1:
                                        amplier = 450
                                    else:
                                        amplier = 16
                                elif win_pyeon == "적무":
                                    if yong_card == x5_card or yong_card == x5_card1:
                                        amplier = 725
                                    elif yong_card == x5_card and yong_card == x5_card1:
                                        amplier = 1450
                                    else:
                                        amplier = 55
                            else:
                                if win_pyeon == "무" or win_pyeon == "적무":
                                    amplier = 0.5
                                else:
                                    amplier = 0
                            given_money = the_charge*amplier
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                            user_info = cur.fetchone()
                            if amplier < 1:
                                ohshittt = await message.reply("배팅 마감되었습니다! :dragon: :tiger:")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"미적중!",color=0xff0000, timestamp=message.created_at)
                                embed.add_field(name=f"카드 결과", value=f"**```용 {yong_card} : {ho_card} 호```**", inline=False)
                                embed.add_field(name=f"결과", value=f"**```{win_pyeon}```**", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{bet_pyeon}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{math.floor(the_charge)}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"{math.floor(given_money)}", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                given_money = the_charge*amplier
                            else:
                                ohshittt = await message.reply("배팅 마감되었습니다! :dragon: :tiger:")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"적중!",color=0x00ff00, timestamp=message.created_at)
                                embed.add_field(name=f"카드 결과", value=f"**```용 {yong_card} : {ho_card} 호```**", inline=False)
                                embed.add_field(name=f"결과", value=f"**```{win_pyeon}```**", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{bet_pyeon}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{math.floor(the_charge)}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"{math.floor(given_money)}", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                given_money = the_charge*amplier

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + given_money), message.author.id))
                                con.commit()

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    

    if message.content.startswith('.라이트닝천악 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    ga1 = Button(label="천사", custom_id="천사", style=ButtonStyle.blue)
                    ba1 = Button(label="악마", custom_id="악마", style=ButtonStyle.red)

                    embed = discord.Embed(title=":zap: 라이트닝 천악 배팅",
                                            description='아래 버튼을 눌러 `라이트닝 천악` 게임에 배팅해 주세요.',
                                            color=0x34c6eb)
                    embed.set_footer(text="수수료 20%")
                    bet_msg = await message.reply(embed=embed, components=
                    ActionRow(
                        [ga1, ba1],
                    )
                                                    )
                    while True:
                        try:
                            interaction = await client.wait_for("button_click",
                                                                check=lambda inter: inter.custom_id != "",
                                                                timeout=5)
                        except asyncio.exceptions.TimeoutError:
                            return

                        if message.author.id == interaction.user.id:
                            await bet_msg.delete()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] - amount, interaction.user.id))
                            con.commit()
                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount*0.8, message.author.id))
                            con.commit()
                            add_bet(message.author.id,amount)
                            con.close()

                            if interaction.custom_id == "천사":
                                lr = ['천사','악마', '악마']
                            elif interaction.custom_id == "악마":
                                lr = ['천사', '천사', '악마']

                            
                            lg = ['라', '노', '노', '노', '노', '노', '노', '노', '노', '노','노', '노', '노', '노','노', '노', '노', '노','노', '노', '노', '노','노', '노', '노', '노','노']
                            c = random.choice(lr)
                            d = random.choice(lg)
                            betnodot = math.floor(amount*0.8)
                            betlgdot = math.floor(amount*6.4)
                            
                            # if amount >= 10000 and interaction.custom_id == c and c == "천사":
                            #     ohshittt = await message.reply("타조가 어디로 갈까요? 🦄")
                            #     await asyncio.sleep(2)
                            #     await ohshittt.delete()
                            #     embed = discord.Embed(title=f"미적중!",color=0xff0000, timestamp=message.created_at)
                            #     embed.add_field(name=f"결과", value=f"**```악마```**", inline=False)
                            #     embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                            #     embed.add_field(name=f"배팅 금액", value=f"{betnodot}", inline=False)
                            #     embed.add_field(name=f"적중 금액", value=f"0", inline=False)
                            #     embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                            #     await message.reply(embed=embed)
                            #     break
                            # elif amount >= 10000 and interaction.custom_id == c and c == "악마":
                            #     ohshittt = await message.reply("타조가 어디로 갈까요? 🦄")
                            #     await asyncio.sleep(2)
                            #     await ohshittt.delete()
                            #     embed = discord.Embed(title=f"미적중!",color=0xff0000, timestamp=message.created_at)
                            #     embed.add_field(name=f"결과", value=f"**```천사```**", inline=False)
                            #     embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                            #     embed.add_field(name=f"배팅 금액", value=f"{betnodot}", inline=False)
                            #     embed.add_field(name=f"적중 금액", value=f"0", inline=False)
                            #     embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                            #     await message.reply(embed=embed)
                            #     break

                            if interaction.custom_id == c and d == '라':
                                ohshittt = await message.reply("천사? :angel: 악마? :smiling_imp:")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"적중!",color=0x00ff00, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"```{c} ⚡ 8x```", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{betnodot}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"{betlgdot}", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                con = sqlite3.connect("./database/database.db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                user_info = cur.fetchone()

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 6.4)), message.author.id))
                                con.commit()
                                break
                            if interaction.custom_id == c and d == '노':
                                ohshittt = await message.reply("천사? :angel: 악마? :smiling_imp:")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"적중!",color=0x00ff00, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"```{c}```", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{betnodot}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"{betnodot}", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                con = sqlite3.connect("./database/database.db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                user_info = cur.fetchone()

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 1.8)), message.author.id))
                                con.commit()
                                break
                            
                            if not (interaction.custom_id == c) and d == '노':
                                ohshittt = await message.reply("천사? :angel: 악마? :smiling_imp:")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"미적중!",color=0xff0000, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"```{c}```", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{betnodot}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"0", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                break
                            if not (interaction.custom_id == c) and d == '라':
                                ohshittt = await message.reply("천사? :angel: 악마? :smiling_imp:")
                                await asyncio.sleep(2)
                                await ohshittt.delete()
                                embed = discord.Embed(title=f"미적중!",color=0xff0000, timestamp=message.created_at)
                                embed.add_field(name=f"결과", value=f"```{c} ⚡ 8x```", inline=False)
                                embed.add_field(name=f"{message.author}", value=f"**```{interaction.custom_id}```**", inline=False)
                                embed.add_field(name=f"배팅 금액", value=f"{betnodot}", inline=False)
                                embed.add_field(name=f"적중 금액", value=f"0", inline=False)
                                embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                await message.reply(embed=embed)
                                break

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))


    if message.content.startswith('.가위바위보 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    ga = Button(label="가위", custom_id="가위", style=ButtonStyle.red)
                    ba = Button(label="바위", custom_id="바위", style=ButtonStyle.green)
                    bo = Button(label="보", custom_id="보", style=ButtonStyle.blue)

                    embed = discord.Embed(title="가위바위보 배팅",
                                            description='아래 버튼을 눌러 `가위바위보` 게임에 배팅해 주세요.',
                                            color=0x34c6eb)
                    embed.set_footer(text=서버이름)
                    bet_msg = await message.reply(embed=embed, components=
                    ActionRow(
                        [ga, ba, bo],
                    )
                                                    )
                    while True:
                        try:
                            interaction = await client.wait_for("button_click",
                                                                check=lambda inter: inter.custom_id != "",
                                                                timeout=5)
                        except asyncio.exceptions.TimeoutError:
                            return

                        if message.author.id == interaction.user.id:
                            await bet_msg.delete()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] - amount, interaction.user.id))
                            con.commit()
                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                            con.commit()
                            con.close()
                            
                            if interaction.custom_id == "가위":
                                a = ['가위','보','바위', '바위', '가위']
                                c = random.choice(a)
                                if c == '가위':
                                    ohshittt = await message.reply("안 내면 진다... 가위 바위 보! :man_raising_hand:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"비겼습니다",color=0xe4f05a, timestamp=message.created_at)
                                    embed.add_field(name=f"BOT", value=f"가위✌", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"가위✌", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.channel.send(embed=embed)
                                    con = sqlite3.connect("./database/database.db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                    user_info = cur.fetchone()

                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 1)), message.author.id))
                                    con.commit()
                                if c == '보':
                                    ohshittt = await message.reply("안 내면 진다... 가위 바위 보! :man_raising_hand:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"{message.author} 승리",color=0xff00, timestamp=message.created_at)
                                    embed.add_field(name=f"BOT", value=f"보🤚", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"가위✌", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.channel.send(embed=embed)
                                    con = sqlite3.connect("./database/database.db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                    user_info = cur.fetchone()
                                    add_bet(message.author.id,amount)

                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 2)), message.author.id))
                                    con.commit()
                                if c == '바위':
                                    ohshittt = await message.reply("안 내면 진다... 가위 바위 보! :man_raising_hand:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"{message.author} 패배",color=discord.Colour.red(), timestamp=message.created_at)
                                    embed.add_field(name=f"BOT", value=f"바위✊", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"가위✌", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.channel.send(embed=embed)
                                    add_bet(message.author.id,amount)
                            elif interaction.custom_id == "바위":
                                a = ['가위','보','바위','보', '바위']
                                c = random.choice(a)
                                if c == '가위':
                                    ohshittt = await message.reply("안 내면 진다... 가위 바위 보! :man_raising_hand:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"{message.author} 승리",color=0xff00, timestamp=message.created_at)
                                    embed.add_field(name=f"BOT", value=f"가위✌", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"바위✊", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.channel.send(embed=embed)
                                    con = sqlite3.connect("./database/database.db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                    user_info = cur.fetchone()

                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 2)), message.author.id))
                                    con.commit()
                                if c == '보':
                                    ohshittt = await message.reply("안 내면 진다... 가위 바위 보! :man_raising_hand:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"{message.author} 패배",color=discord.Colour.red(), timestamp=message.created_at)
                                    embed.add_field(name=f"BOT", value=f"보🤚", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"바위✊", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.channel.send(embed=embed)
                                    add_bet(message.author.id,amount)
                                if c == '바위':
                                    ohshittt = await message.reply("안 내면 진다... 가위 바위 보! :man_raising_hand:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"비겼습니다",color=0xe4f05a, timestamp=message.created_at)
                                    embed.add_field(name=f"BOT", value=f"바위✊", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"바위✊", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.channel.send(embed=embed)
                                    add_bet(message.author.id,amount)
                                    con = sqlite3.connect("./database/database.db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                    user_info = cur.fetchone()

                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 1)), message.author.id))
                                    con.commit()
                            elif interaction.custom_id == "보":
                                a = ['가위','보','바위','가위', '보']
                                c = random.choice(a)
                                if c == '가위':
                                    ohshittt = await message.reply("안 내면 진다... 가위 바위 보! :man_raising_hand:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"{message.author} 패배",color=discord.Colour.red(), timestamp=message.created_at)
                                    embed.add_field(name=f"BOT", value=f"가위✌", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"보🤚", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.channel.send(embed=embed)
                                    add_bet(message.author.id,amount)
                                if c == '보':
                                    ohshittt = await message.reply("안 내면 진다... 가위 바위 보! :man_raising_hand:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    embed = discord.Embed(title=f"비겼습니다",color=0xe4f05a, timestamp=message.created_at)
                                    embed.add_field(name=f"BOT", value=f"보🤚", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"보🤚", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.channel.send(embed=embed)
                                    con = sqlite3.connect("./database/database.db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                    user_info = cur.fetchone()

                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 1)), message.author.id))
                                    con.commit()
                                if c == '바위':
                                    ohshittt = await message.reply("안 내면 진다... 가위 바위 보! :man_raising_hand:")
                                    await asyncio.sleep(2)
                                    await ohshittt.delete()
                                    add_bet(message.author.id,amount)
                                    embed = discord.Embed(title=f"{message.author} 승리",color=0xff00, timestamp=message.created_at)
                                    embed.add_field(name=f"BOT", value=f"바위✊", inline=True)
                                    embed.add_field(name=f"{message.author}", value=f"보🤚", inline=True)
                                    embed.set_footer(text=f"{message.author}", icon_url=message.author.avatar_url)
                                    await message.channel.send(embed=embed)
                                    con = sqlite3.connect("./database/database.db")
                                    cur = con.cursor()
                                    cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                    user_info = cur.fetchone()

                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount * 2)), message.author.id))
                                    con.commit()
                                con.close()
                                break

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.스바a '):
        evobkra_betclose = 0
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    file_path = "evobkrA.txt"
                    # req = requests.get(
                    #     "https://bepick.net/json/game/duyenha.json?" + str(time.time()).split(".")[0], headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()

                    with open(file_path, "r") as file:
                        content = file.read()
                    
                    for value in content:
                        if value == "1":
                            evobkra_betclose = 1
                        elif value == "0":
                            evibkra_betclose = 0

                    if not evobkra_betclose == 1:
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                owrunright = Button(label="플레이어", custom_id="플레이어", style=ButtonStyle.blue)
                                owrunleft = Button(label="뱅커", custom_id="뱅커", style=ButtonStyle.red)
                                xd = Button(label="타이", custom_id="타이", style=ButtonStyle.green)
                                pb = Button(label="플레이어 페어", custom_id="플레이어 페어", style=ButtonStyle.blue)
                                bb = Button(label="뱅커 페어", custom_id="뱅커 페어", style=ButtonStyle.red)

                                embed = discord.Embed(title="✅ 에볼루션 스피드 바카라 A 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [owrunright, owrunleft, xd],
                                    [pb, bb],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        with open(file_path, "r") as file:
                                            content = file.read()
                                        
                                        for value in content:
                                            if value == "1":
                                                evobkra_betclose = 1
                                            elif value == "0":
                                                evibkra_betclose = 0
                                        if evobkra_betclose == 1:
                                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))
                                            return
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evobkrA_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evobkrA_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        con.close()
                                        
                                        add_bet(message.author.id,amount)
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/duyenha', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```에볼루션 스피드 바카라 A / {interaction.custom_id}\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue
                                else:
                                    await bet_msg.delete()

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.스바b '):
        evobkrb_betclose = 0
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    file_path = "evobkrB.txt"
                    # req = requests.get(
                    #     "https://bepick.net/json/game/duyenha.json?" + str(time.time()).split(".")[0], headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()

                    with open(file_path, "r") as file:
                        content = file.read()
                    
                    for value in content:
                        if value == "1":
                            evobkrb_betclose = 1
                        elif value == "0":
                            evibkrb_betclose = 0

                    if not evobkrb_betclose == 1:
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                owrunright = Button(label="플레이어", custom_id="플레이어", style=ButtonStyle.blue)
                                owrunleft = Button(label="뱅커", custom_id="뱅커", style=ButtonStyle.red)
                                xd = Button(label="타이", custom_id="타이", style=ButtonStyle.green)
                                pb = Button(label="플레이어 페어", custom_id="플레이어 페어", style=ButtonStyle.blue)
                                bb = Button(label="뱅커 페어", custom_id="뱅커 페어", style=ButtonStyle.red)

                                embed = discord.Embed(title="✅ 에볼루션 스피드 바카라 B 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [owrunright, owrunleft, xd],
                                    [pb, bb],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        with open(file_path, "r") as file:
                                            content = file.read()
                                        
                                        for value in content:
                                            if value == "1":
                                                evobkrb_betclose = 1
                                            elif value == "0":
                                                evibkrb_betclose = 0
                                        if evobkrb_betclose == 1:
                                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))
                                            return
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evobkrB_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evobkrB_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        con.close()
                                        
                                        add_bet(message.author.id,amount)
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/duyenha', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```에볼루션 스피드 바카라 B / {interaction.custom_id}\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue
                                else:
                                    await bet_msg.delete()

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.식보a '):
        evosicbo_betclose = 0
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    file_path = "evo_sicbo.txt"
                    # req = requests.get(
                    #     "https://bepick.net/json/game/duyenha.json?" + str(time.time()).split(".")[0], headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()

                    with open(file_path, "r") as file:
                        content = file.read()
                    
                    for value in content:
                        if value == "1":
                            evosicbo_betclose = 1
                        elif value == "0":
                            evosicbo_betclose = 0

                    if not evosicbo_betclose == 1:
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                owrunright = Button(label="낮은 수", custom_id="낮은 수", style=ButtonStyle.blue)
                                owrunleft = Button(label="높은 수", custom_id="높은 수", style=ButtonStyle.red)
                                asdjo = Button(label="홀", custom_id="홀수", style=ButtonStyle.blue)
                                qnegqnqk = Button(label="짝", custom_id="짝수", style=ButtonStyle.red)
                                xd = Button(label="모든 트리플", custom_id="모든 트리플", style=ButtonStyle.green)

                                embed = discord.Embed(title="✅ 에볼루션 식보 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [owrunright, owrunleft],
                                    [asdjo, qnegqnqk],
                                    [xd],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        with open(file_path, "r") as file:
                                            content = file.read()
                                        
                                        for value in content:
                                            if value == "1":
                                                evosicbo_betclose = 1
                                            elif value == "0":
                                                evosicbo_betclose = 0
                                        if evosicbo_betclose == 1:
                                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))
                                            return
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evosicbo_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evosicbo_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        con.close()
                                        
                                        add_bet(message.author.id,amount)
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/duyenha', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```에볼루션 식보 / {interaction.custom_id}\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue
                                else:
                                    await bet_msg.delete()

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.판탄 '):
        evosicbo_betclose = 0
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    file_path = "evo_ft.txt"
                    # req = requests.get(
                    #     "https://bepick.net/json/game/duyenha.json?" + str(time.time()).split(".")[0], headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()

                    with open(file_path, "r") as file:
                        content = file.read()
                    
                    for value in content:
                        if value == "1":
                            evosicbo_betclose = 1
                        elif value == "0":
                            evosicbo_betclose = 0

                    if not evosicbo_betclose == 1:
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                one = Button(label="1", custom_id="1", style=ButtonStyle.grey)
                                two = Button(label="2", custom_id="2", style=ButtonStyle.grey)
                                thre = Button(label="3", custom_id="3", style=ButtonStyle.grey)
                                four = Button(label="4", custom_id="4", style=ButtonStyle.grey)
                                owrunright = Button(label="낮은 수", custom_id="낮은 수", style=ButtonStyle.blue)
                                owrunleft = Button(label="높은 수", custom_id="높은 수", style=ButtonStyle.red)
                                asdjo = Button(label="홀", custom_id="홀수", style=ButtonStyle.blue)
                                qnegqnqk = Button(label="짝", custom_id="짝수", style=ButtonStyle.red)

                                embed = discord.Embed(title="✅ 에볼루션 판탄 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [one, two, thre, four],
                                    [owrunright, owrunleft],
                                    [asdjo, qnegqnqk],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        with open(file_path, "r") as file:
                                            content = file.read()
                                        
                                        for value in content:
                                            if value == "1":
                                                evosicbo_betclose = 1
                                            elif value == "0":
                                                evosicbo_betclose = 0
                                        if evosicbo_betclose == 1:
                                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))
                                            return
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evoft_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evoft_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        con.close()
                                        
                                        add_bet(message.author.id,amount)
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/duyenha', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```에볼루션 판탄 / {interaction.custom_id}\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue
                                else:
                                    await bet_msg.delete()

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.룰렛 '):
        evorl_betclose = 0
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    file_path = "evo_rl.txt"
                    # req = requests.get(
                    #     "https://bepick.net/json/game/duyenha.json?" + str(time.time()).split(".")[0], headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()

                    with open(file_path, "r") as file:
                        content = file.read()
                    
                    for value in content:
                        if value == "1":
                            evorl_betclose = 1
                        elif value == "0":
                            evorl_betclose = 0

                    if not evorl_betclose == 1:
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                owrunright = Button(label="레드", custom_id="레드", style=ButtonStyle.red)
                                owrunleft = Button(label="블랙", custom_id="블랙", style=ButtonStyle.grey)
                                xd = Button(label="그린", custom_id="그린", style=ButtonStyle.green)
                                asdjo = Button(label="홀", custom_id="홀수", style=ButtonStyle.blue)
                                qnegqnqk = Button(label="짝", custom_id="짝수", style=ButtonStyle.red)

                                embed = discord.Embed(title="✅ 에볼루션 룰렛 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [owrunright, owrunleft, xd],
                                    [asdjo, qnegqnqk],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        with open(file_path, "r") as file:
                                            content = file.read()
                                        
                                        for value in content:
                                            if value == "1":
                                                evorl_betclose = 1
                                            elif value == "0":
                                                evorl_betclose = 0
                                        if evorl_betclose == 1:
                                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))
                                            return
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evorl_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evorl_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        con.close()
                                        
                                        add_bet(message.author.id,amount)
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/duyenha', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```에볼루션 룰렛 / {interaction.custom_id}\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue
                                else:
                                    await bet_msg.delete()

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.코스바a '):
        evobkra_betclose = 0
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    file_path = "evokoreabkrA.txt"
                    # req = requests.get(
                    #     "https://bepick.net/json/game/duyenha.json?" + str(time.time()).split(".")[0], headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()

                    with open(file_path, "r") as file:
                        content = file.read()
                    
                    for value in content:
                        if value == "1":
                            evobkra_betclose = 1
                        elif value == "0":
                            evibkra_betclose = 0

                    if not evobkra_betclose == 1:
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                owrunright = Button(label="플레이어", custom_id="플레이어", style=ButtonStyle.blue)
                                owrunleft = Button(label="뱅커", custom_id="뱅커", style=ButtonStyle.red)
                                xd = Button(label="타이", custom_id="타이", style=ButtonStyle.green)
                                pb = Button(label="플레이어 페어", custom_id="플레이어 페어", style=ButtonStyle.blue)
                                bb = Button(label="뱅커 페어", custom_id="뱅커 페어", style=ButtonStyle.red)

                                embed = discord.Embed(title="✅ 에볼루션 코리안 스피드 바카라 A 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [owrunright, owrunleft, xd],
                                    [pb, bb],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        with open(file_path, "r") as file:
                                            content = file.read()
                                        
                                        for value in content:
                                            if value == "1":
                                                evobkra_betclose = 1
                                            elif value == "0":
                                                evibkra_betclose = 0
                                        if evobkra_betclose == 1:
                                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))
                                            return
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evokoreabkrA_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evokoreabkrA_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        con.close()
                                        
                                        add_bet(message.author.id,amount)
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/duyenha', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```에볼루션 코리안 스피드 바카라 A / {interaction.custom_id}\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue
                                else:
                                    await bet_msg.delete()

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.코스바b '):
        evobkra1_betclose = 0
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    file_path = "evokoreabkrA.txt"
                    # req = requests.get(
                    #     "https://bepick.net/json/game/duyenha.json?" + str(time.time()).split(".")[0], headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()

                    with open(file_path, "r") as file:
                        content = file.read()
                    
                    for value in content:
                        if value == "1":
                            evobkra_betclose = 1
                        elif value == "0":
                            evibkra_betclose = 0

                    if not evobkra_betclose == 1:
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                owrunright = Button(label="플레이어", custom_id="플레이어", style=ButtonStyle.blue)
                                owrunleft = Button(label="뱅커", custom_id="뱅커", style=ButtonStyle.red)
                                xd = Button(label="타이", custom_id="타이", style=ButtonStyle.green)
                                pb = Button(label="플레이어 페어", custom_id="플레이어 페어", style=ButtonStyle.blue)
                                bb = Button(label="뱅커 페어", custom_id="뱅커 페어", style=ButtonStyle.red)

                                embed = discord.Embed(title="✅ 에볼루션 코리안 스피드 바카라 B 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [owrunright, owrunleft, xd],
                                    [pb, bb],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        with open(file_path, "r") as file:
                                            content = file.read()
                                        
                                        for value in content:
                                            if value == "1":
                                                evobkra_betclose = 1
                                            elif value == "0":
                                                evibkra_betclose = 0
                                        if evobkra_betclose == 1:
                                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))
                                            return
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evokoreabkrB_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evokoreabkrB_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        con.close()
                                        
                                        add_bet(message.author.id,amount)
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/duyenha', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```에볼루션 코리안 스피드 바카라 B / {interaction.custom_id}\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue
                                else:
                                    await bet_msg.delete()

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.용호a '):
        evobkra_betclose = 0
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    file_path = "evo_dragontiger.txt"
                    # req = requests.get(
                    #     "https://bepick.net/json/game/duyenha.json?" + str(time.time()).split(".")[0], headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()

                    with open(file_path, "r") as file:
                        content = file.read()
                    
                    for value in content:
                        if value == "1":
                            evobkra_betclose = 1
                        elif value == "0":
                            evibkra_betclose = 0

                    if not evobkra_betclose == 1:
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                owrunright = Button(label="용", custom_id="용", style=ButtonStyle.red)
                                owrunleft = Button(label="호", custom_id="호", style=ButtonStyle.blue)
                                xd = Button(label="무승부", custom_id="타이", style=ButtonStyle.green)
                                x1d = Button(label="적절한 무", custom_id="적절한 무승부", style=ButtonStyle.green)

                                embed = discord.Embed(title="✅ 에볼루션 용호 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [owrunright, owrunleft, xd, x1d],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        with open(file_path, "r") as file:
                                            content = file.read()
                                        
                                        for value in content:
                                            if value == "1":
                                                evobkra_betclose = 1
                                            elif value == "0":
                                                evibkra_betclose = 0
                                        if evobkra_betclose == 1:
                                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))
                                            return
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evodt_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evodt_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        con.close()
                                        
                                        add_bet(message.author.id,amount)
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/duyenha', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```에볼루션 용호 / {interaction.custom_id}\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue
                                else:
                                    await bet_msg.delete()

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.축구a '):
        evobkra_betclose = 0
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    file_path = "evo_soccer.txt"
                    # req = requests.get(
                    #     "https://bepick.net/json/game/duyenha.json?" + str(time.time()).split(".")[0], headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()

                    with open(file_path, "r") as file:
                        content = file.read()
                    
                    for value in content:
                        if value == "1":
                            evobkra_betclose = 1
                        elif value == "0":
                            evibkra_betclose = 0

                    if not evobkra_betclose == 1:
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                owrunright = Button(label="홈", custom_id="홈", style=ButtonStyle.red)
                                owrunleft = Button(label="어웨이", custom_id="어웨이", style=ButtonStyle.blue)
                                xd = Button(label="무승부", custom_id="타이", style=ButtonStyle.green)

                                embed = discord.Embed(title="✅ 에볼루션 축구 스튜디오 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [owrunright, owrunleft, xd],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        with open(file_path, "r") as file:
                                            content = file.read()
                                        
                                        for value in content:
                                            if value == "1":
                                                evobkra_betclose = 1
                                            elif value == "0":
                                                evibkra_betclose = 0
                                        if evobkra_betclose == 1:
                                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))
                                            return
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evosoccer_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET evosoccer_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        con.close()
                                        
                                        add_bet(message.author.id,amount)
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/duyenha', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```에볼루션 축구 스튜디오 / {interaction.custom_id}\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue
                                else:
                                    await bet_msg.delete()

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.두옌하 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    # req = requests.get(
                    #     "https://bepick.net/json/game/duyenha.json?" + str(time.time()).split(".")[0], headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()

                    url = 'https://bepick.net/json/game/duyenha.json?'

                    # User Agent 설정
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # URL에서 JSON 데이터 가져오기
                    req = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(req)

                    # 응답 데이터 읽기
                    data = response.read()

                    # JSON 데이터를 파이썬 객체로 변환
                    req = json.loads(data)

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 15):
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                owrunright = Button(label="플레이어", custom_id="플레이어", style=ButtonStyle.blue)
                                owrunleft = Button(label="뱅커", custom_id="뱅커", style=ButtonStyle.red)
                                xd = Button(label="타이", custom_id="타이", style=ButtonStyle.green)

                                embed = discord.Embed(title="✅ 두옌하바카라 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [owrunright, owrunleft, xd],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET bakara_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET bakara_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        con.close()
                                        seconds = int(res["nextTime"])-5
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"
                                        add_bet(message.author.id,amount)
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/duyenha', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        url = 'https://bepick.net/live/result/duyenha'

                                        # User Agent 설정
                                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                                        # URL에서 JSON 데이터 가져오기
                                        req = urllib.request.Request(url, headers=headers)
                                        response = urllib.request.urlopen(req)

                                        # 응답 데이터 읽기
                                        data = response.read()

                                        # JSON 데이터를 파이썬 객체로 변환
                                        req = json.loads(data)
                                        roundmsg3 = int(req["round"]) + 1
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{roundmsg6}회차 두옌하 바카라 / {interaction.custom_id}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue
                                else:
                                    await bet_msg.delete()

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.슈마 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    # req = requests.get(
                    #     "https://bepick.net/json/game/jw_supermario.json?" + str(time.time()).split(".")[0], headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()

                    url = 'https://bepick.net/json/game/jw_supermario.json?'

                    # User Agent 설정
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # URL에서 JSON 데이터 가져오기
                    req = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(req)

                    # 응답 데이터 읽기
                    data = response.read()

                    # JSON 데이터를 파이썬 객체로 변환
                    req = json.loads(data)

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 15):
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                un = Button(label="은", custom_id="은", style=ButtonStyle.red)
                                gum = Button(label="금", custom_id="금", style=ButtonStyle.blue)
                                so = Button(label="소", custom_id="소", style=ButtonStyle.blue)
                                dae = Button(label="대", custom_id="대", style=ButtonStyle.red)

                                embed = discord.Embed(title="✅ 슈퍼마리오 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [un, gum],
                                    [so, dae],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET kino_ladder_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET kino_ladder_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        seconds = int(res["nextTime"])-5
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"
                                        con.close()
                                        add_bet(message.author.id,amount)
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/jw_supermario', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        url = 'https://bepick.net/live/result/jw_supermario'

                                        # User Agent 설정
                                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                                        # URL에서 JSON 데이터 가져오기
                                        req = urllib.request.Request(url, headers=headers)
                                        response = urllib.request.urlopen(req)

                                        # 응답 데이터 읽기
                                        data = response.read()

                                        # JSON 데이터를 파이썬 객체로 변환
                                        req = json.loads(data)
                                        roundmsg3 = int(req["round"]) + 1
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{roundmsg3}회차 슈퍼마리오 / {interaction.custom_id}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue
                                else:
                                    await bet_msg.delete()

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.천악 '):
        capick = ""
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    # req = requests.get(
                    #     "https://bepick.net/json/game/jw_angelsdemons.json?" + str(time.time()).split(".")[0], headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()

                    url = 'https://bepick.net/json/game/jw_angelsdemons.json?'

                    # User Agent 설정
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # URL에서 JSON 데이터 가져오기
                    req = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(req)

                    # 응답 데이터 읽기
                    data = response.read()

                    # JSON 데이터를 파이썬 객체로 변환
                    req = json.loads(data)

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 15):
                        if (user_info[12] == None):
                            if not (user_info[5] == 3):
                                mario1 = Button(label="천사", custom_id="천사", style=ButtonStyle.blue)
                                mario2 = Button(label="악마", custom_id="악마", style=ButtonStyle.red)

                                embed = discord.Embed(title="✅ 천사와악마 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [mario1, mario2],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        if interaction.custom_id == "천사":
                                            capick = "천사"
                                        elif interaction.custom_id == "악마":
                                            capick = "악마"
                                        else:
                                            calist = ["천사", "악마"]
                                            capick = random.choice(calist)
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET mario_bet_pick = ? WHERE id == ?;",
                                                    (capick, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET mario_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        con.close()
                                        seconds = int(res["nextTime"])-5
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"
                                        add_bet(message.author.id,amount)
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/jw_angelsdemons', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        url = 'https://bepick.net/live/result/jw_angelsdemons'

                                        # User Agent 설정
                                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                                        # URL에서 JSON 데이터 가져오기
                                        req = urllib.request.Request(url, headers=headers)
                                        response = urllib.request.urlopen(req)

                                        # 응답 데이터 읽기
                                        data = response.read()

                                        # JSON 데이터를 파이썬 객체로 변환
                                        req = json.loads(data)
                                        roundmsg8 = int(req["round"]) + 1
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{roundmsg8}회차 천사와악마 / {capick}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue
                                else:
                                    await bet_msg.delete()

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.보글볼 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    # req = requests.get(
                    #     "https://bepick.net/json/game/bubble_power.json?" + str(time.time()).split(".")[0], headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         # "Host": "ntry.com",
                    #         # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()
                    url = 'https://bepick.net/json/game/bubble_power.json?'

                    # User Agent 설정
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # URL에서 JSON 데이터 가져오기
                    req = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(req)

                    # 응답 데이터 읽기
                    data = response.read()

                    # JSON 데이터를 파이썬 객체로 변환
                    req = json.loads(data)

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
                                button_so = Button(label="소", custom_id="소", style=ButtonStyle.green)
                                button_jung = Button(label="중", custom_id="중", style=ButtonStyle.green)
                                button_dae = Button(label="대", custom_id="대", style=ButtonStyle.green)

                                embed = discord.Embed(title="✅ 보글볼 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [button_first_hole, button_first_zzak, button_first_un, button_first_op],
                                    [button_pa_hole, button_pa_zzak, button_pa_un, button_pa_op],
                                    [button_so, button_jung, button_dae],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET boggle_bet_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        seconds = int(res["nextTime"])-5
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"
                                        cur.execute("UPDATE users SET boggle_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        con.close()
                                        add_bet(message.author.id,amount)
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/bubble_power', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        url = 'https://bepick.net/live/result/bubble_power'

                                        # User Agent 설정
                                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                                        # URL에서 JSON 데이터 가져오기
                                        req = urllib.request.Request(url, headers=headers)
                                        response = urllib.request.urlopen(req)

                                        # 응답 데이터 읽기
                                        data = response.read()

                                        # JSON 데이터를 파이썬 객체로 변환
                                        req = json.loads(data)
                                        roundmsg4 = int(req["round"]) + 1
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{roundmsg4}회차 보글파워볼 / {interaction.custom_id}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.파워볼 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    # req = requests.get(
                    #     "https://bepick.net/json/game/ntry_power.json?" + str(time.time()).split(".")[0], headers={
                    #         "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #         # "Host": "ntry.com",
                    #         # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                    #         "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #         "X-Requested-With": "XMLHttpRequest",
                    #     }).json()

                    url = 'https://bepick.net/json/game/ntry_power.json?'

                    # User Agent 설정
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # URL에서 JSON 데이터 가져오기
                    req = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(req)

                    # 응답 데이터 읽기
                    data = response.read()

                    # JSON 데이터를 파이썬 객체로 변환
                    req = json.loads(data)

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 15):
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
                                button_so = Button(label="소", custom_id="소", style=ButtonStyle.green)
                                button_jung = Button(label="중", custom_id="중", style=ButtonStyle.green)
                                button_dae = Button(label="대", custom_id="대", style=ButtonStyle.green)

                                embed = discord.Embed(title="✅ 파워볼 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [button_first_hole, button_first_zzak, button_first_un, button_first_op],
                                    [button_pa_hole, button_pa_zzak, button_pa_un, button_pa_op],
                                    [button_so, button_jung, button_dae],
                                )
                                                            )
                                while True:
                                    if message.author.id == 1013479428958998528:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "")
                                    else:
                                        try:
                                            interaction = await client.wait_for("button_click",
                                                                                check=lambda
                                                                                    inter: inter.custom_id != "",
                                                                                timeout=5)
                                        except asyncio.exceptions.TimeoutError:
                                            await message.reply(
                                                embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                            await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET pwball_bet_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET pwball_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        con.close()
                                        seconds = int(res["nextTime"])-5
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"
                                        add_bet(message.author.id,amount)
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/ntry_power', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        url = 'https://bepick.net/live/result/ntry_power'

                                        # User Agent 설정
                                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                                        # URL에서 JSON 데이터 가져오기
                                        req = urllib.request.Request(url, headers=headers)
                                        response = urllib.request.urlopen(req)

                                        # 응답 데이터 읽기
                                        data = response.read()

                                        # JSON 데이터를 파이썬 객체로 변환
                                        req = json.loads(data)
                                        roundmsg5 = int(req["round"]) + 1

                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{roundmsg5}회차 파워볼 / {interaction.custom_id}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.이오스1분 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    # req = requests.get("https://bepick.net/json/game/eosball1m.json?" + str(time.time()).split(".")[0],
                    #                 headers={
                    #                     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #                     # "Host": "ntry.com",
                    #                     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                    #                     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #                     "X-Requested-With": "XMLHttpRequest",
                    #                 }).json()

                    url = 'https://bepick.net/json/game/eosball1m.json?'

                    # User Agent 설정
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # URL에서 JSON 데이터 가져오기
                    req = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(req)

                    # 응답 데이터 읽기
                    data = response.read()

                    # JSON 데이터를 파이썬 객체로 변환
                    req = json.loads(data)

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 15):
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
                                button_so = Button(label="소", custom_id="소", style=ButtonStyle.green)
                                button_jung = Button(label="중", custom_id="중", style=ButtonStyle.green)
                                button_dae = Button(label="대", custom_id="대", style=ButtonStyle.green)

                                embed = discord.Embed(title="✅ 이오스1분 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [button_first_hole, button_first_zzak, button_first_un, button_first_op],
                                    [button_pa_hole, button_pa_zzak, button_pa_un, button_pa_op],
                                    [button_so, button_jung, button_dae],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET eos1_bet_pcik = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        add_bet(message.author.id,amount)
                                        cur.execute("UPDATE users SET eos1_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        con.commit()
                                        con.close()
                                        seconds = int(res["nextTime"])-5
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        req = requests.get('https://bepick.net/live/result/eosball1m', headers={
                                            "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                            # "Host": "ntry.com",
                                            # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                            "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                            "X-Requested-With": "XMLHttpRequest",
                                        }).json()
                                        url = 'https://bepick.net/live/result/eosball1m'

                                        # User Agent 설정
                                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                                        # URL에서 JSON 데이터 가져오기
                                        req = urllib.request.Request(url, headers=headers)
                                        response = urllib.request.urlopen(req)

                                        # 응답 데이터 읽기
                                        data = response.read()

                                        # JSON 데이터를 파이썬 객체로 변환
                                        req = json.loads(data)
                                        roundmsg6 = int(req["round"]) + 1
                                        
                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{roundmsg6}회차 이오스1분 / {interaction.custom_id}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.이오스2분 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    # req = requests.get("https://bepick.net/json/game/eosball2m.json?" + str(time.time()).split(".")[0],
                    #                 headers={
                    #                     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #                     # "Host": "ntry.com",
                    #                     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                    #                     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #                     "X-Requested-With": "XMLHttpRequest",
                    #                 }).json()

                    url = 'https://bepick.net/json/game/eosball2m.json?'

                    # User Agent 설정
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # URL에서 JSON 데이터 가져오기
                    req = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(req)

                    # 응답 데이터 읽기
                    data = response.read()

                    # JSON 데이터를 파이썬 객체로 변환
                    req = json.loads(data)

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 15):
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
                                button_so = Button(label="소", custom_id="소", style=ButtonStyle.green)
                                button_jung = Button(label="중", custom_id="중", style=ButtonStyle.green)
                                button_dae = Button(label="대", custom_id="대", style=ButtonStyle.green)

                                embed = discord.Embed(title="✅ 이오스2분 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [button_first_hole, button_first_zzak, button_first_un, button_first_op],
                                    [button_pa_hole, button_pa_zzak, button_pa_un, button_pa_op],
                                    [button_so, button_jung, button_dae],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET eos2_bet_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        add_bet(message.author.id,amount)
                                        cur.execute("UPDATE users SET eos2_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        con.commit()
                                        seconds = int(res["nextTime"])-5
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"
                                        con.close()
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/eosball2m', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        url = 'https://bepick.net/live/result/eosball2m'

                                        # User Agent 설정
                                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                                        # URL에서 JSON 데이터 가져오기
                                        req = urllib.request.Request(url, headers=headers)
                                        response = urllib.request.urlopen(req)

                                        # 응답 데이터 읽기
                                        data = response.read()

                                        # JSON 데이터를 파이썬 객체로 변환
                                        req = json.loads(data)
                                        roundmsg6 = int(req["round"]) + 1

                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{roundmsg6}회차 이오스2분 / {interaction.custom_id}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.이오스3분 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    # req = requests.get("https://bepick.net/json/game/eosball3m.json?" + str(time.time()).split(".")[0],
                    #                 headers={
                    #                     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #                     # "Host": "ntry.com",
                    #                     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                    #                     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #                     "X-Requested-With": "XMLHttpRequest",
                    #                 }).json()

                    url = 'https://bepick.net/json/game/eosball3m.json?'

                    # User Agent 설정
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # URL에서 JSON 데이터 가져오기
                    req = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(req)

                    # 응답 데이터 읽기
                    data = response.read()

                    # JSON 데이터를 파이썬 객체로 변환
                    req = json.loads(data)

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 15):
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
                                button_so = Button(label="소", custom_id="소", style=ButtonStyle.green)
                                button_jung = Button(label="중", custom_id="중", style=ButtonStyle.green)
                                button_dae = Button(label="대", custom_id="대", style=ButtonStyle.green)

                                embed = discord.Embed(title="✅ 이오스3분 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [button_first_hole, button_first_zzak, button_first_un, button_first_op],
                                    [button_pa_hole, button_pa_zzak, button_pa_un, button_pa_op],
                                    [button_so, button_jung, button_dae],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        add_bet(message.author.id,amount)
                                        cur.execute("UPDATE users SET eos3_bet_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET eos3_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        con.commit()
                                        seconds = int(res["nextTime"])-5
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"
                                        con.close()
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/eosball3m', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        url = 'https://bepick.net/live/result/eosball3m'

                                        # User Agent 설정
                                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                                        # URL에서 JSON 데이터 가져오기
                                        req = urllib.request.Request(url, headers=headers)
                                        response = urllib.request.urlopen(req)

                                        # 응답 데이터 읽기
                                        data = response.read()

                                        # JSON 데이터를 파이썬 객체로 변환
                                        req = json.loads(data)
                                        roundmsg6 = int(req["round"]) + 1

                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{roundmsg6}회차 이오스3분 / {interaction.custom_id}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.이오스4분 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    # req = requests.get("https://bepick.net/json/game/eosball4m.json?" + str(time.time()).split(".")[0],
                    #                 headers={
                    #                     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #                     # "Host": "ntry.com",
                    #                     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                    #                     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #                     "X-Requested-With": "XMLHttpRequest",
                    #                 }).json()

                    url = 'https://bepick.net/json/game/eosball4m.json?'

                    # User Agent 설정
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # URL에서 JSON 데이터 가져오기
                    req = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(req)

                    # 응답 데이터 읽기
                    data = response.read()

                    # JSON 데이터를 파이썬 객체로 변환
                    req = json.loads(data)

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 15):
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
                                button_so = Button(label="소", custom_id="소", style=ButtonStyle.green)
                                button_jung = Button(label="중", custom_id="중", style=ButtonStyle.green)
                                button_dae = Button(label="대", custom_id="대", style=ButtonStyle.green)

                                embed = discord.Embed(title="✅ 이오스4분 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [button_first_hole, button_first_zzak, button_first_un, button_first_op],
                                    [button_pa_hole, button_pa_zzak, button_pa_un, button_pa_op],
                                    [button_so, button_jung, button_dae],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
                                        await bet_msg.delete()

                                    if message.author.id == interaction.user.id:
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET eos4_bet_pick = ? WHERE id == ?;",
                                                    (interaction.custom_id, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET eos4_bet_money = ? WHERE id == ?;",
                                                    (amount, interaction.user.id))
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        seconds = int(res["nextTime"])-5
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"
                                        add_bet(message.author.id,amount)
                                        con.close()
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/eosball4m', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        url = 'https://bepick.net/live/result/eosball4m'

                                        # User Agent 설정
                                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                                        # URL에서 JSON 데이터 가져오기
                                        req = urllib.request.Request(url, headers=headers)
                                        response = urllib.request.urlopen(req)

                                        # 응답 데이터 읽기
                                        data = response.read()

                                        # JSON 데이터를 파이썬 객체로 변환
                                        req = json.loads(data)
                                        roundmsg6 = int(req["round"]) + 1

                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{roundmsg6}회차 이오스4분 / {interaction.custom_id}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))


    if message.content.startswith('.이오스5분 '):
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    # req = requests.get("https://bepick.net/json/game/eosball5m.json?" + str(time.time()).split(".")[0],
                    #                 headers={
                    #                     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                    #                     # "Host": "ntry.com",
                    #                     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                    #                     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                    #                     "X-Requested-With": "XMLHttpRequest",
                    #                 }).json()

                    url = 'https://bepick.net/json/game/eosball5m.json?'

                    # User Agent 설정
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                    # URL에서 JSON 데이터 가져오기
                    req = urllib.request.Request(url, headers=headers)
                    response = urllib.request.urlopen(req)

                    # 응답 데이터 읽기
                    data = response.read()

                    # JSON 데이터를 파이썬 객체로 변환
                    req = json.loads(data)

                    res = req['time_set']

                    if not (int(res['nextTime']) <= 15):
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
                                
                                button_so = Button(label="소", custom_id="소", style=ButtonStyle.green)
                                button_jung = Button(label="중", custom_id="중", style=ButtonStyle.green)
                                button_dae = Button(label="대", custom_id="대", style=ButtonStyle.green)

                                embed = discord.Embed(title="✅ 이오스5분 배팅하기",
                                                    description='```배팅할 곳을 선택해주세요.```',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [button_first_hole, button_first_zzak, button_first_un, button_first_op],
                                    [button_pa_hole, button_pa_zzak, button_pa_un, button_pa_op],
                                    [button_so, button_jung, button_dae],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        await message.reply(
                                            embed=talmoembed('🎲 시간 초과', "**버튼은 5초 이내로 누르셔야 합니다.\n다시 시도해주세요.**"))
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
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        seconds = int(res["nextTime"])-5
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"
                                        add_bet(message.author.id,amount)
                                        con.close()
                                        # req = requests.get('http://boglegames.com/game/powerball/ajax.get_live_data.php')
                                        # ress = req.json()['prevGame']
                                        # req = requests.get('https://bepick.net/live/result/eosball5m', headers={
                                        #     "Cookie": f"PHPSESSID=8j6q{random.randint(100, 999)}2vba{random.randint(100, 999)}kgtk626{random.randint(100, 999)}r1; __cfruid=669704593{random.randint(100, 999)}d435{random.randint(100, 999)}191986d7{random.randint(100, 999)}56d704b189-1{random.randint(100, 999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100, 999)}b351cf3a2c9d3f8c570{random.randint(100, 999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100, 999)}21d0{random.randint(100, 999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100, 999)}b33d889e02; _ga=GA1.2.2010{random.randint(100, 999)}188.1651927914; _gid=GA1.2.14{random.randint(100, 999)}60696.16{random.randint(100, 999)}27914",
                                        #     # "Host": "ntry.com",
                                        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
                                        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100, 999)}.54 Safari/537.{random.randint(1, 211)}",
                                        #     "X-Requested-With": "XMLHttpRequest",
                                        # }).json()
                                        url = 'https://bepick.net/live/result/eosball5m'

                                        # User Agent 설정
                                        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

                                        # URL에서 JSON 데이터 가져오기
                                        req = urllib.request.Request(url, headers=headers)
                                        response = urllib.request.urlopen(req)

                                        # 응답 데이터 읽기
                                        data = response.read()

                                        # JSON 데이터를 파이썬 객체로 변환
                                        req = json.loads(data)

                                        roundmsg7 = int(req["round"]) + 1

                                        await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{roundmsg7}회차 이오스5분 / {interaction.custom_id}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))
                                        con.close()
                                        break
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue

                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))

                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))

                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**가입되어 있지 않은 유저입니다.**"))
    if message.content.startswith('.정보'):
        global rolling
        buser_id = 0
        try:
            m = message.content.split(" ")[1]
            m = m.split('@')[1]
            m = m.split('>')[0]
            id = int(m)
            buser_id = int(m)
        except Exception as e:
            id = message.author.id
            buser_id = int(message.author.id)
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
            message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
        user_info = cur.fetchone()

        user = id

        if not (user_info == None):
            con.close()
            try:
                
                if calculate_rolling(buser_id)[1] >= get_rolling(buser_id):
                    if calculate_rolling(buser_id)[1] == 0:
                        bobo = "환전 불가능"
                    else:
                        bobo = "환전 가능"
                else:
                    bobo = "환전 불가능"
                # print(get_bet(buser_id))
                # print(get_chung(buser_id))
                # print(get_rolling(buser_id))
                # print(calculate_rolling(buser_id))
                await message.reply(
                    embed=talmoembed('정보', f"**```보유하신 머니 : {str(user_info[1])}원\n최근 배팅한 금액 : {str(user_info[48])}원\n현재 롤링 : {math.floor(calculate_rolling(buser_id)[1])}% {bobo}```**"))
                pass
            except KeyError:
                await message.reply(
                    embed=talmoembed('정보', f"**```보유하신 머니 : {str(user_info[1])}원\n최근 배팅한 금액 : {str(user_info[48])}원\n현재 롤링 : {math.floor(calculate_rolling(buser_id)[1])}% {bobo}```**"))
                pass
        else:
            con.close()
            await message.reply(embed=talmoembed('실패', "**가입되있지않은 유저입니다.**"))
    
    if message.content.startswith('.롤링'):
        global rolling
        buser_id = 0
        try:
            m = message.content.split(" ")[1]
            m = m.split('@')[1]
            m = m.split('>')[0]
            id = int(m)
            buser_id = int(m)
        except Exception as e:
            id = message.author.id
            buser_id = int(message.author.id)
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
            message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
        user_info = cur.fetchone()

        user = id

        if not (user_info == None):
            con.close()
            try:
                
                if calculate_rolling(buser_id)[1] >= get_rolling(buser_id):
                    if calculate_rolling(buser_id)[1] == 0:
                        bobo = "환전 불가능"
                    else:
                        bobo = "환전 가능"
                else:
                    bobo = "환전 불가능"
                # print(get_bet(buser_id))
                # print(get_chung(buser_id))
                # print(get_rolling(buser_id))
                # print(calculate_rolling(buser_id))
                await message.reply(
                    embed=talmoembed('정보', f"**```현재 롤링 : {math.floor(calculate_rolling(buser_id)[1])}% {bobo}```**"))
                pass
            except KeyError:
                await message.reply(
                    embed=talmoembed('정보', f"**```현재 롤링 : {math.floor(calculate_rolling(buser_id)[1])}% {bobo}```**"))
                pass
        else:
            con.close()
            await message.reply(embed=talmoembed('실패', "**가입되있지않은 유저입니다.**"))
    

    if message.content.startswith('.구버전정보'):
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
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
            message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            con.close()
            await message.reply(
                embed=talmoembed('정보', f"**```보유하신 머니 : {str(user_info[1])}원```**"))
        else:
            con.close()
            await message.reply(embed=talmoembed('실패', "**가입되있지않은 유저입니다.**"))
    if message.content.startswith('!롤링초기화'):
        if message.author.id in admin_id:
            try:
                m = message.content.split(" ")[1]
                m = m.split('@')[1]
                m = m.split('>')[0]
                id = int(m)
            except Exception as e:
                await message.reply(embed=talmoembed('실패', "**초기화할 대상을 멘션해주세요.**"))
                
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
            user_info = cur.fetchone()

            if (user_info == None):
                cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0))
                con.commit()
                con.close()

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                con.close()
                reset_rolling_stat(id)
                await message.reply(
                    embed=talmoembed('완료', f"**```성공적으로 롤링이 초기화 되었습니다.```**"))
            else:
                con.close()
                await message.reply(embed=talmoembed('실패', "**가입되있지않은 유저입니다.**"))
    if message.content.startswith('!충전액'):
        if message.author.id in admin_id:
            try:
                m = message.content.split(" ")[1]
                amount = message.content.split(" ")[2]
                m = m.split('@')[1]
                m = m.split('>')[0]
                id = int(m)
            except Exception as e:
                await message.reply(embed=talmoembed('실패', "**수정할 대상을 멘션해주세요.**"))
                
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
            user_info = cur.fetchone()

            if (user_info == None):
                cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0))
                con.commit()
                con.close()

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                con.close()
                # reset_rolling_stat(id)
                # write_bet(message.author.id,0)
                # write_rolling(message.author.id,bonus_rolling)
                add_chung1(id,float(amount))
                await message.reply(
                    embed=talmoembed('완료', f"**```성공적으로 충전액이 {amount}원으로 수정 되었습니다.```**"))
            else:
                con.close()
                await message.reply(embed=talmoembed('실패', "**가입되있지않은 유저입니다.**"))
    if message.content.startswith('!롤링설정'):
        if message.author.id in admin_id:
            try:
                m = message.content.split(" ")[1]
                amount = message.content.split(" ")[2]
                m = m.split('@')[1]
                m = m.split('>')[0]
                id = int(m)
            except Exception as e:
                await message.reply(embed=talmoembed('실패', "**수정할 대상을 멘션해주세요.**"))
                
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
            user_info = cur.fetchone()

            if (user_info == None):
                cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0))
                con.commit()
                con.close()

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                con.close()
                # reset_rolling_stat(id)
                # write_bet(message.author.id,0)
                write_rolling(id,amount)
                # add_chung1(id,float(amount))
                await message.reply(
                    embed=talmoembed('완료', f"**```성공적으로 롤링이 {amount}%으로 수정 되었습니다.```**"))
            else:
                con.close()
                await message.reply(embed=talmoembed('실패', "**가입되있지않은 유저입니다.**"))
    if message.content.startswith('!배팅액'):
        if message.author.id in admin_id:
            try:
                m = message.content.split(" ")[1]
                amount = message.content.split(" ")[2]
                m = m.split('@')[1]
                m = m.split('>')[0]
                id = int(m)
            except Exception as e:
                await message.reply(embed=talmoembed('실패', "**수정할 대상을 멘션해주세요.**"))
                
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
            user_info = cur.fetchone()

            if (user_info == None):
                cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                message.author.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 0))
                con.commit()
                con.close()

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                con.close()
                # reset_rolling_stat(id)
                write_bet(id,amount)
                # write_rolling(id,amount)
                # add_chung1(id,float(amount))
                await message.reply(
                    embed=talmoembed('완료', f"**```성공적으로 배팅액이 {amount}원 추가 되었습니다.```**"))
            else:
                con.close()
                await message.reply(embed=talmoembed('실패', "**가입되있지않은 유저입니다.**"))

    if message.content.startswith('.충전 '):
        log_id = 출금로그
        log_ch = client.get_channel(int(log_id))
        if message.author.id in admin_id:
            try:
                user_id = message.mentions[0].id
                amount = int(message.content.split(" ")[2])
            except:
                con.close()
                await message.reply(embed=talmoembed('실패', "**정확하게 명령어를 입력해주세요!**"))
                return

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] + amount, user_id))
                
                write_rolling(user_id,rolling)
                write_chung(user_id,float(amount))
                con.commit()
                ktotal += int(amount)
                await message.reply(embed=talmoembed('충전성공',
                                                    f"{str(amount)}원 충전 성공\n\n{str(user_info[1])}원 -> {str(user_info[1] + amount)}원"))
                await log_ch.send(f"<@{message.mentions[0].id}>님이 {amount}원을 충전하셨습니다")
            else:
                con.close()
                await message.channel.send(embed=talmoembed("충전실패", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.환전 '):
        if message.author.id in admin_id:
            try:
                user_id = message.mentions[0].id
                amount = int(message.content.split(" ")[2])
            except:
                con.close()
                await message.reply(embed=talmoembed('실패', "**정확하게 명령어를 입력해주세요!**"))
                return

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] - amount, user_id))
                con.commit()
                moneytotal -= int(amount)
                await message.delete()
                userss = await client.fetch_user(user_id)
                await userss.send(embed=bet_embed('😎 환전 완료!', f"요청하신 금액 **`{amount}원`**이 성공적으로 계좌로 출금되었습니다."))
                res = getinfo(user_id)
                webhook = DiscordWebhook(
                    url=출금로그웹훅,
                    username='환전로그',
                    avatar_url=f"https://cdn.discordapp.com/avatars/{user_id}/{res['avatar']}.webp?size=80",
                    content=f'<@{user_id}> 님이 {amount}원을 환전하셨습니다.')
                webhook.execute()
                webhook = DiscordWebhook(
                    url="https://discord.com/api/webhooks/1119571905830191114/mFxVHE4pJeGAqB_nVr42GbiJSU34kt_zbYndydlez8vEFLqMF4moKF86q-b9I2fQ3IfF",
                    username='환전로그',
                    avatar_url=f"https://cdn.discordapp.com/avatars/{user_id}/{res['avatar']}.webp?size=80",
                    content=f'<@{user_id}> 님이 {amount}원을 환전하셨습니다.')
                webhook.execute()
            else:
                con.close()
                await message.channel.send(embed=talmoembed("차감실패", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.강제충전 '):
        log_id = 출금로그
        log_ch = client.get_channel(int(log_id))
        if message.author.id in admin_id:
            try:
                user_id = message.mentions[0].id
                amount = int(message.content.split(" ")[2])
            except:
                con.close()
                await message.reply(embed=talmoembed('실패', "**정확하게 명령어를 입력해주세요!**"))
                return

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] + amount, user_id))

                con.commit()
                await message.reply(embed=talmoembed('충전성공',
                                                    f"```{str(amount)}원 강제충전 성공\n\n{str(user_info[1])}원 -> {str(user_info[1] + amount)}원```"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("충전실패", "**가입되어 있지 않은 유저입니다.**"))

    # if message.content.startswith('.ㅈㅈ '):
    #     log_id = 출금로그
    #     log_ch = client.get_channel(int(log_id))
    #     if message.author.id in admin_id:
    #         try:
    #             user_id = message.mentions[0].id
    #             amount = int(message.content.split(" ")[2])
    #         except:
    #             con.close()
    #             await message.reply(embed=talmoembed('실패', "**정확하게 명령어를 입력해주세요!**"))
    #             return

    #         con = sqlite3.connect("./database/database.db")
    #         cur = con.cursor()
    #         cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
    #         user_info = cur.fetchone()

    #         if not (user_info == None):
    #             cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] + amount, user_id))

    #             con.commit()
    #             await message.delete()
    #             userss = await client.fetch_user(user_id)
    #             await userss.send(embed=discord.Embed(title="적중", description=f"배팅 게임 : 라이브 카지노\n─────────────\n적중 금액 : {amount}\n남은 금액 : {user_info[1]+amount}", color=0x00ff00))
    #         else:
    #             con.close()
    #             await message.channel.send(embed=talmoembed("충전실패", "**가입되어 있지 않은 유저입니다.**"))

    # if message.content.startswith('.테스트머니'):

    #     con = sqlite3.connect("./database/database.db")
    #     cur = con.cursor()
    #     cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
    #     user_info = cur.fetchone()

    #     if not (user_info == None):
    #         cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] + 1000000, message.author.id))

    #         con.commit()
    #         await message.reply(embed=talmoembed('지급 완료',
    #                                             f"```1000000원 지갑 송금 완료!\n테스트가 완료되면 자동으로 몰수돼요.```"))
    #     else:
    #         con.close()
    #         await message.channel.send(embed=talmoembed("충전실패", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.송금 '):
        # try:
        #     user_id = message.mentions[0].id
        #     amount = int(message.content.split(" ")[2])
        # except:
        #     con.close()
        #     await message.reply(embed=talmoembed('실패', "**정확하게 명령어를 입력해주세요.\n.송금 @멘션 금액**"))
        #     return

        # con = sqlite3.connect("./database/database.db")
        # cur = con.cursor()
        # cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        # user_info = cur.fetchone()
        # con1 = sqlite3.connect("./database/database.db")
        # cur1 = con1.cursor()
        # cur1.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        # user_info1 = cur1.fetchone()
        # susuro = amount*1.1
        # if amount > 0:
        #     if user_info1[1] < susuro:
        #         await message.reply(embed=talmoembed('실패', "**잔액이 부족합니다.\n수수료 10%와 같이 부과되니 다시 확인해주세요.**"))
        #         return
                
        #     if not (user_info == None):
        #         cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] + amount, user_id))

        #         con.commit()
        #         cur1.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info1[1] - susuro, message.author.id))
        #         con1.commit()
        #         await message.reply(embed=talmoembed('✅ 송금 완료',
        #                                             f"**{str(amount)}원이 <@{user_id}>님에게 송금되었습니다.\n수수료 {amount*0.1}원이 차감되었습니다.**"))
        #         userss = await client.fetch_user(user_id)
        #         await userss.send(embed=talmoembed("이체 받음", f"**{amount}원이 내 알파머니로 입금되었어요.\n입금자 : <@{message.author.id}>**"))
                        
        #     else:
        #         con.close()
        #         await message.channel.send(embed=talmoembed("충전실패", "**가입되어 있지 않은 유저입니다.**"))
        # else:
        #     con.close()
        await message.channel.send(embed=talmoembed("🎲 송금 근황", "**```아쉽게도, 송금 시스템은 5월 14일 부로 삭제 되었습니다.```**"))

    if message.content.startswith('.몰수 '):
        if message.author.id in admin_id:
            try:
                user_id = message.mentions[0].id
                reason = message.content[26:]
            except:
                con.close()
                await message.reply(embed=talmoembed('실패', "**정확하게 명령어를 입력해주세요!\n.몰수 @멘션 사유**"))
                return

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (0, user_id))

                con.commit()
                await message.reply(embed=talmoembed('🤖 몰수 성공',
                                                    f"```{str(user_info[1])}원 몰수 성공\n\n{str(user_info[1])}원 -> 0원```"))
                userss = await client.fetch_user(user_id)
                await userss.send(embed=talmoembed("🤖 몰수 안내", f"**{str(user_info[1])}원이 몰수되었습니다.\n사유 : {reason}\n\n`자세한 이유는 관리자에게 문의하세요!`**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("충전실패", "**가입되어 있지 않은 유저입니다.**"))

    if message.content.startswith('.강제차감 '):
        if message.author.id in admin_id:
            try:
                user_id = message.mentions[0].id
                amount = int(message.content.split(" ")[2])
            except:
                con.close()
                await message.reply(embed=talmoembed('실패', "**정확하게 명령어를 입력해주세요!**"))
                return

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] - amount, user_id))
                con.commit()
                await message.reply(embed=talmoembed('차감성공',
                                                    f"{str(amount)}원 강제차감 성공\n\n{str(user_info[1])}원 -> {str(user_info[1] - amount)}원"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("차감실패", "**가입되어 있지 않은 유저입니다.**"))

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
                await message.reply(embed=talmoembed('추가성공', "**성공적으로 블랙리스트 추가를 완료하였습니다!**"))
                userss = await client.fetch_user(user_id)
                await userss.send(embed=talmoembed("🎓 블랙리스트 안내", f"**관리자에 의해 블랙 유저 처리되셨습니다.**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("추가실패", "**가입되어 있지 않은 유저입니다.**"))

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
                await message.reply(embed=talmoembed('추가성공', "**성공적으로 화이트리스트 추가를 완료하였습니다!**"))
                userss = await client.fetch_user(user_id)
                await userss.send(embed=talmoembed("🎓 화이트리스트 안내", f"**관리자에 의해 블랙 유저 삭제 처리 되셨습니다.**"))
            else:
                con.close()
                await message.channel.send(embed=talmoembed("추가실패", "**가입되어 있지 않은 유저입니다.**"))
    if message.content == '!수익':
        if message.author.id in admin_id:
            embed = discord.Embed(title="오늘 수익",
                                description=f"계좌수익 : {ktotal}\n\n환전해준돈 : {moneytotal}\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\n총 수익 : {ktotal + moneytotal}",
                                color=0x2f3136)
            await message.channel.send(embed=embed)
    if message.content == '!초기화 수익':
        if message.author.id in admin_id:
            ktotal = 0
            moneytotal = 0
            message.channel.send('완료샤!')
        else:
            message.channel.send(':middle_finger: ')
    if message.content == "!용호":
        if message.author.id in admin_id:
            rs_pe = client.get_channel(용호회차)
            pe_rs = await rs_pe.send(f"`1회차`가 진행되고있습니다.")

            if dt_on == 0:
                await message.channel.send(f"<#{용호채널}> 에 게임이 시작됩니다.")
                dt_on = 1
                dt_round = 0
                while True:
                    dt_round += 1
                    if dt_round == 500:
                        dt_round = 1
                    else:
                        pass
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
                    bet_embed = discord.Embed(title=f"{dt_round}회차 용호 배팅 시간입니다.",
                                                description=f"용, 호, 또는 무승부에 배팅 해주십시오.\n남은 배팅시간 : `{tim}`",
                                                color=0x34c6eb)
                    bet_embed.set_footer(text=서버이름)
                    bet_msg = await dt_ch.send(embed=bet_embed)
                    for i in range(0, 12):
                        await asyncio.sleep(5)
                        tim -= 5
                        bet_embed = discord.Embed(title=f"{dt_round}회차 용호 배팅 시간입니다.",
                                                    description=f"용, 호, 또는 무승부에 배팅 해주십시오.\n남은 배팅시간 : `{tim}`",
                                                    color=0x34c6eb)
                        bet_embed.set_footer(text=서버이름)
                        await bet_msg.delete()
                        bet_msg = await dt_ch.send(embed=bet_embed)
                    dt_total_d = 0
                    dt_total_t = 0
                    close_embed = discord.Embed(title=f"{dt_round}회차 배팅이 마감되었습니다", description=f'''
        ```d
        🐲 용  ||  🐯 호

        {d_card}     //     {t_card}
        ```
        ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        **🐲 용 : {d_card} {"✅" if d_card > t_card else ""}   {"< 승리! > X2배" if d_card > t_card else ""}\n
        🐯 호 : {t_card}   {"✅" if d_card < t_card else ""}   {"< 승리! > X2배" if d_card < t_card else ""}\n
        🟢 무승부{"< 승리! > X9배" if d_card == t_card else ""}**''', color=0x34c6eb)
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
                            
                            user = await client.fetch_user(f"{i[0]}")
                            await user.send(embed=discord.Embed(title="적중", description=f"배팅 게임 : 용호 (카지노)\n배팅 회차 : {dt_round}\n배팅 내역 : {i[18]}\n배팅 금액 : {i[19]}원\n─────────────\n적중 금액 : {round(i[19] * (배당-1))}\n남은 금액 : {i[1] + round(i[19] * 배당)}",color=0x00ff00))
                            
                            bet_log += (f"**<@{i[0]}> {i[18]} {round(i[19] * 배당)} 적중**\n")
                            c.execute("UPDATE users SET money = money + ? where id=?", (round(i[19] * 배당), i[0],))
                        elif result == "무승부":
                            user = await client.fetch_user(f"{i[0]}")
                            await user.send(embed=discord.Embed(title="무승부", description=f"배팅 게임 : 용호 (카지노)\n배팅 회차 : {bkr_round}\n배팅 내역 : {i[24]}\n배팅 금액 : {i[25]}원\n─────────────\n적중 금액 : {round(i[19] // 2)}\n남은 금액 : {i[1] + round(i[19] // 2)}"))
                            
                            bet_log += (f"**<@{i[0]}> {i[18]} {round(i[19] // 2)} 무승부**\n")
                            c.execute("UPDATE users SET money = money + ? where id=?",
                                    (round(i[19] // 2), i[0],))
                        else:
                            user = await client.fetch_user(f"{i[0]}")
                            await user.send(embed=discord.Embed(title="미적중", description=f"배팅 게임 : 용호 (카지노)\n배팅 회차 : {dt_round}\n배팅 내역 : {i[18]}\n배팅 금액 : {i[19]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {i[1]}",color=0xff0000))
                            
                            bet_log += (f"**<@{i[0]}> {i[18]} 미적중**\n")

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
                    await pe_rs.edit(embed=discord.Embed(title=f"용호 회차", description=f"{round_rs}",color=0x34c6eb))

    if message.content.startswith('.용호 '):
        if dt_on != 0:
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()
            if not user_info[5] == 3:
                if message.content.split(" ")[1] == "올인":
                    if (int(user_info[1]) >= 500):
                        amount = int(user_info[1])
                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
                else:
                    try:
                        amount = int(message.content.split(" ")[1])
                    except:
                        con.close()
                        await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**금액은 정수만 배팅이 가능합니다.**"))
                        return
                if not amount < 500:
                    if user_info[1] >= amount:
                        if tim > 15:
                            choice = message.content.split(" ")[1]
                            if not message.author.id in doing_bet4:
                                yong = Button(label="용", custom_id="용", style=ButtonStyle.red)
                                ho = Button(label="호", custom_id="호", style=ButtonStyle.blue)
                                tie = Button(label="무승부", custom_id="무승부", style=ButtonStyle.green)

                                embed = discord.Embed(title="배팅하기",
                                                    description='**용호 카지노 배팅하기**\n**배팅할 곳의 버튼을 클릭하여 배팅해주세요.**',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [yong, ho, tie],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        return

                                    if message.author.id == interaction.user.id:
                                        doing_bet4.append(message.author.id)
                                        if user_info[1] >= 500:
                                            dt_total_d = 0
                                            choice = interaction.custom_id
                                            dt_total_t = 0

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
                                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                        (amount, message.author.id))
                                            con.commit()
                                            
                                            seconds = int(tim)
                                            minutes = seconds // 60
                                            remaining_seconds = seconds % 60

                                            if minutes > 0:
                                                if remaining_seconds > 0:
                                                    iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                                else:
                                                    iwannadosex = f"{minutes}분"
                                            else:
                                                iwannadosex = f"{seconds}초"
                                            add_bet(message.author.id,amount)
                                            con.close()
                                            await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{dt_round}회차 용호 / {choice}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))


                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.```**"))
                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
        else:
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```게임이 진행중이지 않습니다.```**"))


    if message.content == "!바카라":
        if message.author.id in admin_id:
            rs_pe = client.get_channel(바카라회차)
            pe_rs = await rs_pe.send(f"`1회차`가 진행되고있습니다.")
            round_rs = ''
            leng = 0

            if bakara_on == 0:
                await message.channel.send(f"<#{바카라채널}> 에 게임이 시작됩니다.")
                bakara_on = 1
                bkr_round = 0
                while True:
                    bkr_round += 1
                    if bkr_round == 500:
                        bkr_round = 1
                    else:
                        pass
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
                    bet_embed = discord.Embed(title=f"{bkr_round}회차 바카라 배팅 시간입니다.",
                                              description=f"플레이어, 뱅커, 또는 무승부에 배팅해주십시오.\n남은 배팅시간 : `{ti}`",
                                              color=0x00C9FF)
                    bet_embed.set_footer(text=서버이름)
                    bet_msg = await bkr_ch.send(embed=bet_embed)
                    for i in range(0, 12):
                        await asyncio.sleep(5)
                        ti -= 5
                        bet_embed = discord.Embed(title=f"{bkr_round}회차 바카라 배팅 시간입니다.",
                                                  description=f"플레이어, 뱅커, 또는 무승부에 배팅해주십시오.\n남은 배팅시간 : `{ti}`",
                                                  color=0x00C9FF)
                        bet_embed.set_footer(text=서버이름)
                        await bet_msg.delete()
                        bet_msg = await bkr_ch.send(embed=bet_embed)
                    close_embed = discord.Embed(title=f"{bkr_round}회차 배팅이 마감되었습니다", description=f'''
        ```
        🔵플레이어  ||  🔴뱅커

        {player_card} ,  ? ,  ?  //   ? ,  ? ,  ?
        ```
        ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        **🔵플레이어 : 카드 공개중...
        🔴뱅커 : 카드 공개중...
        🟢무승부 : 카드 공개중...**''', color=0x34c6eb)
                    await asyncio.sleep(1)
                    await bet_msg.edit(embed=close_embed, components="")
                    close_embed = discord.Embed(title=f"{bkr_round}회차 배팅이 마감되었습니다", description=f'''
        ```
        🔵플레이어  ||  🔴뱅커

        {player_card} ,  ? ,  ?  //   {banker_card} ,  ? ,  ?
        ```
        ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        **🔵플레이어 : 카드 공개중...
        🔴뱅커 : 카드 공개중...
        🟢무승부 : 카드 공개중...**''', color=0x34c6eb)
                    await asyncio.sleep(1)
                    await bet_msg.edit(embed=close_embed, components="")
                    close_embed = discord.Embed(title=f"{bkr_round}회차 배팅이 마감되었습니다", description=f'''
        ```
        🔵플레이어  ||  🔴뱅커

        {player_card} ,  {player_card2} ,  ?  //   {banker_card} ,  ? ,  ?
        ```
        ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        **🔵플레이어 : 카드 공개중...
        🔴뱅커 : 카드 공개중...
        🟢무승부 : 카드 공개중...**''', color=0x34c6eb)
                    await asyncio.sleep(1)
                    await bet_msg.edit(embed=close_embed, components="")
                    close_embed = discord.Embed(title=f"{bkr_round}회차 배팅이 마감되었습니다", description=f'''
        ```
        🔵플레이어  ||  🔴뱅커

        {player_card} ,  {player_card2} ,  ?  //   {banker_card} ,  {banker_card2} ,  ?
        ```
        ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        **🔵플레이어 : 카드 공개중...
        🔴뱅커 : 카드 공개중...
        🟢무승부 : 카드 공개중...**''', color=0x34c6eb)
                    await asyncio.sleep(1)
                    await bet_msg.edit(embed=close_embed, components="")
                    close_embed = discord.Embed(title=f"{bkr_round}회차 배팅이 마감되었습니다", description=f'''
        ```
        🔵플레이어  ||  🔴뱅커

        {player_card} ,  {player_card2} ,  {p_add_card if p_add_card != 0 else ""}  //   {banker_card} ,  {banker_card2} ,  {b_add_card if b_add_card != 0 else ""}
        ```
        ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        **🔵플레이어 : {p} {"✅" if p > b else ""}   {"< 승리! > X2배" if p > b else ""}\n
        🔴뱅커 : {b}   {"✅" if p < b else ""}   {"< 승리! > X1.95배" if p < b else ""}\n
        🟢무승부{"< 승리! > X9배" if p == b else ""}**''', color=0x34c6eb)
                    await bet_msg.edit(embed=close_embed, components="")
                    bet_log = ""
                    result = "플레이어" if p > b else '뱅커' if b > p else '무승부'
                    conn = sqlite3.connect('./database/database.db')
                    c = conn.cursor()
                    list_a = list(c.execute("SELECT * FROM users"))
                    
                    for i in list_a:
                        # con = sqlite3.connect("./database/database.db")
                        # cur = con.cursor()
                        # cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                        # user_info = cur.fetchone()
                        # user = client.get_user(i)
                        if (i[24] == None):
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
                            user = await client.fetch_user(f"{i[0]}")
                            await user.send(embed=discord.Embed(title="적중", description=f"배팅 게임 : 바카라 (카지노)\n배팅 회차 : {bkr_round}\n배팅 내역 : {i[24]}\n배팅 금액 : {i[25]}원\n─────────────\n적중 금액 : {round(i[25] * (배당-1))}\n남은 금액 : {i[1] + round(i[25] * 배당)}",color=0x00ff00))
                            
                            bet_log += (f"**<@{i[0]}> {i[24]} {round(i[25] * 배당)} 적중**\n")
                            c.execute("UPDATE users SET money = money + ? where id=?", (round(i[25] * 배당), i[0],))
                            # await user.send(embed=discord.Embed(title="적중", description=f"배팅 게임 : 바카라 (카지노)\n배팅 회차 : {bkr_round}\n배팅 내역 : {i[24]}\n배팅 금액 : {i[25]}원\n─────────────\n적중 금액 : {round(i[25] * (배당-1))}\n남은 금액 : {user_info[1] + round(i[25] * 배당)}",color=0x00ff00))
                            
                        elif result == "무승부":
                            user = await client.fetch_user(f"{i[0]}")
                            await user.send(embed=discord.Embed(title="무승부", description=f"배팅 게임 : 바카라 (카지노)\n배팅 회차 : {bkr_round}\n배팅 내역 : {i[24]}\n배팅 금액 : {i[25]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {i[1] + round(i[25])}"))
                            
                            bet_log += (f"**<@{i[0]}> {i[24]} {round(i[25])} 무승부**\n")
                            c.execute("UPDATE users SET money = money + ? where id=?",
                                      (round(i[25] * 1), i[0],))
                            # await user.send(embed=discord.Embed(title="무승부", description=f"배팅 게임 : 바카라 (카지노)\n배팅 회차 : {bkr_round}\n배팅 내역 : {i[24]}\n배팅 금액 : {i[25]}원\n─────────────\n적중 금액 : {round(i[25] * 1)}\n남은 금액 : {user_info[1]}",color=0xff0000))
                        else:
                            user = await client.fetch_user(f"{i[0]}")
                            await user.send(embed=discord.Embed(title="미적중", description=f"배팅 게임 : 바카라 (카지노)\n배팅 회차 : {bkr_round}\n배팅 내역 : {i[24]}\n배팅 금액 : {i[25]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {i[1]}",color=0xff0000))
                            
                            # await user.send(embed=discord.Embed(title="미적중", description=f"배팅 게임 : 바카라 (카지노)\n배팅 회차 : {bkr_round}\n배팅 내역 : {i[24]}\n배팅 금액 : {i[25]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {user_info    [1]}",color=0xff0000))
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
                    leng += 1
                    if leng >= 60:
                        round_rs = "**🎨 결과값 초기화 🎨**"
                        leng = 0
                    round_rs += f"\n\n`{bkr_round}회차` 결과 : **{result}**"
                    doing_bet2 = []
                    oplog = ''
                    ch = client.get_channel(바카라배팅내역)
                    await ch.send(embed=discord.Embed(title=f"{bkr_round}회차 바카라 배팅내역", description=f"{bet_log}",color=0x34c6eb))
                    await pe_rs.edit(embed=discord.Embed(title=f"바카라 회차", description=f"{round_rs}",color=0x34c6eb))
    if message.content.startswith('.바카라 '):
        if bakara_on != 0:
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
                        await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                else:
                    amount = int(message.content.split(" ")[1])
                if not amount < 1000:
                    if user_info[1] >= amount:
                        if not ti < 15:
                            player = Button(label="플레이어", custom_id="플", style=ButtonStyle.blue)
                            banker = Button(label="뱅커", custom_id="뱅", style=ButtonStyle.red)
                            tie = Button(label="무승부", custom_id="무", style=ButtonStyle.green)

                            embed = discord.Embed(title="배팅하기",
                                                description='**바카라 카지노 배팅하기**\n**배팅할 곳의 버튼을 클릭하여 배팅해주세요.**',
                                                color=0x2f3136)
                            embed.set_footer(text=서버이름)
                            bet_msg = await message.reply(embed=embed, components=
                            ActionRow(
                                [player, banker, tie],
                            )
                                                        )
                            while True:
                                try:
                                    interaction = await client.wait_for("button_click",
                                                                        check=lambda inter: inter.custom_id != "",
                                                                        timeout=5)
                                except asyncio.exceptions.TimeoutError:
                                    return

                                if message.author.id == interaction.user.id:
                                    if not message.author.id in doing_bet2:
                                        doing_bet2.append(message.author.id)
                                        if user_info[1] >= 1000:
                                            choice = interaction.custom_id
                                            await bet_msg.delete()
                                            add_bet(message.author.id, amount)

                                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                        (user_info[1] - int(amount), message.author.id))
                                            if choice == "플":
                                                choice = "플레이어"
                                            elif choice == "뱅":
                                                choice = "뱅커"
                                            else:
                                                choice = "무승부"
                                            cur.execute("UPDATE users SET rotoladder_bet_pick = ? WHERE id == ?;",
                                                        (choice, message.author.id))
                                            cur.execute("UPDATE users SET rotoladder_bet_money = ? WHERE id == ?;",
                                                        (amount, message.author.id))
                                            con.commit()
                                            con.close()
                                            seconds = int(ti)
                                            minutes = seconds // 60
                                            remaining_seconds = seconds % 60

                                            if minutes > 0:
                                                if remaining_seconds > 0:
                                                    iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                                else:
                                                    iwannadosex = f"{minutes}분"
                                            else:
                                                iwannadosex = f"{seconds}초"
                                            await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{bkr_round}회차 바카라 / {choice}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))

                                        else:
                                            con.close()
                                            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                                    else:
                                        con.close()
                                        await message.reply(embed=discord.Embed(title="배팅 실패", description="이미 배팅중 입니다.",color=0x34c6eb))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.```**"))
                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                else:
                    con.close()
                    await message.reply(embed=discord.Embed(title="배팅 실패", description="`1,000원` 미만의 금액은 배팅 할 수 없습니다.",color=0x34c6eb))
            else:
                con.close()
                await message.reply(embed=discord.Embed(title="배팅 실패", description="당신은 봇 사용이 금지되어 있습니다.",color=0x34c6eb))
        else:
            await message.reply(embed=discord.Embed(title="배팅 실패", description="오류가 발생하였습니다.\n관리자에게 문의하세요.",color=0x34c6eb))

    if message.content == "!라바":
        if message.author.id in admin_id:
            rs_pe = client.get_channel(라바카라회차)
            pe_rs = await rs_pe.send(f"`1회차`가 진행되고있습니다.")
            round_rs = ''
            leng = 0

            if lbakara_on == 0:
                await message.channel.send(f"<#{라바카라채널}> 에 게임이 시작됩니다.")
                lbakara_on = 1
                lightning = ""
                lbkr_round = 0
                while True:
                    result = ""
                    presult = ""
                    text = ''
                    lbkr_round += 1
                    if lbkr_round == 500:
                        lbkr_round = 1
                    else:
                        pass
                    lp_add_card = pick_a_card()
                    lb_add_card = pick_a_card()
                    lcard1 = pick_a_card()
                    lcard2 = pick_a_card()
                    lcard3 = pick_a_card()
                    lplayer_card = pick_a_card()
                    lbanker_card = pick_a_card()
                    lplayer_card2 = pick_a_card()
                    lbanker_card2 = pick_a_card()
                    rs_ch = 라바카라유출픽
                    lp = (lplayer_card[0] + lplayer_card2[0]) % 10
                    lb = (lbanker_card[0] + lbanker_card2[0]) % 10
                    if lp <= 5:
                        
                        if lp_add_card[0] >= 10:
                            lp_add_card[0] = 0
                            lp_add_card[1] = "없음"
                    lp = (lp + lp_add_card[0]) % 10
                    if lb == 4 or lb == 5:
                        if lb < lp:
                            if lb_add_card[0] >= 10:
                                lb_add_card[0] = 0
                                lb_add_card[1] = "없음"
                    elif lb <= 5:
                        lb_add_card = pick_a_card()
                        if lb_add_card[0] >= 10:
                            lb_add_card[0] = 0
                            lb_add_card[1] = "없음"
                    lb = (lb + lb_add_card[0]) % 10
                    if lp == lb and lp == 5:
                        lp_add_card = pick_a_card()
                        if lp_add_card[0] >= 10:
                            lp_add_card[0] = 0
                            lp_add_card[1] = "없음"
                        lp = (lp + lp_add_card[0]) % 10
                    await client.get_channel(rs_ch).send(
                        f"{lbkr_round}회차\n플레이어" if lp > lb else f"{lbkr_round}회차\n뱅커" if lb > lp else f"{lbkr_round}회차\n무승부")
                    await client.get_channel(rs_ch).send(
                        f"{lbkr_round}회차\n플레이어페어" if lplayer_card[0] == lplayer_card2[0] else f"{lbkr_round}회차\n뱅커페어" if lbanker_card[0] == lbanker_card2[0] else f"{lbkr_round}회차\n노페어")
                    timm = 60
                    lbkr_ch = client.get_channel(라바카라채널)
                    # player = Button(label="플레이어", custom_id="플레이어", style=ButtonStyle.blue)
                    # banker = Button(label="뱅커", custom_id="뱅커", style=ButtonStyle.red)
                    # draw = Button(label="무승부", custom_id="무승부", style=ButtonStyle.green)
                    bet_embed = discord.Embed(title=f"{lbkr_round}회차 라이트닝바카라 배팅 시간입니다.",
                                                description=f"플레이어, 뱅커, 또는 무승부에 배팅해주십시오.\n플레이어 페어, 뱅커 페어에도 배팅이 가능합니다.\n\n남은 배팅시간 : `{timm}`",
                                                color=0x00C9FF)
                    bet_embed.set_footer(text=서버이름)
                    bet_msg = await lbkr_ch.send(embed=bet_embed)
                    for i in range(0, 60):
                        await asyncio.sleep(0.9)
                        timm -= 1
                        bet_embed = discord.Embed(title=f"{lbkr_round}회차 라이트닝바카라 배팅 시간입니다.",
                                                  description=f"플레이어, 뱅커, 또는 무승부에 배팅해주십시오.\n플레이어 페어, 뱅커 페어에도 배팅이 가능합니다.\n\n남은 배팅시간 : `{timm}`",
                                                  color=0x00C9FF)
                        bet_embed.set_footer(text=서버이름)
                        await bet_msg.edit(embed=bet_embed)
                        pamplier = 2
                        pamplierp = 11
                        bamplier = 1.95
                        bamplierp = 11
                        tamplier = 8
                    
                    if lp > lb and lcard1 == lplayer_card or lcard1 == lplayer_card2 or lcard1 == lp_add_card or lcard2 == lplayer_card or lcard2 == lplayer_card2 or lcard2 == lp_add_card or lcard3 == lplayer_card or lcard3 == lplayer_card2 or lcard3 == lp_add_card:
                        pamplier = 10 
                    elif lplayer_card == lplayer_card2 and lcard1 == lplayer_card or lcard1 == lplayer_card2 or lplayer_card == lplayer_card2 and lcard2 == lplayer_card or lcard2 == lplayer_card2 or lplayer_card == lplayer_card2 and lcard3 == lplayer_card or lcard3 == lplayer_card2:
                        pamplierp = 55
                    elif lp < lb and lcard1 == lbanker_card or lcard1 == lbanker_card2 or lcard1 == lb_add_card or lcard2 == lbanker_card or lcard2 == lbanker_card2 or lcard2 == lb_add_card or lcard3 == lbanker_card or lcard3 == lbanker_card2 or lcard3 == lb_add_card:
                        bamplier = 10 
                    elif lbanker_card == lbanker_card and lcard1 == lbanker_card or lcard1 == lbanker_card2 or lcard1 == lb_add_card or lcard2 == lbanker_card or lcard2 == lbanker_card2 or lcard2 == lb_add_card or lcard3 == lbanker_card or lcard3 == lbanker_card2 or lcard3 == lb_add_card:
                        bamplierp = 55
                    elif lplayer_card == lplayer_card2 or lbanker_card == lbanker_card and lcard1 == lbanker_card or lcard1 == lbanker_card2 or lcard1 == lplayer_card or lcard1 == lplayer_card2 or lplayer_card == lplayer_card2 or lbanker_card == lbanker_card and lcard2 == lbanker_card or lcard2 == lbanker_card2 or lcard2 == lplayer_card or lcard2 == lplayer_card2 or lplayer_card == lplayer_card2 or lbanker_card == lbanker_card and lcard3 == lbanker_card or lcard3 == lbanker_card2 or lcard3 == lplayer_card or lcard3 == lplayer_card2:
                        tamplier = 50
                    else:
                        pass


                    close_embed = discord.Embed(title=f"{lbkr_round}회차 배팅이 마감되었습니다", description=f'''
        ```
        ⚡ 라이트닝 카드 5x:
        {lcard1[1]}{lcard1[0]} , {lcard2[1]}{lcard2[0]}, {lcard3[1]}{lcard3[0]}


        🔵플레이어  ||  🔴뱅커

    {lplayer_card[1]}{lplayer_card[0]} ,  ? ,  ?  //   ? ,  ? ,  ?
        ```
        ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        **🔵 플레이어 : 카드 공개중...\n
        🟦 페어 : 카드 공개중...\n
        🔴 뱅커 : 카드 공개중...\n
        🟥 페어 : 카드 공개중...\n
        🟢 무승부 : 카드 공개중...**''', color=0x34c6eb)
                    await bet_msg.edit(embed=close_embed, components="")
                    await asyncio.sleep(1)
                    close_embed = discord.Embed(title=f"{lbkr_round}회차 배팅이 마감되었습니다", description=f'''
        ```
        ⚡ 라이트닝 카드 5x:
        {lcard1[1]}{lcard1[0]} , {lcard2[1]}{lcard2[0]}, {lcard3[1]}{lcard3[0]}


        🔵플레이어  ||  🔴뱅커

    {lplayer_card[1]}{lplayer_card[0]} ,  ? ,  ?  //   {lbanker_card[1]}{lbanker_card[0]} ,  ? ,  ?
        ```
        ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        **🔵 플레이어 : 카드 공개중...\n
        🟦 페어 : 카드 공개중...\n
        🔴 뱅커 : 카드 공개중...\n
        🟥 페어 : 카드 공개중...\n
        🟢 무승부 : 카드 공개중...**''', color=0x34c6eb)
                    await bet_msg.edit(embed=close_embed, components="")
                    await asyncio.sleep(1)
                    close_embed = discord.Embed(title=f"{lbkr_round}회차 배팅이 마감되었습니다", description=f'''
        ```
        ⚡ 라이트닝 카드 5x:
        {lcard1[1]}{lcard1[0]} , {lcard2[1]}{lcard2[0]}, {lcard3[1]}{lcard3[0]}


        🔵플레이어  ||  🔴뱅커

    {lplayer_card[1]}{lplayer_card[0]} ,  {lplayer_card2[1]}{lplayer_card2[0]} ,  ?  //   {lbanker_card[1]}{lbanker_card[0]} ,  ? ,  ?
        ```
        ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        **🔵 플레이어 : 카드 공개중...\n
        🟦 페어 : 카드 공개중...\n
        🔴 뱅커 : 카드 공개중...\n
        🟥 페어 : 카드 공개중...\n
        🟢 무승부 : 카드 공개중...**''', color=0x34c6eb)
                    await bet_msg.edit(embed=close_embed, components="")
                    await asyncio.sleep(1)
                    close_embed = discord.Embed(title=f"{lbkr_round}회차 배팅이 마감되었습니다", description=f'''
        ```
        ⚡ 라이트닝 카드 5x:
        {lcard1[1]}{lcard1[0]} , {lcard2[1]}{lcard2[0]}, {lcard3[1]}{lcard3[0]}


        🔵플레이어  ||  🔴뱅커

    {lplayer_card[1]}{lplayer_card[0]} ,  {lplayer_card2[1]}{lplayer_card2[0]} ,  ?  //   {lbanker_card[1]}{lbanker_card[0]} ,  {lbanker_card2[1]}{lbanker_card2[0]} ,  ?
        ```
        ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        **🔵 플레이어 : 카드 공개중...\n
        🟦 페어 : 카드 공개중...\n
        🔴 뱅커 : 카드 공개중...\n
        🟥 페어 : 카드 공개중...\n
        🟢 무승부 : 카드 공개중...**''', color=0x34c6eb)
                    await bet_msg.edit(embed=close_embed, components="")
                    await asyncio.sleep(1)
                    close_embed = discord.Embed(title=f"{lbkr_round}회차 배팅이 마감되었습니다", description=f'''
        ```
        ⚡ 라이트닝 카드 5x:
        {lcard1[1]}{lcard1[0]} , {lcard2[1]}{lcard2[0]}, {lcard3[1]}{lcard3[0]}


        🔵플레이어  ||  🔴뱅커

    {lplayer_card[1]}{lplayer_card[0]} ,  {lplayer_card2[1]}{lplayer_card2[0]} ,  {lp_add_card if lp_add_card != 0 else ""}  //   {lbanker_card[1]}{lbanker_card[0]} ,  {lbanker_card2[1]}{lbanker_card2[0]} ,  {lb_add_card if lb_add_card != 0 else ""}
        ```
        ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        **🔵 플레이어 : {lp} {"✅" if lp > lb else ""}   {f"< 승리! > X{pamplier}배" if lp > lb else ""}\n
        🟦 페어 : {"✅" if lplayer_card[0] == lplayer_card2[0] else ""}   {f"< 승리! > X{pamplierp}배" if lplayer_card[0] == lplayer_card2[0] else ""}\n
        🔴 뱅커 : {lb}   {"✅" if lp < lb else ""}   {f"< 승리! > X{bamplier}배" if lp < lb else ""}\n
        🟥 페어 : {"✅" if lbanker_card[0] == lbanker_card2[0] else ""}   {f"< 승리! > X{bamplierp}배" if lbanker_card[0] == lbanker_card2[0] else ""}\n
        🟢 무승부{f"< 승리! > X{tamplier}배" if lp == lb else ""}**''', color=0x34c6eb)
                    await bet_msg.edit(embed=close_embed, components="")
                    bet_log = ""
                    
                    conn = sqlite3.connect('./database/database.db')
                    c = conn.cursor()
                    list_a = list(c.execute("SELECT * FROM users"))

                    if lp>lb:
                        result = "플레이어"
                    elif lp<lb:
                        result = "뱅커"
                    elif lp == lb:
                        result = "무승부"
                    else:
                        pass
                    
                    if lbanker_card[0] == lbanker_card2[0]:
                        presult = "뱅커페어"
                    elif lplayer_card[0] == lplayer_card2[0]:
                        presult = "플레이어페어"
                    else:
                        pass

                    

                    for i in list_a:
                        if (i[50] == None):
                            continue
                        conn = sqlite3.connect('./database/database.db')
                        c = conn.cursor()
                        

                        if i[50] == "플레이어":
                            배당 = pamplier
                        elif i[50] == "플레이어페어":
                            배당 = pamplierp
                        elif i[50] == "뱅커":
                            배당 = bamplier
                        elif i[50] == "뱅커페어":
                            배당 = bamplierp
                        else:
                            배당 = tamplier
                        
                        if i[50] == result or i[50] == presult:
                            user = await client.fetch_user(f"{i[0]}")
                            await user.send(embed=discord.Embed(title="적중", description=f"배팅 게임 : 라이트닝바카라 (카지노)\n배팅 회차 : {lbkr_round}\n배팅 내역 : {i[50]}\n배팅 금액 : {i[51]}원\n─────────────\n적중 금액 : {round(i[51] * (배당-1))}\n남은 금액 : {i[1] + round(i[51] * 배당)}",color=0x00ff00))
                            
                            bet_log += (f"**<@{i[0]}> {i[50]} {round(i[51] * 배당)} 적중**\n")
                            c.execute("UPDATE users SET money = money + ? where id=?", (round(i[51] * 배당), i[0],))
                        elif result == "무승부":
                            user = await client.fetch_user(f"{i[0]}")
                            await user.send(embed=discord.Embed(title="무승부", description=f"배팅 게임 : 라이트닝바카라 (카지노)\n배팅 회차 : {lbkr_round}\n배팅 내역 : {i[50]}\n배팅 금액 : {i[51]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {i[1] + round(i[51])}"))
                            
                            bet_log += (f"**<@{i[0]}> {i[50]} {round(i[51])} 무승부**\n")
                            c.execute("UPDATE users SET money = money + ? where id=?",
                                      (round(i[51] * 1), i[0],))
                        else:
                            user = await client.fetch_user(f"{i[0]}")
                            await user.send(embed=discord.Embed(title="미적중", description=f"배팅 게임 : 라이트닝바카라 (카지노)\n배팅 회차 : {lbkr_round}\n배팅 내역 : {i[50]}\n배팅 금액 : {i[51]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {i[1]}",color=0xff0000))
                            
                            bet_log += (f"**<@{i[0]}> {i[50]} 미적중**\n")

                        c.execute("UPDATE users SET lightbkr_bet_pick = ? where id=?", (None, i[0],))
                        c.execute("UPDATE users SET lightbkr_bet_money = ? where id=?", (None, i[0],))
                        conn.commit()
                        conn.close()
                    doing_bet7 = []
                    oplog = ''
                    

                    if result == "플레이어":
                        if presult == "뱅커페어":
                            result1 = f"🔵 PLAYER | 🟥 뱅커 페어"
                        elif presult == "플레이어페어":
                            result1 = f"🔵 PLAYER | 🟦 플레이어 페어"
                        else:
                            result1 = f"🔵 PLAYER | ❌ 노 페어"
                    elif result == "뱅커":
                        if presult == "뱅커페어":
                            result1 = f"🔴 BANKER | 🟥 뱅커 페어"
                        elif presult == "플레이어페어":
                            result1 = f"🔴 BANKER | 🟦 플레이어 페어"
                        else:
                            result1 = f"🔴 BANKER | ❌ 노 페어"
                    elif result == "무승부":
                        if presult == "뱅커페어":
                            result1 = f"🟢 TIE | 🟥 뱅커 페어"
                        elif presult == "플레이어페어":
                            result1 = f"🟢 TIE | 🟦 플레이어 페어"
                        else:
                            result1 = f"🟢 TIE | ❌ 노 페어"
                    leng += 1
                    if leng >= 30:
                        round_rs = "**🎨 결과값 초기화 🎨**"
                        leng = 0
                    round_rs += f"\n\n`{lbkr_round}회차` 결과 : **{result1}**"
                    ch = client.get_channel(라바카라배팅내역)
                    await ch.send(embed=discord.Embed(title=f"{lbkr_round}회차 라이트닝바카라 배팅내역", description=f"{bet_log}",color=0x34c6eb))
                    await pe_rs.edit(embed=discord.Embed(title=f"라이트닝바카라 회차", description=f"{round_rs}",color=0x34c6eb))
    if message.content.startswith('.라바 '):
        if lbakara_on != 0:
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()
            if not user_info[5] == 3:
                if message.content.split(" ")[1] == "올인":
                    if (int(user_info[1]) >= 1000):
                        lbkramount = int(user_info[1])
                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                else:
                    lbkramount = int(message.content.split(" ")[1])
                if not lbkramount < 1000:
                    if user_info[1] >= lbkramount*1.2:
                        if not timm < 15:
                            owrunright = Button(label="플레이어", custom_id="플레이어", style=ButtonStyle.blue)
                            owrunleft = Button(label="뱅커", custom_id="뱅커", style=ButtonStyle.red)
                            pla = Button(label="플레이어 페어", custom_id="플레이어페어", style=ButtonStyle.blue)
                            ban = Button(label="뱅커 페어", custom_id="뱅커페어", style=ButtonStyle.red)
                            xd = Button(label="무승부", custom_id="무승부", style=ButtonStyle.green)

                            embed = discord.Embed(title="배팅하기",
                                                description='**라이트닝바카라 카지노 배팅하기**\n**배팅할 곳의 버튼을 클릭하여 배팅해주세요.**',
                                                color=0x2f3136)
                            embed.set_footer(text=서버이름)
                            bet_msg = await message.reply(embed=embed, components=
                            ActionRow(
                                [owrunright, owrunleft, xd],
                                [pla, ban],
                            )
                                                        )
                            while True:
                                try:
                                    interaction = await client.wait_for("button_click",
                                                                        check=lambda inter: inter.custom_id != "",
                                                                        timeout=5)
                                except asyncio.exceptions.TimeoutError:
                                    return

                                if message.author.id == interaction.user.id:
                                    if not message.author.id in doing_bet7:
                                        doing_bet7.append(message.author.id)
                                        if user_info[1] >= 1000:

                                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                        (user_info[1] - float(lbkramount), message.author.id))
                                            choice = interaction.custom_id
                                            cur.execute("UPDATE users SET lightbkr_bet_pick = ? WHERE id == ?;",
                                                        (choice, message.author.id))
                                            cur.execute("UPDATE users SET lightbkr_bet_money = ? WHERE id == ?;",
                                                        (lbkramount*1.2, message.author.id))
                                            con.commit()
                                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                        (lbkramount, message.author.id))
                                            con.commit()
                                            seconds = int(timm)
                                            minutes = seconds // 60
                                            remaining_seconds = seconds % 60

                                            if minutes > 0:
                                                if remaining_seconds > 0:
                                                    iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                                else:
                                                    iwannadosex = f"{minutes}분"
                                            else:
                                                iwannadosex = f"{seconds}초"
                                            add_bet(message.author.id,lbkramount*0.8)
                                            con.close()
                                            await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{lbkr_round}회차 라이트닝바카라 / {choice}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {math.floor(amount*1.2)}원```**"))


                                        else:
                                            con.close()
                                            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                                    else:
                                        con.close()
                                        await message.reply(embed=discord.Embed(title="배팅 실패", description="이미 배팅중 입니다.",color=0x34c6eb))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.```**"))
                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                else:
                    con.close()
                    await message.reply(embed=discord.Embed(title="배팅 실패", description="`1,000원` 미만의 금액은 배팅 할 수 없습니다.",color=0x34c6eb))
            else:
                con.close()
                await message.reply(embed=discord.Embed(title="배팅 실패", description="당신은 봇 사용이 금지되어 있습니다.",color=0x34c6eb))
        else:
            await message.reply(embed=discord.Embed(title="배팅 실패", description="오류가 발생하였습니다.\n관리자에게 문의하세요.",color=0x34c6eb))

    if message.content == "!식보":
        if message.author.id in admin_id:
            pw_pe = client.get_channel(식보회차)
            pw_rs = await pw_pe.send(f"`1회차`가 진행되고있습니다.")
            round_rs = ''
            leng = 0

            if lotto_on == 0:
                await message.channel.send(f"<#{식보채널}> 에 게임이 시작됩니다.")
                lotto_on = 1
                triple = 0
                oddeven = ""
                lightning = ""
                tripleresult = ""
                lotto_round = 0
                while True:
                    result = ""
                    lotto_round += 1
                    if lotto_round == 500:
                        lotto_round = 1
                    else:
                        pass

                    il1 = random.randint(1, 6)
                    il2 = random.randint(1, 6)
                    il3 = random.randint(1, 6)

                    if il1 == il2 and il2 == il3:
                        triple = 1
                        tripleresult = "모든 트리플"
                    else:
                        triple = 0
                        tripleresult = "트리플 없음"
                    
                    if (il1 + il2 + il3) % 2 == 0 and triple != 1:
                        oddeven = "짝"
                    elif (il1 + il2 + il3) % 2 == 1 and triple != 1:
                        oddeven = "홀"
                    else:
                        oddeven = "X"
                    
                    
                    if (il1 + il2 + il3) > 3 and (il1 + il2 + il3) < 11 and triple != 1:
                        updown = "낮은 수"
                    elif (il1 + il2 + il3) > 10 and (il1 + il2 + il3) < 18 and triple != 1:
                        updown = "높은 수"
                    else:
                        updown = "X"


                    pw_ch = 식보유출픽
                    await client.get_channel(pw_ch).send(
                        f"{lotto_round}회차\n> {il1} {il2} {il3}\n\n> {oddeven}\n> {updown}\n> {tripleresult}")
                    timmm = 60
                    pw1_ch = client.get_channel(식보채널)
                    # player = Button(label="플레이어", custom_id="플레이어", style=ButtonStyle.blue)
                    # banker = Button(label="뱅커", custom_id="뱅커", style=ButtonStyle.red)
                    # draw = Button(label="무승부", custom_id="무승부", style=ButtonStyle.green)
                    bet_embed = discord.Embed(title=f"{lotto_round}회차 식보 배팅 시간입니다.",
                                                description=f"홀, 짝, 높은수, 낮은수, 트리플에 배팅해주세요.\n\n남은 배팅시간 : `{timmm}`",
                                                color=0x00C9FF)
                    bet_embed.set_footer(text=서버이름)
                    bet_msg = await pw1_ch.send(embed=bet_embed)
                    for i in range(0, 60):
                        await asyncio.sleep(0.8)
                        timmm -= 1
                        bet_embed = discord.Embed(title=f"{lotto_round}회차 식보 배팅 시간입니다.",
                                                    description=f"홀, 짝, 높은수, 낮은수, 트리플에 배팅해주세요.\n\n남은 배팅시간 : `{timmm}`",
                                                    color=0x00C9FF)
                        bet_embed.set_footer(text=서버이름)
                        await bet_msg.edit(embed=bet_embed)
                    


                    close_embed = discord.Embed(title=f"{lotto_round}회차 배팅이 마감되었습니다", description=f'''
        ```d

        🔵주사위

          ?  ?  ?
        ```
        ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        **🔵 높은수/낮은수 : 주사위 굴리는 중...\n
        🔴 홀수/짝수 : 주사위 굴리는 중...\n
        🟩 모든 트리플 : 주사위 굴리는 중...**''', color=0x34c6eb)
                    await bet_msg.edit(embed=close_embed, components="")
                    await asyncio.sleep(1)
                    close_embed = discord.Embed(title=f"{lotto_round}회차 배팅이 마감되었습니다", description=f'''
        ```d

        🔵주사위

          {il1}  ?  ?
        ```
        ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        **🔵 높은수/낮은수 : 주사위 굴리는 중...\n
        🔴 홀수/짝수 : 주사위 굴리는 중...\n
        🟩 모든 트리플 : 주사위 굴리는 중...**''', color=0x34c6eb)
                    await bet_msg.edit(embed=close_embed, components="")
                    await asyncio.sleep(1)
                    close_embed = discord.Embed(title=f"{lotto_round}회차 배팅이 마감되었습니다", description=f'''
        ```d

        🔵주사위

          {il1}  {il2}  ?
        ```
        ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        **🔵 높은수/낮은수 : 주사위 굴리는 중...\n
        🔴 홀수/짝수 : 주사위 굴리는 중...\n
        🟩 모든 트리플 : 주사위 굴리는 중...**''', color=0x34c6eb)
                    await bet_msg.edit(embed=close_embed, components="")
                    await asyncio.sleep(1)
                    close_embed = discord.Embed(title=f"{lotto_round}회차 배팅이 마감되었습니다", description=f'''
        ```d

        🔵주사위

          {il1}  {il2}  {il3}
        ```
        ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
        **🔵 높은수/낮은수 : {updown}\n
        🔴 홀수/짝수 : {oddeven}\n
        🟩 모든 트리플 : {tripleresult}**''', color=0x34c6eb)
                    await bet_msg.edit(embed=close_embed, components="")
                    bet_log = ""
                    
                    conn = sqlite3.connect('./database/database.db')
                    c = conn.cursor()
                    list_a = list(c.execute("SELECT * FROM users"))

                    
                    
                    for i in list_a:
                        if (i[52] == None):
                            continue
                        if triple != 1:
                            배당 = 2
                        else:
                            배당 = 30
                        conn = sqlite3.connect('./database/database.db')
                        c = conn.cursor()
                        
                        
                        if i[52] == updown or i[52] == oddeven or i[52] == tripleresult:
                            bet_log += (f"**<@{i[0]}> {i[52]} {round(i[53] * 배당)} 적중**\n")
                            user = await client.fetch_user(f"{i[0]}")
                            await user.send(embed=discord.Embed(title="적중", description=f"배팅 게임 : 식보 (카지노)\n배팅 회차 : {lotto_round}\n배팅 내역 : {i[52]}\n배팅 금액 : {i[53]}원\n─────────────\n적중 금액 : {round(i[53] * (배당-1))}\n남은 금액 : {i[1] + round(i[53] * 배당)}",color=0x00ff00))
                            
                            
                            c.execute("UPDATE users SET money = money + ? where id=?", (round(i[53] * 배당), i[0],))
                        else:
                            user = await client.fetch_user(f"{i[0]}")
                            await user.send(embed=discord.Embed(title="미적중", description=f"배팅 게임 : 식보 (카지노)\n배팅 회차 : {lotto_round}\n배팅 내역 : {i[52]}\n배팅 금액 : {i[53]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {i[1]}",color=0xff0000))
                            
                            bet_log += (f"**<@{i[0]}> {i[52]} 미적중**\n")

                        c.execute("UPDATE users SET alphapw_bet_pick = ? where id=?", (None, i[0],))
                        c.execute("UPDATE users SET alphapw_bet_money = ? where id=?", (None, i[0],))
                        conn.commit()
                        conn.close()
                    doing_bet77 = []
                    oplog = ''
                    
                    result1 = f"🔵 {il1} {il2} {il3}"
                    leng += 1
                    if leng >= 30:
                        round_rs = "**🎨 결과값 초기화 🎨**"
                        leng = 0
                    round_rs += f"\n\n`{lotto_round}회차` 결과 : **{result1}**"
                    ch = client.get_channel(식보배팅내역)
                    await ch.send(embed=discord.Embed(title=f"{lotto_round}회차 식보 배팅내역", description=f"{bet_log}",color=0x34c6eb))
                    await pw_rs.edit(embed=discord.Embed(title=f"식보 회차", description=f"{round_rs}",color=0x34c6eb))
    if message.content.startswith('.식보 '):
        if lotto_on != 0:
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
                        await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                else:
                    amount = int(message.content.split(" ")[1])
                if not amount < 1000:
                    if user_info[1] >= amount:
                        if not timmm < 15:
                            if not message.author.id in doing_bet77:
                                up = Button(label="낮은 수", custom_id="낮은 수", style=ButtonStyle.red)
                                down = Button(label="높은 수", custom_id="높은 수", style=ButtonStyle.blue)
                                hol = Button(label="홀", custom_id="홀", style=ButtonStyle.red)
                                chak = Button(label="짝", custom_id="짝", style=ButtonStyle.blue)
                                triplebutton = Button(label="모든 트리플", custom_id="모든 트리플", style=ButtonStyle.green)

                                embed = discord.Embed(title="배팅하기",
                                                    description='**식보 카지노 배팅하기**\n**배팅할 곳의 버튼을 클릭하여 배팅해주세요.**',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [up, down],
                                    [hol, chak],
                                    [triplebutton],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        return

                                    if message.author.id == interaction.user.id:
                                        choice = interaction.custom_id
                                        await bet_msg.delete()
                                        doing_bet77.append(message.author.id)
                                        if user_info[1] >= 1000:

                                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                        (user_info[1] - float(amount), message.author.id))
                                            cur.execute("UPDATE users SET alphapw_bet_pick = ? WHERE id == ?;",
                                                        (choice, message.author.id))
                                            cur.execute("UPDATE users SET alphapw_bet_money = ? WHERE id == ?;",
                                                        (amount, message.author.id))
                                            con.commit()
                                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                        (amount, message.author.id))
                                            con.commit()
                                            
                                            seconds = int(timmm)
                                            minutes = seconds // 60
                                            remaining_seconds = seconds % 60

                                            if minutes > 0:
                                                if remaining_seconds > 0:
                                                    iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                                else:
                                                    iwannadosex = f"{minutes}분"
                                            else:
                                                iwannadosex = f"{seconds}초"
                                            add_bet(message.author.id,amount)
                                            con.close()
                                            await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{lotto_round}회차 식보 / {choice}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))

                                        else:
                                            con.close()
                                            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                            else:
                                con.close()
                                await message.reply(embed=discord.Embed(title="배팅 실패", description="이미 배팅중 입니다.",color=0x34c6eb))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.```**"))
                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                else:
                    con.close()
                    await message.reply(embed=discord.Embed(title="배팅 실패", description="`1,000원` 미만의 금액은 배팅 할 수 없습니다.",color=0x34c6eb))
            else:
                con.close()
                await message.reply(embed=discord.Embed(title="배팅 실패", description="당신은 봇 사용이 금지되어 있습니다.",color=0x34c6eb))
        else:
            await message.reply(embed=discord.Embed(title="배팅 실패", description="오류가 발생하였습니다.\n관리자에게 문의하세요.",color=0x34c6eb))

    if message.content == "!홀짝":
        if message.author.id in admin_id:
            rs_pe = client.get_channel(홀짝회차)
            pe_rs = await rs_pe.send(f"`1회차`가 진행되고있습니다.")
            round_rs = ''
            leng = 0
            bet_msg = await client.get_channel(홀짝채널).send(f"start")
            if hz_on == 0:
                await message.channel.send(f"<#{홀짝채널}> 에 게임이 시작됩니다.")
                hz_on = 1
                hz_round = 0
                while True:
                    text = ''
                    hz_round += 1
                    hz_h = []
                    hz_z = []
                    oplog = ''
                    if hz_round == 500:
                        hz_round = 1
                    else:
                        pass
                    result = "홀" if random.randint(0, 1) == 1 else '짝'
                    await client.get_channel(유출픽).send(f"> {hz_round}회차\n> `{result}`")
                    t = 60
                    hz_ch = client.get_channel(홀짝채널)
                    bet_embed = discord.Embed(title=f"{hz_round}회차 홀짝 배팅 시간입니다.",
                                              description=f"홀 또는 짝에 배팅해주십시오.\n\n남은 배팅시간 : `{t}`", color=0x00C9FF)
                    bet_embed.set_footer(text=서버이름)
                    await bet_msg.edit("", embed=bet_embed)
                    for i in range(0, 12):
                        await asyncio.sleep(5)
                        t -= 5
                        bet_embed = discord.Embed(title=f"{hz_round}회차 홀짝 배팅 시간입니다.",
                                                  description=f"홀 또는 짝에 배팅해주십시오.\n\n남은 배팅시간 : `{t}`",
                                                  color=0x00C9FF)
                        bet_embed.set_footer(text=서버이름)
                        await bet_msg.delete()
                        bet_msg = await hz_ch.send(embed=bet_embed)
                        if t == 0:
                            break

                    if result == "홀":
                        for i in hz_h:
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                            user_info = cur.fetchone()
                            user = client.get_user(i)
                            await user.send(embed=discord.Embed(title="적중", description=f"배팅 게임 : 홀짝 (카지노)\n배팅 회차 : {hz_round}\n배팅 내역 : 홀수\n배팅 금액 : {user_info[27]}원\n─────────────\n적중 금액 : {round(user_info[27] * 0.95)}\n남은 금액 : {user_info[1] + round(user_info[27] * 1.95)}",color=0x00ff00))
                            new_money = int(f'{(user_info[27] * 1.95):.0f}')
                            text += f"{user}: 홀에 {user_info[27]}원 -> {new_money}원 (적중)\n"
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] + new_money, i))
                            cur.execute("UPDATE users SET hz_bet_pick = ? where id=?", (None, i,))
                            cur.execute("UPDATE users SET hz_bet_money = ? where id=?", (None, i,))
                            con.commit()
                            con.close()
                            
                        for i in hz_z:
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                            user_info = cur.fetchone()
                            user = client.get_user(i)
                            new_money = 0
                            await user.send(embed=discord.Embed(title="미적중", description=f"배팅 게임 : 홀짝 (카지노)\n배팅 회차 : {hz_round}\n배팅 내역 : 홀수\n배팅 금액 : {user_info[27]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {user_info[1]}",color=0xff0000))
                            text += f"{user}: 짝에 {user_info[27]}원 -> {new_money}원 (미적중)\n"
                            cur.execute("UPDATE users SET hz_bet_pick = ? where id=?", (None, i,))
                            cur.execute("UPDATE users SET hz_bet_money = ? where id=?", (None, i,))
                            con.commit()
                            con.close()
                    else:
                        for i in hz_h:
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                            user_info = cur.fetchone()
                            user = client.get_user(i)
                            new_money = 0
                            text += f"{user}: 홀에 {user_info[27]}원 -> {new_money}원 (미적중)\n"
                            await user.send(embed=discord.Embed(title="미적중", description=f"배팅 게임 : 홀짝 (카지노)\n배팅 회차 : {hz_round}\n배팅 내역 : 홀수\n배팅 금액 : {user_info[27]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {user_info[1]}",color=0xff0000))
                            cur.execute("UPDATE users SET hz_bet_pick = ? where id=?", (None, i,))
                            cur.execute("UPDATE users SET hz_bet_money = ? where id=?", (None, i,))
                            con.commit()
                            con.close()
                        for i in hz_z:
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                            user_info = cur.fetchone()
                            user = client.get_user(i)
                            new_money = int(f'{(user_info[27] * 1.95):.0f}')
                            await user.send(embed=discord.Embed(title="적중", description=f"배팅 게임 : 홀짝 (카지노)\n배팅 회차 : {hz_round}\n배팅 내역 : 짝수\n배팅 금액 : {user_info[27]}원\n─────────────\n적중 금액 : {round(user_info[27] * 0.95)}\n남은 금액 : {user_info[1] + round(user_info[27] * 1.95)}",color=0x00ff00))
                            text += f"{user}: 짝에 {user_info[27]}원 -> {new_money}원 (적중)\n"
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] + new_money, i))
                            cur.execute("UPDATE users SET hz_bet_pick = ? where id=?", (None, i,))
                            cur.execute("UPDATE users SET hz_bet_money = ? where id=?", (None, i,))
                            con.commit()
                            con.close()
                    if text == '':
                        close_embed = discord.Embed(title=f"{hz_round}회차 배팅이 마감되었습니다",
                                                    description=f"{hz_round}회차 결과 : `{result}`\n\n```아무도 참여하지 않았습니다.```",
                                                    color=0x00C9FF)
                        close_embed.set_footer(text='10초후 다음 회차가 시작됩니다.')
                    else:
                        close_embed = discord.Embed(title=f"{hz_round}회차 배팅이 마감되었습니다",
                                                    description=f"{hz_round}회차 결과 : `{result}`\n\n```{text}```",
                                                    color=0x00C9FF)
                        close_embed.set_footer(text='10초후 다음 회차가 시작됩니다.')
                    await bet_msg.edit("", embed=close_embed, components="")
                    await asyncio.sleep(10)
                    doing_bet = []
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
                    leng += 1
                    if leng >= 50:
                        round_rs = "**🎨 결과값 초기화 🎨**"
                        leng = 0
                    round_rs += f"\n\n`{hz_round}회차` 결과 : **{result}**"
                    ch = client.get_channel(배팅내역)
                    await ch.send(embed=discord.Embed(title=f"{hz_round}회차 홀짝 배팅내역", description=f"{text}",color=0x34c6eb))
                    await pe_rs.edit(embed=discord.Embed(title=f"홀짝 회차", description=f"{round_rs}",color=0x34c6eb))
    if message.content.startswith('.홀짝 '):
        if hz_on != 0:
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
                        await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                else:
                    amount = int(message.content.split(" ")[1])
                if not amount < 1000:
                    if user_info[1] >= amount:
                        if t > 10:
                            if not message.author.id in doing_bet:
                                hol = Button(label="홀", custom_id="홀", style=ButtonStyle.blue)
                                chak = Button(label="짝", custom_id="짝", style=ButtonStyle.red)

                                embed = discord.Embed(title="배팅하기",
                                                    description='**홀짝 카지노 배팅하기**\n**배팅할 곳의 버튼을 클릭하여 배팅해주세요.**',
                                                    color=0x2f3136)
                                embed.set_footer(text=서버이름)
                                bet_msg = await message.reply(embed=embed, components=
                                ActionRow(
                                    [hol, chak],
                                )
                                                            )
                                while True:
                                    try:
                                        interaction = await client.wait_for("button_click",
                                                                            check=lambda inter: inter.custom_id != "",
                                                                            timeout=5)
                                    except asyncio.exceptions.TimeoutError:
                                        return

                                    if message.author.id == interaction.user.id:
                                        doing_bet.append(message.author.id)
                                        choice = interaction.custom_id
                                        await bet_msg.delete()
                                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                    (user_info[1] - amount, interaction.user.id))
                                        con.commit()
                                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                    (amount, message.author.id))
                                        con.commit()
                                        seconds = int(t)
                                        minutes = seconds // 60
                                        remaining_seconds = seconds % 60

                                        if minutes > 0:
                                            if remaining_seconds > 0:
                                                iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                            else:
                                                iwannadosex = f"{minutes}분"
                                        else:
                                            iwannadosex = f"{seconds}초"
                                        add_bet(message.author.id,amount)
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
                                            await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{hz_round}회차 홀짝 / {choice}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))

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
                                            await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{hz_round}회차 홀짝 / {choice}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))

                                        else:
                                            con.close()
                                            await message.reply(embed=discord.Embed(title="배팅 실패", description="홀/짝 으로만 배팅해 주십시오.",color=0x34c6eb))
                                    else:
                                        embed = discord.Embed(title='🎲 배팅 실패', description="**배팅은 본인만 가능합니다.**", color=0x2f3136)
                                        embed.set_footer(text=message.author)
                                        await interaction.respond(embed=embed)
                                        continue
                                else:
                                    await bet_msg.delete()
                                    
                            else:
                                con.close()
                                await message.reply(embed=discord.Embed(title="배팅 실패", description="이미 배팅중 입니다.",color=0x34c6eb))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.```**"))
                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                else:
                    con.close()
                    await message.reply(embed=discord.Embed(title="배팅 실패", description="`1,000원` 미만의 금액은 배팅 할 수 없습니다.",color=0x34c6eb))
            else:
                con.close()
                await message.reply(embed=discord.Embed(title="배팅 실패", description="당신은 봇 사용이 금지되어 있습니다.",color=0x34c6eb))
        else:
            await message.reply(embed=discord.Embed(title="배팅 실패", description="오류가 발생하였습니다.\n관리자에게 문의하세요.",color=0x34c6eb))
    if message.content == "!코인":
        if message.author.id in admin_id:
            coin_pe = client.get_channel(코인회차)
            coin_rs = await coin_pe.send(f"`1회차`가 진행되고있습니다.")
            round_rs = ''
            leng = 0
            bet_msg = await client.get_channel(코인채널).send(f"start")
            if coin1_on == 0:
                await message.channel.send(f"<#{코인채널}> 에 게임이 시작됩니다.")
                coin1_on = 1
                coin_round = 0
                percent = ""
                while True:
                    text = ''
                    coin_round += 1
                    coinbet = []
                    oplog = ''
                    if coin_round == 500:
                        coin_round = 1
                    else:
                        pass
                    result1 = ['나락', '나락','나락', '떡상', '떡상']
                    result = random.choice(result1)
                    coinpercent = random.randint(1, 100)
                    if result == "떡상":
                        percent = f"+{coinpercent}%"
                    elif result == "나락":
                        percent = f"-{coinpercent}%"
                    
                    await client.get_channel(코인유출픽).send(f"> {coin_round}회차\n> `{result}`\n> {percent}")
                    ticoin = 60
                    coin1_ch = client.get_channel(코인채널)
                    bet_embed = discord.Embed(title=f"{coin_round}회차 코인 투자가능 시간입니다.",
                                              description=f"원하는 금액을 매수해주세요.\n\n남은 배팅시간 : `{ticoin}`", color=0x00C9FF)
                    bet_embed.set_footer(text=서버이름)
                    await bet_msg.edit("", embed=bet_embed)
                    for i in range(0, 12):
                        await asyncio.sleep(5)
                        ticoin -= 5
                        bet_embed = discord.Embed(title=f"{coin_round}회차 코인 투자가능 시간입니다.",
                                                description=f"원하는 금액을 매수해주세요.\n\n남은 배팅시간 : `{ticoin}`", color=0x00C9FF)
                        bet_embed.set_footer(text=서버이름)
                        await bet_msg.delete()
                        bet_msg = await coin1_ch.send(embed=bet_embed)
                        if ticoin == 0:
                            break

                    if result == "떡상":
                        for i in coinbet:
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                            user_info = cur.fetchone()
                            user = client.get_user(i)
                            
                            new_money = int(f'{(user_info[30] + user_info[30] * coinpercent / 100):.0f}')
                            text += f"{user}: {user_info[30]}원 -> {new_money}원 (성공)\n"
                            await user.send(embed=discord.Embed(title="투자 성공", description=f"배팅 게임 : 코인 (카지노)\n투자 회차 : {coin_round}\n투자 금액 : {user_info[30]}원\n─────────────\n적중 금액 : {user_info[30] * coinpercent / 100}\n남은 금액 : {user_info[1]}",color=0x00ff00))
                            
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] + new_money, i))
                            cur.execute("UPDATE users SET coin_bet_money = ? where id=?", (None, i,))
                            con.commit()
                            con.close()
                    else:
                        for i in coinbet:
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (i,))
                            user_info = cur.fetchone()
                            user = client.get_user(i)
                            
                            new_money = int(f'{(user_info[30] - user_info[30] * coinpercent / 100):.0f}')
                            await user.send(embed=discord.Embed(title="투자 실패", description=f"배팅 게임 : 코인 (카지노)\n투자 회차 : {coin_round}\n투자 금액 : {user_info[30]}원\n─────────────\n적중 금액 : {user_info[30] * coinpercent / 100}\n남은 금액 : {user_info[1]}",color=0xff0000))
                            
                            text += f"{user}: {user_info[30]}원 -> {new_money}원 (실패)\n"
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] + new_money, i))
                            cur.execute("UPDATE users SET coin_bet_money = ? where id=?", (None, i,))
                            con.commit()
                            con.close()
                    if text == '':
                        close_embed = discord.Embed(title=f"{coin_round}회차 투자가 마감되었습니다",
                                                    description=f"{coin_round}회차 결과 : `{percent}`\n\n```아무도 투자하지 않았습니다.```",
                                                    color=0x00C9FF)
                        close_embed.set_footer(text='10초후 다음 회차가 시작됩니다.')
                    else:
                        close_embed = discord.Embed(title=f"{coin_round}회차 투자가 마감되었습니다",
                                                    description=f"{coin_round}회차 결과 : `{percent}`\n\n```{text}```",
                                                    color=0x00C9FF)
                        close_embed.set_footer(text='10초후 다음 회차가 시작됩니다.')
                    await bet_msg.edit("", embed=close_embed, components="")
                    await asyncio.sleep(10)
                    doing_betcoin = []
                    if result == "떡상":
                        if text != '':
                            result = f"{percent} ↑ "
                        else:
                            result = f"{percent} ↑ "
                    else:
                        if text != '':
                            result = f"{percent} ↓ "
                        else:
                            result = f"{percent} ↓ "
                    leng += 1
                    if leng >= 50:
                        round_rs = "**🎨 결과값 초기화 🎨**"
                        leng = 0
                    round_rs += f"\n\n`{coin_round}회차` 결과 : **{result}**"
                    ch = client.get_channel(코인배팅내역)
                    await ch.send(f"`{coin_round}회차`\n\n{text}")
                    await ch.send(embed=discord.Embed(title=f"{coin_round}회차 코인 배팅내역", description=f"{text}",color=0x34c6eb))
                    await coin_rs.edit(embed=discord.Embed(title=f"코인 회차", description=f"{round_rs}",color=0x34c6eb))
    if message.content.startswith('.코인 '):
        if coin1_on != 0:
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
                        await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                else:
                    amount = int(message.content.split(" ")[1])
                if not amount < 1000:
                    if user_info[1] >= amount:
                        if ticoin > 10:
                            if not message.author.id in doing_betcoin:
                                doing_betcoin.append(message.author.id)

                                if user_info[1] >= 1000:
                                    coinbet.append(message.author.id)
                                    cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                (user_info[1] - amount, message.author.id))
                                    cur.execute("UPDATE users SET coin_bet_money = ? WHERE id == ?;",
                                                (amount, message.author.id))
                                    con.commit()
                                    
                                    seconds = int(ticoin)
                                    minutes = seconds // 60
                                    remaining_seconds = seconds % 60

                                    if minutes > 0:
                                        if remaining_seconds > 0:
                                            iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                        else:
                                            iwannadosex = f"{minutes}분"
                                    else:
                                        iwannadosex = f"{seconds}초"
                                    con.close()
                                    await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{coin_round}회차 코인\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))

                                
                                else:
                                    con.close()
                                    await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                            else:
                                con.close()
                                await message.reply(embed=discord.Embed(title="배팅 실패", description="이미 배팅중 입니다.",color=0x34c6eb))
                        else:
                            con.close()
                            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.```**"))
                    else:
                        con.close()
                        await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                else:
                    con.close()
                    await message.reply(embed=discord.Embed(title="배팅 실패", description="`1,000원` 미만의 금액은 배팅 할 수 없습니다.",color=0x34c6eb))
            else:
                con.close()
                await message.reply(embed=discord.Embed(title="배팅 실패", description="당신은 봇 사용이 금지되어 있습니다.",color=0x34c6eb))
        else:
            await message.reply(embed=discord.Embed(title="배팅 실패", description="오류가 발생하였습니다.\n관리자에게 문의하세요.",color=0x34c6eb))
    if message.content == "!경마":
        if message.author.id in admin_id:
            rs_pe = client.get_channel(경마회차)
            pe_rs = await rs_pe.send(f"`1회차`가 진행되고있습니다.")
            round_rs = ''
            # leng = 0
            # bet_msg = await client.get_channel(경마채널).send(f"start")
            if km_on == 0:
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
                    if km_round == 500:
                        km_round = 1
                    else:
                        pass
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
                            user = await client.fetch_user(f"{i[0]}")
                            await user.send(embed=discord.Embed(title="적중", description=f"배팅 게임 : 경마 (카지노)\n배팅 회차 : {km_round}\n배팅 내역 : {i[20]}\n배팅 금액 : {i[21]}원\n─────────────\n적중 금액 : {round(i[21] * (배당-1))}\n남은 금액 : {i[1] + round(i[21] * 배당)}",color=0x00ff00))
                            
                            c.execute("UPDATE users SET money = money + ? where id=?", (round(i[21] * 배당), i[0],))
                        elif km_result == '무승부':
                            user = await client.fetch_user(f"{i[0]}")
                            await user.send(embed=discord.Embed(title="무승부", description=f"배팅 게임 : 경마 (카지노)\n배팅 회차 : {km_round}\n배팅 내역 : {i[20]}\n배팅 금액 : {i[21]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {i[1] + round(i[25])}"))
                            
                            bet_log += (f"**<@{i[0]}> {i[20]}번 {i[21]}원 무승부**\n")
                            c.execute("UPDATE users SET money = money + ? where id=?",
                                    (round(i[21] * 1), i[0],))
                        else:
                            user = await client.fetch_user(f"{i[0]}")
                            await user.send(embed=discord.Embed(title="미적중", description=f"배팅 게임 : 경마 (카지노)\n배팅 회차 : {km_round}\n배팅 내역 : {i[20]}\n배팅 금액 : {i[21]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {i[1]}",color=0xff0000))
                            
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
                    await pe_rs.edit(embed=discord.Embed(title=f"경마 회차", description=f"{round_rs}",color=0x34c6eb))
                    await bet_msg.delete()

    if message.content.startswith('.경마 '):
        if km_on != 0:
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()
            if not user_info[5] == 3:
                if message.content.split(" ")[1] == "올인":
                    if (int(user_info[1]) >= 500):
                        amount = int(user_info[1])
                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
                else:
                    try:
                        amount = int(message.content.split(" ")[1])
                    except:
                        con.close()
                        await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**금액은 정수만 배팅이 가능합니다.**"))
                        return
                if not amount < 500:
                    if user_info[1] >= amount:
                        if ttii > 10:
                            
                            if user_info[1] >= 500:
                                if not message.author.id in doing_bet5:
                                    onemal = Button(label="1", custom_id="1", style=ButtonStyle.red)
                                    twomal = Button(label="2", custom_id="2", style=ButtonStyle.blue)
                                    threemal = Button(label="3", custom_id="3", style=ButtonStyle.red)
                                    fourmal = Button(label="4", custom_id="4", style=ButtonStyle.blue)

                                    embed = discord.Embed(title="배팅하기",
                                                        description='**경마 카지노 배팅하기**\n**배팅할 곳의 버튼을 클릭하여 배팅해주세요.**',
                                                        color=0x2f3136)
                                    embed.set_footer(text=서버이름)
                                    bet_msg = await message.reply(embed=embed, components=
                                    ActionRow(
                                        [onemal, twomal, threemal, fourmal],
                                    )
                                                                )
                                    while True:
                                        try:
                                            interaction = await client.wait_for("button_click",
                                                                                check=lambda inter: inter.custom_id != "",
                                                                                timeout=5)
                                        except asyncio.exceptions.TimeoutError:
                                            return

                                        if message.author.id == interaction.user.id:
                                            choice = interaction.custom_id
                                            doing_bet5.append(message.author.id)
                                            
                                            seconds = int(ttii)
                                            minutes = seconds // 60
                                            remaining_seconds = seconds % 60

                                            if minutes > 0:
                                                if remaining_seconds > 0:
                                                    iwannadosex = f"{minutes}분 {remaining_seconds}초"
                                                else:
                                                    iwannadosex = f"{minutes}분"
                                            else:
                                                iwannadosex = f"{seconds}초"
                                            if choice == "1":
                                                cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                            (user_info[1] - amount, message.author.id))
                                                cur.execute("UPDATE users SET ad_bet_pick = ? WHERE id == ?;",
                                                            (choice, message.author.id))
                                                cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                            (amount, message.author.id))
                                                con.commit()
                                                add_bet(message.author.id,amount)
                                                cur.execute("UPDATE users SET ad_bet_money = ? WHERE id == ?;",
                                                            (amount, message.author.id))
                                                con.commit()
                                                con.close()
                                                await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{km_round}회차 경마 / {choice}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))

                                                
                                            elif choice == "2":
                                                cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                            (user_info[1] - amount, message.author.id))
                                                cur.execute("UPDATE users SET ad_bet_pick = ? WHERE id == ?;",
                                                            (choice, message.author.id))
                                                cur.execute("UPDATE users SET ad_bet_money = ? WHERE id == ?;",
                                                            (amount, message.author.id))
                                                add_bet(message.author.id,amount)
                                                cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                            (amount, message.author.id))
                                                con.commit()
                                                con.commit()
                                                con.close()
                                                await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{km_round}회차 경마 / {choice}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))

                                            elif choice == "3":
                                                hz_z.append(message.author.id)
                                                cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                            (user_info[1] - amount, message.author.id))
                                                cur.execute("UPDATE users SET ad_bet_pick = ? WHERE id == ?;",
                                                            (choice, message.author.id))
                                                cur.execute("UPDATE users SET ad_bet_money = ? WHERE id == ?;",
                                                            (amount, message.author.id))
                                                cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                            (amount, message.author.id))
                                                add_bet(message.author.id,amount)
                                                con.commit()
                                                con.commit()
                                                con.close()
                                                await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{km_round}회차 경마 / {choice}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))

                                            elif choice == "4":
                                                hz_z.append(message.author.id)
                                                cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                                            (user_info[1] - amount, message.author.id))
                                                cur.execute("UPDATE users SET ad_bet_pick = ? WHERE id == ?;",
                                                            (choice, message.author.id))
                                                cur.execute("UPDATE users SET ad_bet_money = ? WHERE id == ?;",
                                                            (amount, message.author.id))
                                                cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                                            (amount, message.author.id))
                                                add_bet(message.author.id,amount)
                                                con.commit()
                                                con.commit()
                                                con.close()
                                                await message.reply(embed=betingembed("**✅ 배팅 성공**", f"**```{km_round}회차 경마 / {choice}\n\n{iwannadosex} 뒤 진행\n\n잔액 : {user_info[1] - amount}원\n배팅금 : {amount}원```**"))

                                            else:
                                                con.close()
                                                await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**1/2/3/4 중에서만 배팅해주세요.**"))
                                else:
                                    con.close()
                                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```이미 배팅중입니다.```**"))
                            else:
                                con.close()
                                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))

                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```배팅이 마감되었습니다.\n다음 회차에 배팅해주십시오.```**"))
                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
        else:
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```게임이 진행중이지 않습니다.```**"))
    
    if message.content.startswith('.슬롯 '):
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?);", (message.author.id, 0, None, 0, 0, 0,None ,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    if not (user_info[5] == 1):
                        cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] - amount, message.author.id))
                        con.commit()
                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                    (amount, message.author.id))
                        bet_amount = amount
                        add_bet(message.author.id,amount)
                        con.commit()
                        con.close()
                        the_numbers = [0,1,2,3,4,5,3,1,7,1,0,0,0,6,8,8,9]
                        first_layer = []
                        second_layer = []
                        third_layer = []
                        def roll_slots():
                            for fusiqj in range(3):
                                selected_num = random.choice(the_numbers)
                                first_layer.append(selected_num)
                            for fusiqj in range(3):
                                selected_num = random.choice(the_numbers)
                                second_layer.append(selected_num)
                            for fusiqj in range(3):
                                selected_num = random.choice(the_numbers)
                                third_layer.append(selected_num)
                        def calc_slots():
                            result = []
                            #세로
                            if first_layer[0] == first_layer[1] == first_layer[2] != 0:
                                result.append("1빙고")
                            if second_layer[0] == second_layer[1] == second_layer[2] != 0:
                                result.append("1빙고")
                            if third_layer[0] == third_layer[1] == third_layer[2] != 0:
                                result.append("1빙고")
                            #가로
                            if first_layer[0] == second_layer[0] == third_layer[0] != 0:
                                result.append("1빙고")
                            if first_layer[1] == second_layer[1] == third_layer[1] != 0:
                                result.append("1빙고")
                            if first_layer[2] == second_layer[1] == third_layer[2] != 0:
                                result.append("1빙고")
                            #대각선
                            if first_layer[0] == second_layer[1] == third_layer[2] != 0:
                                result.append("1빙고")
                            if first_layer[2] == second_layer[1] == third_layer[0] != 0:
                                result.append("1빙고")
                            #숫자 체크
                            first_Counter = collections.Counter(first_layer)
                            second_Counter = collections.Counter(second_layer)
                            third_Counter = collections.Counter(third_layer)
                            total_Counter = first_Counter + second_Counter + third_Counter
                            most_values = total_Counter.most_common(3)
                            for inas in range(3):
                                number_tuple = most_values[inas]
                                if number_tuple[1] >= 3 and number_tuple[0] != 0:
                                    result.append(f"{number_tuple[0]}-{number_tuple[1]}")
                            return result
                        winning_amount = 0
                        roll_slots()
                        result_sum = ""
                        result_ = calc_slots()
                        sent_first = await message.reply(embed=discord.Embed(title="🎲 슬롯", description=f"**```d\n{amount}원\n\n슬롯이 시작됩니다.```**",color=0x34c6eb))
                        await asyncio.sleep(1)
                        if result_ != []:
                            for wining in result_:
                                if wining != "1빙고":
                                    splited_res = wining.split("-")
                                    winning_amount += bet_amount/5*3
                                    await asyncio.sleep(0.7)
                                    result_sum += f"{splited_res[0]}이 {splited_res[1]}개 이상이므로 {math.floor(bet_amount/5*3)}원에 당첨되었습니다.\n스핀 1번 기회가 주어집니다.\n"
                                else:
                                    winning_amount += bet_amount*3
                                    await asyncio.sleep(0.7)
                                    result_sum += f"1빙고 당첨이므로 {math.floor(bet_amount*3)}원에 당첨되었습니다.\n스핀 1번 기회가 주어집니다.\n"
                            first_message = f"{first_layer[0]} | ? | ?\n{first_layer[1]} | ? | ?\n{first_layer[2]} | ? | ?"
                            second_message = f"{first_layer[0]} | {second_layer[0]} | ?\n{first_layer[1]} | {second_layer[1]} | ?\n{first_layer[2]} | {second_layer[2]} | ?"
                            third_message = f"{first_layer[0]} | {second_layer[0]} | {third_layer[0]}\n{first_layer[1]} | {second_layer[1]} | {third_layer[1]}\n{first_layer[2]} | {second_layer[2]} | {third_layer[2]}" + f"\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}"
                            await sent_first.edit(embed=discord.Embed(title="🎲 슬롯", description=f"**```d\n{first_layer[0]} | ? | ?\n{first_layer[1]} | ? | ?\n{first_layer[2]} | ? | ?```**",color=0x34c6eb))
                            await asyncio.sleep(1)
                            await sent_first.edit(embed=discord.Embed(title="🎲 슬롯", description=f"**```d\n{first_layer[0]} | {second_layer[0]} | ?\n{first_layer[1]} | {second_layer[1]} | ?\n{first_layer[2]} | {second_layer[2]} | ?```**",color=0x34c6eb))
                            await asyncio.sleep(1)
                            await sent_first.edit(embed=discord.Embed(title="🎲 슬롯", description=f"**```d\n{first_layer[0]} | {second_layer[0]} | {third_layer[0]}\n{first_layer[1]} | {second_layer[1]} | {third_layer[1]}\n{first_layer[2]} | {second_layer[2]} | {third_layer[2]}```\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}**",color=0x34c6eb))
                            await asyncio.sleep(1)
                            first_layer = []
                            second_layer = []
                            third_layer = []
                        else:
                            first_message = f"{first_layer[0]} | ? | ?\n{first_layer[1]} | ? | ?\n{first_layer[2]} | ? | ?"
                            second_message = f"{first_layer[0]} | {second_layer[0]} | ?\n{first_layer[1]} | {second_layer[1]} | ?\n{first_layer[2]} | {second_layer[2]} | ?"
                            third_message = f"{first_layer[0]} | {second_layer[0]} | {third_layer[0]}\n{first_layer[1]} | {second_layer[1]} | {third_layer[1]}\n{first_layer[2]} | {second_layer[2]} | {third_layer[2]}" + f"\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}"
                            await sent_first.edit(embed=discord.Embed(title="🎲 슬롯", description=f"**```d\n{first_layer[0]} | ? | ?\n{first_layer[1]} | ? | ?\n{first_layer[2]} | ? | ?```**",color=0x34c6eb))
                            await asyncio.sleep(1)
                            await sent_first.edit(embed=discord.Embed(title="🎲 슬롯", description=f"**```d\n{first_layer[0]} | {second_layer[0]} | ?\n{first_layer[1]} | {second_layer[1]} | ?\n{first_layer[2]} | {second_layer[2]} | ?```**",color=0x34c6eb))
                            await asyncio.sleep(1)
                            await sent_first.edit(embed=discord.Embed(title="🎲 슬롯", description=f"**```d\n{first_layer[0]} | {second_layer[0]} | {third_layer[0]}\n{first_layer[1]} | {second_layer[1]} | {third_layer[1]}\n{first_layer[2]} | {second_layer[2]} | {third_layer[2]}```\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}**",color=0x34c6eb))
                            await asyncio.sleep(1)
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                            user_info = cur.fetchone()

                            cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (winning_amount)), message.author.id))
                            con.commit()
                            await message.reply(embed=discord.Embed(title="🎲 슬롯", description=f"**```d\n총 {math.floor(winning_amount)}원에 당첨되셨습니다.```**",color=0x34c6eb))
                            
                            first_layer = []
                            second_layer = []
                            third_layer = []
                            return
                        while True:
                            roll_slots()
                            result_ = calc_slots()          
                            if result_ != []:
                                for wining in result_:
                                    if wining != "1빙고":
                                        splited_res = wining.split("-")
                                        winning_amount += bet_amount/5*3
                                        await asyncio.sleep(0.7)
                                        result_sum += f"{splited_res[0]}이 {splited_res[1]}개 이상이므로 {math.floor(bet_amount/5*3)}원에 당첨되었습니다.\n스핀 1번 기회가 주어집니다.\n"
                                    else:
                                        winning_amount += bet_amount*3
                                        await asyncio.sleep(0.7)
                                        result_sum += f"1빙고 당첨이므로 {math.floor(bet_amount*3)}원에 당첨되었습니다.\n스핀 1번 기회가 주어집니다.\n"
                                first_message = f"{first_layer[0]} | ? | ?\n{first_layer[1]} | ? | ?\n{first_layer[2]} | ? | ?" + f"\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}"
                                second_message = f"{first_layer[0]} | {second_layer[0]} | ?\n{first_layer[1]} | {second_layer[1]} | ?\n{first_layer[2]} | {second_layer[2]} | ?" + f"\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}"
                                third_message = f"{first_layer[0]} | {second_layer[0]} | {third_layer[0]}\n{first_layer[1]} | {second_layer[1]} | {third_layer[1]}\n{first_layer[2]} | {second_layer[2]} | {third_layer[2]}" + f"\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}"
                                await sent_first.edit(embed=discord.Embed(title="🎲 슬롯", description=f"**```d\n{first_layer[0]} | ? | ?\n{first_layer[1]} | ? | ?\n{first_layer[2]} | ? | ?```\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}**",color=0x34c6eb))
                                await asyncio.sleep(1)
                                await sent_first.edit(embed=discord.Embed(title="🎲 슬롯", description=f"**```d\n{first_layer[0]} | {second_layer[0]} | ?\n{first_layer[1]} | {second_layer[1]} | ?\n{first_layer[2]} | {second_layer[2]} | ?```\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}**",color=0x34c6eb))
                                await asyncio.sleep(1)
                                await sent_first.edit(embed=discord.Embed(title="🎲 슬롯", description=f"**```d\n{first_layer[0]} | {second_layer[0]} | {third_layer[0]}\n{first_layer[1]} | {second_layer[1]} | {third_layer[1]}\n{first_layer[2]} | {second_layer[2]} | {third_layer[2]}```\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}**",color=0x34c6eb))
                                await asyncio.sleep(1)
                                first_layer = []
                                second_layer = []
                                third_layer = []
                            else:
                                first_message = f"{first_layer[0]} | ? | ?\n{first_layer[1]} | ? | ?\n{first_layer[2]} | ? | ?" + f"\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}"
                                second_message = f"{first_layer[0]} | {second_layer[0]} | ?\n{first_layer[1]} | {second_layer[1]} | ?\n{first_layer[2]} | {second_layer[2]} | ?" + f"\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}"
                                third_message = f"{first_layer[0]} | {second_layer[0]} | {third_layer[0]}\n{first_layer[1]} | {second_layer[1]} | {third_layer[1]}\n{first_layer[2]} | {second_layer[2]} | {third_layer[2]}" + f"\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}"
                                await sent_first.edit(embed=discord.Embed(title="🎲 슬롯", description=f"**```d\n{first_layer[0]} | ? | ?\n{first_layer[1]} | ? | ?\n{first_layer[2]} | ? | ?```\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}**",color=0x34c6eb))
                                await asyncio.sleep(1)
                                await sent_first.edit(embed=discord.Embed(title="🎲 슬롯", description=f"**```d\n{first_layer[0]} | {second_layer[0]} | ?\n{first_layer[1]} | {second_layer[1]} | ?\n{first_layer[2]} | {second_layer[2]} | ?```\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}**",color=0x34c6eb))
                                await asyncio.sleep(1)
                                await sent_first.edit(embed=discord.Embed(title="🎲 슬롯", description=f"**```d\n{first_layer[0]} | {second_layer[0]} | {third_layer[0]}\n{first_layer[1]} | {second_layer[1]} | {third_layer[1]}\n{first_layer[2]} | {second_layer[2]} | {third_layer[2]}```\n> 당첨금 : {math.floor(winning_amount)}\n{result_sum}**",color=0x34c6eb))
                                await asyncio.sleep(1)
                                con = sqlite3.connect("./database/database.db")
                                cur = con.cursor()
                                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                                user_info = cur.fetchone()

                                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (winning_amount)), message.author.id))
                                con.commit()
                                await message.reply(embed=discord.Embed(title="🎲 슬롯", description=f"**```d\n총 {math.floor(winning_amount)}원에 당첨되셨습니다.```**",color=0x34c6eb))
                                first_layer = []
                                second_layer = []
                                third_layer = []
                                break
                    
                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.reply(embed=discord.Embed(title="배팅 실패", description="섹스.",color=0x34c6eb))
    
    if message.content.startswith('.랜덤박스 '):
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?);", (message.author.id, 0, None, 0, 0, 0,None ,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    if not (user_info[5] == 1):
                        cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] - amount, message.author.id))
                        con.commit()
                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                    (amount, message.author.id))
                        bet_amount = amount
                        add_bet(message.author.id,amount)
                        con.commit()
                        con.close()
                        sent_first = await message.reply(embed=discord.Embed(title="🎲 랜덤박스", description=f"**```yaml\n{amount}원\n\n랜덤박스 오픈이 시작됩니다.```**",color=0x34c6eb))
                        await asyncio.sleep(1)
                        winning_amount = random.randint(0, amount*1.3)
                        con = sqlite3.connect("./database/database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                        user_info = cur.fetchone()

                        cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (winning_amount)), message.author.id))
                        con.commit()
                        await sent_first.edit(embed=discord.Embed(title="🎲 랜덤박스", description=f"**```yaml\n총 {math.floor(winning_amount)}원에 당첨되셨습니다.```**",color=0x34c6eb))
                        
                    
                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.reply(embed=discord.Embed(title="배팅 실패", description="섹스.",color=0x34c6eb))
    
    if message.content.startswith('.독보찾기 ') or message.content.startswith('.도그보찾기 '):
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?);", (message.author.id, 0, None, 0, 0, 0,None ,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    if not (user_info[5] == 1):
                        cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] - amount, message.author.id))
                        con.commit()
                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                    (amount, message.author.id))
                        bet_amount = amount
                        add_bet(message.author.id,amount)
                        
                        con.commit()
                        con.close()

                        sexslist = ["x", "x", "x", "x", "x", "o"]
                        resultfind = random.choice(sexslist)

                        sent_first = await message.reply(embed=discord.Embed(title="🎲 Dogbo 찾기!", description=f"**```yaml\n{amount}원\n\nDogbo를 한번 찾아봅시다.```**",color=0x34c6eb))
                        await asyncio.sleep(1)
                        if resultfind == "x":
                            await sent_first.edit(embed=discord.Embed(title="🎲 Dogbo 찾기 실패", description=f"**```yaml\nDogbo가 당신의 {amount}원을 배부르게 먹었습니다. 😋```**",color=0x34c6eb))
                        else:
                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                            user_info = cur.fetchone()

                            cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount*5)), message.author.id))
                            con.commit()
                            await sent_first.edit(embed=discord.Embed(title="🎲 Dogbo 찾기 성공", description=f"**```yaml\nDogbo가 당신에게 {amount*5}원을 선물해 주었어요!```**",color=0x34c6eb))
                    
                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.reply(embed=discord.Embed(title="배팅 실패", description="섹스.",color=0x34c6eb))
    
    if message.content.startswith('.광질 '):
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?);", (message.author.id, 0, None, 0, 0, 0,None ,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    if not (user_info[5] == 1):
                        baydang = 0
                        cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] - amount, message.author.id))
                        con.commit()
                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                    (amount, message.author.id))
                        bet_amount = amount
                        add_bet(message.author.id,amount)
                        con.commit()
                        con.close()
                        sent_first = await message.reply(embed=discord.Embed(title="🎲 광질", description=f"**```yaml\n{amount}원\n\n광질을 시작합니다.```**",color=0x34c6eb))
                        await asyncio.sleep(1)
                        await sent_first.edit(embed=discord.Embed(title="🎲 광질", description=f"**```yaml\n ⛏️ · · ·```**",color=0x34c6eb))
                        await asyncio.sleep(1)
                        await sent_first.edit(embed=discord.Embed(title="🎲 광질", description=f"**```yaml\n · ⛏️ · ·```**",color=0x34c6eb))
                        await asyncio.sleep(1)
                        await sent_first.edit(embed=discord.Embed(title="🎲 광질", description=f"**```yaml\n · · ⛏️ ·```**",color=0x34c6eb))
                        await asyncio.sleep(1)
                        await sent_first.edit(embed=discord.Embed(title="🎲 광질", description=f"**```yaml\n · · · ⛏️```**",color=0x34c6eb))
                        await asyncio.sleep(1)
                        listr = ['🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌','🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌',  '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌','🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌','🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '💿 철', '💿 철', '💿 철', '💿 철', '💿 철','💿 철', '💿 철', '💿 철', '💿 철', '💿 철', '💿 철', '💿 철', '💿 철', '💿 철', '💿 철', '💿 철', '🟨 금', '🟨 금', '🟨 금', '🟨 금', '🟨 금', '🟨 금', '🟨 금', '🟨 금', '🟨 금', '🟨 금', '🟨 금', '🟨 금', '🟨 금', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌', '🪨 돌',  '💿 철', '💿 철', '💿 철', '💿 철', '💿 철', '🔷 청금석', '🔷 청금석', '🔷 청금석', '🔷 청금석', '🔷 청금석', '🔷 청금석', '💎 다이아몬드', '💎 다이아몬드', '💜 에메랄드']
                        result = random.choice(listr)
                        if result == '🪨 돌':
                            baydang = 0
                        if result == '💿 철':
                            baydang = 1.2
                        if result == '🟨 금':
                            baydang = 1.3
                        if result == '🔷 청금석':
                            baydang = 2
                        if result == '💎 다이아몬드':
                            baydang = 5
                        if result == '💜 에메랄드':
                            baydang = 10
                        con = sqlite3.connect("./database/database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                        user_info = cur.fetchone()

                        cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount*baydang)), message.author.id))
                        con.commit()
                        await sent_first.edit(embed=discord.Embed(title="🎲 광질", description=f"**```yaml\n획득한 광물: {result}\n총 {math.floor(amount*baydang)}원에 당첨되셨습니다.```**",color=0x34c6eb))
                        
                    
                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.reply(embed=discord.Embed(title="배팅 실패", description="섹스.",color=0x34c6eb))
    
    if message.content.startswith('.로또 '):
        if message.content.split(" ")[1] == "올인":
            if (int(user_info[1]) >= 500):
                amount = int(user_info[1])
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
        else:
            amount = int(message.content.split(" ")[1])

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?);", (message.author.id, 0, None, 0, 0, 0,None ,None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
        user_info = cur.fetchone()
        baedang = 0

        if not (user_info == None):
            if (amount >= 500):
                if (amount <= user_info[1]):
                    if not (user_info[5] == 1):
                        cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] - amount, message.author.id))
                        con.commit()
                        cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                    (amount, message.author.id))
                        bet_amount = amount
                        add_bet(message.author.id,amount)
                        con.commit()
                        con.close()
                        sent_first = await message.reply(embed=discord.Embed(title="🎲 로또", description=f"**```yaml\n{amount}원\n\nDM을 확인해주세요.```**",color=0x34c6eb))
                        user = message.author
                        await user.send("1부터 45 사이의 숫자 6개를 입력해주세요.")

                        def check(msg):
                            return msg.author == user and msg.channel == user.dm_channel and msg.content.isdigit()

                        user_numbers = []
                        while len(user_numbers) < 6:
                            try:
                                msg = await client.wait_for('message', check=check, timeout=30.0)
                                number = int(msg.content)
                                if number < 1 or number > 45:
                                    await user.send(embed=talmoembed("**🎲 배팅 실패**", "**1부터 45까지의 숫자만 입력이 가능합니다.\n다시 시도해주세요.**"))
                                    return
                                elif number in user_numbers:
                                    await user.send(embed=talmoembed("**🎲 배팅 실패**", "**중복된 숫자를 입력할 수 없습니다.**"))
                                    return
                                else:
                                    if len(user_numbers) < 5:
                                        await user.send("네, 다음 번호를 입력해주세요.")
                                        user_numbers.append(number)
                                    else:
                                        await user.send("네, 번호를 모두 정상적으로 받았습니다.")
                                        user_numbers.append(number)
                            except asyncio.TimeoutError:
                                await user.send(embed=talmoembed("**🎲 배팅 실패**", "**시간 초과되었습니다.**"))
                                return

                        bot_numbers = random.sample(range(1, 46), 6)
                        matched_numbers = set(user_numbers).intersection(bot_numbers)

                        if len(matched_numbers) == 3:
                            baedang = 5
                        if len(matched_numbers) == 4:
                            baedang = 50
                        if len(matched_numbers) == 5:
                            baedang = 500
                        if len(matched_numbers) == 6:
                            baedang = 5000

                        await user.send(f"당신이 선택한 숫자: {sorted(user_numbers)}")
                        await user.send(f"봇이 선택한 숫자: {sorted(bot_numbers)}")
                        await user.send(f"일치하는 숫자: {len(matched_numbers)}개")
                        con = sqlite3.connect("./database/database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                        user_info = cur.fetchone()

                        cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (amount*baedang)), message.author.id))
                        con.commit()
                        await user.send(embed=talmoembed("🎲 로또 결과", f"**```당신이 선택한 숫자: {sorted(user_numbers)}\n로또 결과: {sorted(bot_numbers)}\n일치하는 숫자: {len(matched_numbers)}개\n\n당첨금: {math.floor(amount*baedang)}```**"))
                        
                    
                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                con.close()
                await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
        else:
            con.close()
            await message.reply(embed=discord.Embed(title="배팅 실패", description="섹스.",color=0x34c6eb))
    
    if message.content.startswith('.블랙잭 '):
        global bjamount
        global bjusing
        global betauthor
        if bjusing == 0:
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()
            if message.content.split(" ")[1] == "올인":
                if (int(user_info[1]) >= 500):
                    bjamount = int(user_info[1])
                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                bjamount = int(message.content.split(" ")[1])


            betauthor = message.author.id

            if (user_info == None):
                cur.execute("INSERT INTO users Values(?, ?, ?, ?, ?, ?,?,?);", (message.author.id, 0, None, 0, 0, 0,None ,None))
                con.commit()
                con.close()

            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()

            if not (user_info == None):
                if (bjamount >= 500):
                    if (bjamount <= user_info[1]):
                        if not (user_info[5] == 1):
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;", (user_info[1] - bjamount, message.author.id))
                            con.commit()
                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                        (bjamount, message.author.id))
                            add_bet(message.author.id,bjamount)
                            con.commit()
                            con.close()                               
                            bjusing = 1
                            def deal(deck):
                                hand = []
                                random.shuffle(deck)
                                for i in range(2):
                                    card = deck.pop()
                                    if card == 11:
                                        card = 'J'
                                    if card == 12:
                                        card = 'Q'
                                    if card == 13:
                                        card = 'K'
                                    if card == 14:
                                        card = 'A'
                                    hand.append(card)
                                return hand
                            # Adds cards to  hand
                            def draw(deck, hand):
                                card = deck.pop()
                                if card == 11:
                                    card = 'J'
                                if card == 12:
                                    card = 'Q'
                                if card == 13:
                                    card = 'K'
                                if card == 14:
                                    card = 'A'
                                hand.append(card)

                            # Calculates the total of a hand
                            def total(hand):
                                total = 0
                                # Creates a hidden hand that sorts itself
                                calchand = []
                                for card in hand:
                                    calchand.append(card)
                                # Put face cards to number to sort them to maintain elasticity of ACE
                                for i in range(len(calchand)):
                                    if calchand[i] == 'J' or calchand[i] == 'Q' or calchand[i] == 'K':
                                        calchand[i] = 99
                                    if calchand[i]  == 'A':
                                        calchand[i] = 100
                                calchand.sort()
                                # Calculate the total of the hand
                                for card in calchand:
                                    if card == 99:
                                        total += 10
                                    elif card == 100:
                                        if total >= 11:
                                            total += 1
                                        else:
                                            total += 11
                                    else:
                                        total += card
                                return total


                            print(message.author)
                            global playing
                            playing = True
                            global deck
                            deck = [2, 3, 4, 5, 6,2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14] * 4
                            global player_hand
                            player_hand = deal(deck)
                            global dealer_hand
                            dealer_hand = deal(deck)
                        
                            msg = await message.reply(embed=discord.Embed(title="🎲 블랙잭", description=f"**```{bjamount}원 배팅 완료\n\n카드를 분배합니다.```**",color=0x34c6eb))
                            await asyncio.sleep(1)
                            await msg.edit(embed=discord.Embed(title="🎲 블랙잭", description=f"**```yaml\n유저 카드:  [{player_hand[0]}, ?], 딜러 카드: [?, ?]```**",color=0x34c6eb))
                            await asyncio.sleep(1)
                            await msg.edit(embed=discord.Embed(title="🎲 블랙잭", description=f"**```yaml\n유저 카드:  [{player_hand[0]}, ?], 딜러 카드: [{dealer_hand[0]}, ?]```**",color=0x34c6eb))
                            await asyncio.sleep(1)
                            await msg.edit(embed=discord.Embed(title="🎲 블랙잭", description=f"**```yaml\n유저 카드:  {player_hand}, 딜러 카드: [{dealer_hand[0]}, ?]```**",color=0x34c6eb))
                            await asyncio.sleep(1)
                            await msg.edit(embed=discord.Embed(title="🎲 블랙잭", description=f"**```yaml\n유저 카드:  {player_hand}, 딜러 카드: [{dealer_hand[0]}, 미공개]```**",color=0x34c6eb))
                            await message.channel.send("히트 또는 스탠드를 입력해주세요.")
                        else:
                            con.close()
                            await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```봇 사용이 차단된 유저입니다.```**"))
                    else:
                        con.close()
                        await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅이 불가합니다.```**"))
            else:
                con.close()
                await message.reply(embed=discord.Embed(title="배팅 실패", description="섹스.",color=0x34c6eb))
        else:
            con.close()
            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**누군가 사용중입니다.\n오류 방지를 위해 잠시 기다려주세요.\n오류라면 관리자에게 문의하세요.**"))
            return

    if message.content == "히트" and playing == True and message.author.id == betauthor:

        def deal(deck):
            hand = []
            random.shuffle(deck)
            for i in range(2):
                card = deck.pop()
                if card == 11:
                    card = 'J'
                if card == 12:
                    card = 'Q'
                if card == 13:
                    card = 'K'
                if card == 14:
                    card = 'A'
                hand.append(card)
            return hand
        # Adds cards to  hand
        def draw(deck, hand):
            card = deck.pop()
            if card == 11:
                card = 'J'
            if card == 12:
                card = 'Q'
            if card == 13:
                card = 'K'
            if card == 14:
                card = 'A'
            hand.append(card)

        # Calculates the total of a hand
        def total(hand):
            total = 0
            # Creates a hidden hand that sorts itself
            calchand = []
            for card in hand:
                calchand.append(card)
            # Put face cards to number to sort them to maintain elasticity of ACE
            for i in range(len(calchand)):
                if calchand[i] == 'J' or calchand[i] == 'Q' or calchand[i] == 'K':
                    calchand[i] = 99
                if calchand[i]  == 'A':
                    calchand[i] = 100
            calchand.sort()
            # Calculate the total of the hand
            for card in calchand:
                if card == 99:
                    total += 10
                elif card == 100:
                    if total >= 11:
                        total += 1
                    else:
                        total += 11
                else:
                    total += card
            return total


        draw(deck, player_hand)
        await message.reply(embed=discord.Embed(title="블랙잭", description=f"**```yaml\n유저 카드: {player_hand}, 딜러 카드: [{dealer_hand[0]}, 미공개]```**",color=0x34c6eb))
     

        if total(player_hand) > 21:
            await message.channel.send(embed=talmoembed("🎲 패배", f"**딜러에게 패배해 {bjamount}원을 잃었습니다.**"))
            bjusing = 0
            playing = False
    
    if message.content == '스탠드' and playing == True and message.author.id == betauthor:
        
        def deal(deck):
            hand = []
            random.shuffle(deck)
            for i in range(2):
                card = deck.pop()
                if card == 11:
                    card = 'J'
                if card == 12:
                    card = 'Q'
                if card == 13:
                    card = 'K'
                if card == 14:
                    card = 'A'
                hand.append(card)
            return hand
        # Adds cards to  hand
        def draw(deck, hand):
            card = deck.pop()
            if card == 11:
                card = 'J'
            if card == 12:
                card = 'Q'
            if card == 13:
                card = 'K'
            if card == 14:
                card = 'A'
            hand.append(card)

        # Calculates the total of a hand
        def total(hand):
            total = 0
            # Creates a hidden hand that sorts itself
            calchand = []
            for card in hand:
                calchand.append(card)
            # Put face cards to number to sort them to maintain elasticity of ACE
            for i in range(len(calchand)):
                if calchand[i] == 'J' or calchand[i] == 'Q' or calchand[i] == 'K':
                    calchand[i] = 99
                if calchand[i]  == 'A':
                    calchand[i] = 100
            calchand.sort()
            # Calculate the total of the hand
            for card in calchand:
                if card == 99:
                    total += 10
                elif card == 100:
                    if total >= 11:
                        total += 1
                    else:
                        total += 11
                else:
                    total += card
            return total

        while total(dealer_hand) < 17:
            draw(deck, dealer_hand)
            await message.channel.send('딜러가 카드를 뽑았습니다.')
            if total(dealer_hand) > 21:
                await message.channel.send(embed=talmoembed("🎲 승리", f"**딜러에게 승리해 {bjamount * 1.95}원을 얻었습니다.**"))
                bjusing = 0
                con = sqlite3.connect("./database/database.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                user_info = cur.fetchone()

                cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (bjamount * 1.95)), message.author.id))
                con.commit()
                playing = False
                return
        await message.reply(embed=discord.Embed(title="블랙잭", description=f"**```yaml\n유저 카드: {player_hand} ({total(player_hand)}), 딜러 카드: {dealer_hand} ({total(dealer_hand)})```**",color=0x34c6eb))
                        
        if total(dealer_hand) > total(player_hand) and total(dealer_hand) <= 21:
            await message.channel.send(embed=talmoembed("🎲 패배", f"**딜러에게 패배해 {bjamount}원을 잃었습니다.**"))
            bjusing = 0
            playing = False
        elif total(dealer_hand) == total(player_hand) and total(dealer_hand) <= 21:
            await message.channel.send(embed=talmoembed("🎲 타이", f"**딜러와 무승부 해 {bjamount}원을 다시 받았습니다.**"))
            bjusing = 0
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()

            cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (bjamount * 1)), message.author.id))
            con.commit()

        else:
            await message.channel.send(embed=talmoembed("🎲 승리", f"**딜러에게 승리해 {bjamount * 1.95}원을 얻었습니다.**"))
            bjusing = 0
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()

            cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + (bjamount * 1.95)), message.author.id))
            con.commit()
            playing = False
    
    if message.content.startswith('!꽁머니초기화'):
        if len(message.mentions) > 0:
            member = message.mentions[0]
            if message.author.id in admin_id:
                user_data = data.get(member.id, {})
                user_data['date'] = datetime.date.today()
                user_data['count'] = 0
                data[member.id] = user_data
                await message.channel.send(f'{member.mention} 님의 꽁머니 사용 횟수가 초기화되었습니다.')
            else:
                await message.channel.send('권한이 없습니다.')
        else:
            await message.channel.send('멘션된 사용자가 없습니다.')
    
    if message.content.startswith(".꽁머니"):
        user = message.author.id
        log = ""

        id = 출금로그
        channel = client.get_channel(int(id))
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
        if money >= 50000:
            if message.channel.id == 1103334104155574295 or message.channel.id == 1109732419982069871:
                con = sqlite3.connect("./database/database.db")
                cur = con.cursor()
                cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
                user_info = cur.fetchone()

                a = ["꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝",  "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝",  "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝", "꽝",  "꽝", "꽝", "꽝", "꽝", '이천','이천', '삼천', '사천', '오천']
                c = random.choice(a)
                if c == "꽝":
                    await message.reply(embed=talmoembed("💸 꽁머니", f"**```아쉽네요. 나중에 다시 시도해봐요!```**"))
                    return
                elif c == "이천":
                    write_rolling(message.author.id,rolling)
                    write_chung(message.author.id,2000)
                    await message.reply(embed=talmoembed("💸 꽁머니", f"**```당첨! 축하드려요! `2,000원`에 당첨되셨어요! 지갑에 넣어드릴게요!```**"))
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + 2000), message.author.id))
                    con.commit()
                elif c == "삼천":
                    write_rolling(message.author.id,rolling)
                    write_chung(message.author.id,3000)
                    await message.reply(embed=talmoembed("💸 꽁머니", f"**```당첨! 축하드려요! `3,000원`에 당첨되셨어요! 지갑에 넣어드릴게요!```**"))
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + 3000), message.author.id))
                    con.commit()
                elif c == "사천":
                    write_rolling(message.author.id,rolling)
                    write_chung(message.author.id,4000)
                    await message.reply(embed=talmoembed("💸 꽁머니", f"**```당첨! 축하드려요! `4,000원`에 당첨되셨어요! 지갑에 넣어드릴게요!```**"))
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + 4000), message.author.id))
                    con.commit()
                elif c == "오천":
                    write_rolling(message.author.id,rolling)
                    write_chung(message.author.id,5000)
                    await message.reply(embed=talmoembed("💸 꽁머니", f"**```당첨! 축하드려요! `5,000원`에 당첨되셨어요! 지갑에 넣어드릴게요!```**"))
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;", (round(user_info[1] + 5000), message.author.id))
                    con.commit()
            else:
                await message.reply(embed=talmoembed("💸 꽁머니", f"**전용 채널에서 사용해주세요.**"))
                return
        else:
            await message.reply(embed=talmoembed("💸 꽁머니", f"**<@&1106870319878242365> 등급 이상을 소유하고 있어야 꽁머니를 지급 받을 수 있어요.**"))
                
    
    if message.content.startswith(f'.minegame') or message.content.startswith(f'.마인'):
        global using
        if using == 0: # 동시사용 불가를 위해 사용중인지 확인
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()

            if (user_info == None):
                cur.execute("INSERT INTO users Values(?, ?, ?, ?);", (message.author.id, 0, 0, 0))
                con.commit()
                con.close()
            con.close()
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (message.author.id,))
            user_info = cur.fetchone()
            if message.content.split(" ")[1] == "올인":
                if (int(user_info[1]) >= 500):
                    amount = int(user_info[1])
                else:
                    con.close()
                    await message.channel.send(embed=failembed("**🎲 배팅 실패**", "**```보유 금액이 부족합니다.```**"))
            else:
                amount = int(message.content.split(" ")[1])

            if not (user_info[3] == 3):
                if amount > 500:
                    if user_info[1] >= int(amount):
                        global 조작해제
                        조작해제 = 0
                        if int(amount) == 0 :
                            조작해제 = 1
                            print(f"{message.author}님의 게임에서 조작해제모드가 켜짐")
                            webhook = DiscordWebhook(url=게임로그웹훅, content=f"{message.author}님의 게임에서 조작해제모드가 켜짐 배팅금 : {amount}")
                            response = webhook.execute()
                        if message.author.id in admin_id:
                            조작해제 = 1
                            print(f"{message.author}님의(관리자) 게임에서 조작해제모드가 켜짐")
                            webhook = DiscordWebhook(url=게임로그웹훅, content=f"{message.author}님의(관리자) 게임에서 조작해제모드가 켜짐 배팅금 : {amount}")
                            response = webhook.execute()
                        global player_id
                        global player_name
                        global betmoney
                        if using == 0: # 동시사용 불가를 위해 사용중인지 확인
                            betmoney = amount
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                        (user_info[1] - int(amount), message.author.id))
                            con.commit()
                            cur.execute("UPDATE users SET bet_amount = ? WHERE id == ?;",
                                        (amount, message.author.id))
                            con.commit()
                            cur.execute("UPDATE users SET bet_money = ? WHERE id == ?;",(int(amount), message.author.id))
                            con.commit()
                            webhook = DiscordWebhook(url=게임로그웹훅, content=f"{message.author}님이 게임을 시작함 배팅금 : {amount}")
                            response = webhook.execute()
                            count = 0 # 시작전 다이아 개수 초기화 
                            using = 1 # 동시사용 불가 확인시 사용중으로 만들기
                            global bomb
                            bomb = str(random.randrange(1,26)) # 폭탄 위치 정하기 1이상 26미만
                            print(f"{message.author}님의 폭탄위치는 {bomb}번 입니다") # 폭탄위치 cmd에 출력
                            webhook = DiscordWebhook(url=게임로그웹훅, content=f"{message.author}님의 폭탄위치는 {bomb}번 입니다")
                            response = webhook.execute()
                            global grid
                            grid = ['⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏']
                            global already_used
                            already_used = [] # 이미 누른 버튼인지 확인하는 리스트
                            player_name = message.author
                            player_id = message.author.id # 플레이어만 버튼 누를수있게
                            embed=discord.Embed(title=f"RICHLAND",description=f"```yaml\n배팅금 : {amount}```",color=0x2f3136)
                            #await message.channel.send(embed=embed)
                            await message.channel.send(embed=embed,
                                components = [
                                    [
                                        Button(label = grid[0], custom_id = "1"),
                                        Button(label = grid[1], custom_id = "2"),
                                        Button(label = grid[2], custom_id = "3"),
                                        Button(label = grid[3], custom_id = "4"),
                                        Button(label = grid[4], custom_id = "5"),
                                    ],[
                                        Button(label = grid[5], custom_id = "6"),
                                        Button(label = grid[6], custom_id = "7"),
                                        Button(label = grid[7], custom_id = "8"),
                                        Button(label = grid[8], custom_id = "9"),
                                        Button(label = grid[9], custom_id = "10"),
                                    ],[
                                        Button(label = grid[10], custom_id = "11"),
                                        Button(label = grid[11], custom_id = "12"),
                                        Button(label = grid[12], custom_id = "13"),
                                        Button(label = grid[13], custom_id = "14"),
                                        Button(label = grid[14], custom_id = "15"),
                                    ],[
                                        Button(label = grid[15], custom_id = "16"),
                                        Button(label = grid[16], custom_id = "17"),
                                        Button(label = grid[17], custom_id = "18"),
                                        Button(label = grid[18], custom_id = "19"),
                                        Button(label = grid[19], custom_id = "20"),
                                    ],[
                                        Button(label = grid[20], custom_id = "21"),
                                        Button(label = grid[21], custom_id = "22"),
                                        Button(label = grid[22], custom_id = "23"),
                                        Button(label = grid[23], custom_id = "24"),
                                        Button(label = grid[24], custom_id = "25"),
                                    ]
                                ]
                            )
                        else:
                            await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                    else:
                        await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```보유금액이 부족합니다.```**"))
                else:
                    await message.channel.send(embed=talmoembed("**🎲 배팅 실패**", "**```500원 미만의 금액은 배팅할 수 없습니다.```**"))
            else:
                await message.reply(embed=discord.Embed(title="배팅 실패", description="당신은 봇 사용이 금지되어 있습니다.",color=0x34c6eb))
        else:
            await message.reply(embed=discord.Embed(title="배팅 실패", description="이미 다른 유저가 사용중입니다.\n버그라면 관리자에게 문의하세요. :thinking:",color=0x34c6eb))

    if message.content.startswith('.초기화 마인'):
        if message.author.id in admin_id:
            using=0
            await message.channel.send('완료 게이야!')
        else:
            await message.reply('권력이 없슴니다')


    if message.content.startswith('.초기화 블랙잭'):
        if message.author.id in admin_id:
            bjusing=0
            await message.channel.send('완료 게이야!')
        else:
            await message.reply('권력이 없슴니다')
    
    
    if message.content.startswith(".골라 "):
        try:
            onerhffk = message.content.split(" ")[1]
            tworhffk = message.content.split(" ")[2]
        except:
            await message.reply(embed=talmoembed("고르기 실패", f"**`명령어를 잘못 입력하셨어요. 선택지는 최대 2개까지 가능해요.`**"))
        
        rhffk = [onerhffk, tworhffk]
        realrhffk = random.choice(rhffk)
        
        if onerhffk == tworhffk:
            await message.channel.send("두개가 똑같잖아요 ㅗ")
            return

        await message.reply(embed=talmoembed("골랐다!",f"**난 이게 마음에 드네요!\n`{onerhffk}` or `{tworhffk}`\n\n하지만 나는 `{realrhffk}`가 마음에 들어요!**"))
    
    if message.content.startswith(".행운"):
        
        user_id = message.author.id

        # 이전에 저장된 행운 값이 있는지 확인
        if user_id in user_luck:
            luck = user_luck[user_id]
        else:
            # 새로운 랜덤 행운 값 생성
            luck = random.randint(0, 100)
            user_luck[user_id] = luck
        
        if luck > 0 and luck <= 30:
            luckmsg = "운이 매우 안 좋네요!"
        elif luck > 30 and luck <= 65:
            luckmsg = "운이 그럭저럭 좋지도 않고 나쁘지도 않네요!"
        elif luck > 65 and luck <= 80:
            luckmsg = "좋은 일이 있으실 거 같아요!"
        else:
            luckmsg = "오늘은 좋은 일만 있을 거예요!"

        await message.reply(embed=talmoembed("오늘의 행운 점수는?",f"오늘 당신의 행운 점수는 `{luck}점`입니다!\n{luckmsg}"))
    
    if message.content.startswith(".청소"):
        splited_msg = message.content.split(" ")
        clean_amount_s = splited_msg[1]
        clean_amount = int(clean_amount_s)
        if message.author.id in admin_id:
            x100_clean = 0
            while clean_amount > 100:
                clean_amount -= 100
                x100_clean += 1
            while not x100_clean == 0:
                x100_clean -= 1
                await message.channel.purge(limit=100)
            await message.channel.purge(limit=clean_amount+1)
            bobb = await message.channel.send(clean_amount_s + "개의 메시지를 청소했습니다.")
            await asyncio.sleep(1)
            await bobb.delete()


@client.event
async def on_button_click(interaction):
    global doing_bet
    global ktotal
    global mtotal
    global bkr_p
    global bkr_b
    global bkr_d
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
    global using
    global count
    # 용호
    global dt_round
    global lotto_round
    global dt_total_d
    global dt_total_t
    global doing_bet3
    global doing_bet7
    global d_card
    global t_card
    global dt_on
    global grid
    global using
    global count
    global player_id
    global player_name
    global bomb
    global amount
    global lbkramount
    global 조작해제
    
    global 충전중
    global betmoney

    
    def talmoembed(embedtitle, description):
        return discord.Embed(title=embedtitle, description=description, color=0xffffff)


    con = sqlite3.connect("./database/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
    user_info = cur.fetchone()

    if (user_info == None):
        cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
            interaction.user.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None))
        con.commit()


        # if interaction.custom_id == "코인투자":
        #     con = sqlite3.connect("./database/database.db")
        #     cur = con.cursor()
        #     cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
        #     user_info = cur.fetchone()

        #     if not (user_info[5] == 3):
        #         if user_info[1] >= 500:
        #             if not interaction.user.id in doing_bet3:
        #                 doing_bet3.append(interaction.user.id)
        #                 options = []
        #                 for i in range(1, (user_info[1] // 1000) + 1 if user_info[1] // 1000 < 24 else 25):
        #                     options.append(
        #                         SelectOption(description=f"",
        #                                      label=f"{1000 * i}", value=f"{1000 * i}"))
        #                 await interaction.respond(
        #                     embed=discord.Embed(title='금액 선택', description='매수할 금액을 선택해주세요.',
        #                                         color=0x0000FF)
        #                     ,
        #                     components=[
        #                         [Select(placeholder=f"매수액", options=options)]
        #                     ]
        #                 )
        #             else:
        #                 await interaction.respond(content="이미 매수중이십니다.")
        #             inter = await client.wait_for("select_option", check=None)
        #             amount = inter.values[0]
        #             cur.execute("UPDATE users SET money = ? WHERE id == ?;",
        #                         (user_info[1] - int(amount), interaction.user.id))
        #             con.commit()
        #             cur.execute("UPDATE users SET coin_bet_money = ? WHERE id == ?;",
        #                         (amount, interaction.user.id))
        #             con.commit()
        #             try:
        #                 await inter.respond(embed=discord.Embed(title="선택 성공",
        #                                                         description=f"{amount}원을 성공적으로 매수했습니다.",
        #                                                         color=0x2f3136))
        #                 cur.execute("UPDATE users SET perc = ? WHERE id == ?;",
        #                             (random.randint(-100,100), interaction.user.id))
        #                 con.commit()
        #                 con.close()
        #             except:
        #                 pass
        #         else:
        #             await interaction.respond(embed=discord.Embed(title="잔액부족",
        #                                                           description=f"잔고가 투자하기에 너무 낮습니다.", color=0x2f3136))
        #     else:
        #         await interaction.respond(embed=discord.Embed(title="매수불가",
        #                                                       description=f"당신은 차단된유저입니다.", color=0x2f3136))
        # if interaction.custom_id == "돈빼기":
        #     try:
        #         con = sqlite3.connect("./database/database.db")
        #         cur = con.cursor()
        #         cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
        #         user_info = cur.fetchone()
        #         if not (user_info[5] == 3):
        #             await interaction.respond(content=f"> `{user_info[30]}`원을 성공적으로 회수하였습니다.\n> \n> {user_info[1]}원 -> {user_info[1]+user_info[30]}원")
        #             cur.execute("UPDATE users SET money = ? WHERE id == ?;",
        #                         (user_info[1]+user_info[30], interaction.user.id))
        #             con.commit()
        #             cur.execute("UPDATE users SET coin_bet_money = ? WHERE id == ?;",
        #                         (0, interaction.user.id))
        #             con.commit()
        #             con.close()
        #             doing_bet3.remove(interaction.user.id)
        #         else:
        #             await interaction.respond(embed=discord.Embed(title="매도불가",
        #                                                         description=f"당신은 차단된유저입니다.", color=0x2f3136))
        #     except:
        #         await interaction.respond(embed=discord.Embed(title="매도불가",
        #                                                         description=f"당신은 배팅상태가아닙니다.", color=0x2f3136))

        # if interaction.component.custom_id == "플레이어":
        #     con = sqlite3.connect("./database/database.db")
        #     cur = con.cursor()
        #     cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
        #     user_info = cur.fetchone()
        #     if not (user_info[5] == 3):
        #         if user_info[1] >= 500:
        #             if not interaction.user.id in doing_bet2:
        #                 doing_bet2.append(interaction.user.id)
        #                 pick = interaction.component.custom_id
        #                 options = []
        #                 for i in range(1, (user_info[1] // 1000) + 1 if user_info[1] // 1000 < 24 else 25):
        #                     options.append(
        #                         SelectOption(description=f"",
        #                                     label=f"{1000 * i}", value=f"{1000 * i}"))
        #                 await interaction.respond(
        #                     embed=discord.Embed(title='칩 선택', description='배팅할 금액을 선택해주세요',
        #                                         color=0x0000FF)
        #                     ,
        #                     components=[
        #                         [Select(placeholder=f"플레이어", options=options)]
        #                     ]
        #                 )
        #             else:
        #                 await interaction.respond(content="이미 배팅중이십니다.\n현재 배팅하고있는 버튼을 배팅하시거나 다음회차에 배팅해주세요.")
        #             inter = await client.wait_for("select_option", check=None)
        #             amount = inter.values[0]
        #             cur.execute("UPDATE users SET money = ? WHERE id == ?;",
        #                         (user_info[1] - int(amount), interaction.user.id))
        #             con.commit()
        #             cur.execute("UPDATE users SET rotoladder_bet_pick = ? WHERE id == ?;",
        #                         (pick, interaction.user.id))
        #             con.commit()
        #             cur.execute("UPDATE users SET rotoladder_bet_money = ? WHERE id == ?;",
        #                         (amount, interaction.user.id))
        #             con.commit()
        #             con.close()
        #             try:
        #                 await inter.respond(embed=discord.Embed(title="선택 성공",
        #                                                         description=f"{amount}원을 플레이어에 배팅했습니다.\n메시지를 전부 닫아주세요.",
        #                                                         color=0x2f3136))
        #                 await interaction.channel.send(f"{interaction.user}님이 {amount}원을 플레이어에 배팅했습니다.")
        #                 bkr_total_p = bkr_total_p + int(amount)
        #                 print(bkr_total_p)
        #             except Exception as e:
        #                 print(e)
        #         else:
        #             await interaction.respond(embed=discord.Embed(title="잔액부족",
        #                                                         description=f"잔고가 플레이하기에 너무 낮습니다.",color=0x2f3136))
        #     else:
        #         await interaction.respond(embed=discord.Embed(title="배팅불가",
        #                                                         description=f"당신은 차단된유저입니다.",color=0x2f3136))
        # if interaction.component.custom_id == "뱅커":
        #     con = sqlite3.connect("./database/database.db")
        #     cur = con.cursor()
        #     cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
        #     user_info = cur.fetchone()
        #     if not (user_info[5] == 3):
        #         if user_info[1] >= 500:
        #             if not interaction.user.id in doing_bet2:
        #                 doing_bet2.append(interaction.user.id)
        #                 pick = interaction.component.custom_id
        #                 options = []
        #                 for i in range(1, (user_info[1] // 1000) + 1 if user_info[1] // 1000 < 24 else 25):
        #                     options.append(
        #                         SelectOption(description=f"",
        #                                     label=f"{1000 * i}", value=f"{1000 * i}"))
        #                 await interaction.respond(
        #                     embed=discord.Embed(title='칩 선택', description='배팅할 금액을 선택해주세요',
        #                                         color=0xFF0000)
        #                     ,
        #                     components=[
        #                         [Select(placeholder=f"뱅커", options=options)]
        #                     ]
        #                 )
        #             else:
        #                 await interaction.respond(content="이미 배팅중이십니다.\n현재 배팅하고있는 버튼을 배팅하시거나 다음회차에 배팅해주세요.")
        #             inter = await client.wait_for("select_option", check=None)
        #             amount = inter.values[0]
        #             cur.execute("UPDATE users SET money = ? WHERE id == ?;",
        #                         (user_info[1] - int(amount), interaction.user.id))
        #             con.commit()
        #             cur.execute("UPDATE users SET rotoladder_bet_pick = ? WHERE id == ?;",
        #                         (pick, interaction.user.id))
        #             con.commit()
        #             cur.execute("UPDATE users SET rotoladder_bet_money = ? WHERE id == ?;",
        #                         (amount, interaction.user.id))
        #             con.commit()
        #             con.close()
        #             try:
        #                 await inter.respond(embed=discord.Embed(title="선택 성공",
        #                                                         description=f"{amount}원을 뱅커에 배팅했습니다.\n메시지를 전부 닫아주세요.",
        #                                                         color=0x2f3136))
        #                 await interaction.channel.send(f"{interaction.user}님이 {amount}원을 뱅커에 배팅했습니다.")
        #                 bkr_total_b=bkr_total_b+int(amount)
        #                 print(bkr_total_b)
        #             except Exception as e:
        #                 print(e)
        #         else:
        #             await interaction.respond(embed=discord.Embed(title="잔액부족",
        #                                                         description=f"잔고가 플레이하기에 너무 낮습니다.",
        #                                                        color=0x2f3136))
        #     else:
        #         await interaction.respond(embed=discord.Embed(title="배팅불가",
        #                                                         description=f"당신은 차단된유저입니다.",color=0x2f3136))

        # if interaction.component.custom_id == "무승부":
        #     con = sqlite3.connect("./database/database.db")
        #     cur = con.cursor()
        #     cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
        #     user_info = cur.fetchone()
        #     if not (user_info[5] == 3):
        #         if user_info[1] >= 500:
        #             if not interaction.user.id in doing_bet2:
        #                 doing_bet2.append(interaction.user.id)
        #                 pick = interaction.component.custom_id
        #                 options = []
        #                 for i in range(1, (user_info[1] // 1000) + 1 if user_info[1] // 1000 < 24 else 25):
        #                     options.append(
        #                         SelectOption(description=f"",
        #                                     label=f"{1000 * i}", value=f"{1000 * i}"))
        #                 await interaction.respond(
        #                     embed=discord.Embed(title='칩 선택', description='배팅할 금액을 선택해주세요',
        #                                         color=0x00FF00)
        #                     ,
        #                     components=[
        #                         [Select(placeholder=f"무승부", options=options)]
        #                     ]
        #                 )
        #             else:
        #                 await interaction.respond(content="이미 배팅중이십니다.\n현재 배팅하고있는 버튼을 배팅하시거나 다음회차에 배팅해주세요.")
        #             inter = await client.wait_for("select_option", check=None)
        #             amount = inter.values[0]
        #             cur.execute("UPDATE users SET money = ? WHERE id == ?;",
        #                         (user_info[1] - int(amount), interaction.user.id))
        #             con.commit()
        #             cur.execute("UPDATE users SET rotoladder_bet_pick = ? WHERE id == ?;",
        #                         (pick, interaction.user.id))
        #             con.commit()
        #             cur.execute("UPDATE users SET rotoladder_bet_money = ? WHERE id == ?;",
        #                         (amount, interaction.user.id))
        #             con.commit()
        #             con.close()
        #             try:
        #                 await inter.respond(embed=discord.Embed(title="선택 성공",
        #                                                         description=f"{amount}원을 무승부에 배팅했습니다.\n메시지를 전부 닫아주세요.",
        #                                                         color=0x2f3136))
        #                 await interaction.channel.send(f"{interaction.user}님이 {amount}원을 무승부에 배팅했습니다.")
        #             except:
        #                 pass
        #         else:
        #             await interaction.respond(embed=discord.Embed(title="잔액부족",
        #                                                         description=f"잔고가 플레이하기에 너무 낮습니다.",color=0x2f3136))
        #     else:
        #         await interaction.respond(embed=discord.Embed(title="배팅불가",
        #                                                         description=f"당신은 차단된유저입니다.",color=0x2f3136))
    
    
    if interaction.component.custom_id == "계좌충전":
        user_id = interaction.user.id
        user = interaction.user.id
        name = interaction.user.name
        member = interaction.user

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                interaction.user.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            try:
                nam = await interaction.user.send(embed=talmoembed("🎲 계좌 충전", "**입금자명[실명]을 입력해주세요.**"))
                await interaction.respond(embed=talmoembed("🎲 계좌 충전", "**DM을 확인해주세요.**"))
                dobae = await client.get_channel(요청채널).send("@everyone")
                await dobae.delete()
                dobae = await client.get_channel(요청채널).send("@everyone")
                await dobae.delete()
                dobae = await client.get_channel(요청채널).send(f"{interaction.user}님이 계좌 충전 버튼을 클릭하셨습니다. 대기하세요!")
            except:
                await interaction.respond(embed=talmoembed("🎲 계좌 충전", "**DM을 허용해주세요.**"))

            def check(name):
                return (isinstance(name.channel, discord.channel.DMChannel) and (interaction.user.id == name.author.id))

            try:
                name = await client.wait_for("message", timeout=60, check=check)
                await nam.delete()
                name = name.content
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 계좌 충전", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None

            mone = await interaction.user.send(embed=talmoembed("🎲 계좌 충전", "**충전할 금액을 입력해주세요.**"))

            def check(money):
                return (isinstance(money.channel, discord.channel.DMChannel) and (
                        interaction.user.id == money.author.id))

            try:
                money = await client.wait_for("message", timeout=60, check=check)
                await mone.delete()
                money = money.content
                if int(money) < 1000:
                    await interaction.user.send(embed=talmoembed("🎲 계좌 충전", "**최소 충전금액은 `1,000원` 이어야 합니다.**"))
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 계좌 충전", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None
            bonus_m = await interaction.user.send(embed=talmoembed("🎲 계좌 충전", "**선택하실 보너스를 선택해주세요.**"),
                                                  components=[Select(placeholder="선택하실 보너스를 입력해주세요",
                                                            options=bonus_selection,custom_id="계좌충전 보너스")])
            
            def check(bonus):
                return (isinstance(bonus.channel, discord.channel.DMChannel) and (
                        interaction.user.id == bonus.author.id) and (bonus.custom_id == "계좌충전 보너스"))
            bonus_amplier = 0
            bonus_rolling = 0
            try:
                bonus = await client.wait_for("select_option", timeout=60, check=check)
                bonus_split = bonus.values[0].split("-")
                bonus_amplier = float(bonus_split[0])
                bonus_rolling = int(bonus_split[1])
                await bonus_m.delete()
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 계좌 충전", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None
            if money.isdigit():
                await interaction.user.send(embed=discord.Embed(title="계좌 충전",
                                                                description=f"**입금 계좌 : {banks}**\n─────────────\n입금자명 : `{name}`\n입금 금액 : `{money}`원\n보너스 : {bonus_split[2]}",
                                                                color=0x2f3136))
                screenshot = await interaction.user.send(
                    embed=discord.Embed(description=f"충전 후 스크린샷을 5분 내에 보내주세요.", color=0x2f3136))

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
                                embed=discord.Embed(title="계좌 충전 실패", description="올바른 사진 형식이 아닙니다.",
                                                    color=0x2f3136))
                        except:
                            pass
                        return None
                except asyncio.TimeoutError:
                    try:
                        await interaction.user.send(embed=talmoembed("🎲 계좌 충전", "```yaml\n시간 초과되었습니다.```"))
                    except:
                        pass
                    return None

                access_embed = discord.Embed(title='계좌이체 충전 요청',
                                            description=f'디스코드 닉네임 : <@{interaction.user.id}>({interaction.user})\n입금자명 : {name}\n입금 금액 : {money}\n선택한 보너스 : {bonus_split[2]}',
                                            color=0x2f3136)
                try:
                    access_embed.set_image(url=sct)
                except:
                    try:
                        await interaction.user.send(embed=talmoembed("🎲 계좌 충전", "**올바른 사진 형식이 아닙니다..**"))
                    except:
                        pass
                    return None
                await interaction.user.send(
                    embed=discord.Embed(title="충전 요청 성공 ✅", description=f"관리자의 승인을 기다려주세요.",
                                        color=0x2f3136))
                access = Button(label="✅ 승인하기", custom_id="승인", style=ButtonStyle.green)
                deny = Button(label="❌ 거부하기", custom_id="거부", style=ButtonStyle.red)
                dobae = await client.get_channel(요청채널).send("@everyone")
                await dobae.delete()
                dobae = await client.get_channel(요청채널).send("@everyone")
                await dobae.delete()
                dobae = await client.get_channel(요청채널).send("@everyone")
                await dobae.delete()
                a_m = await client.get_channel(요청채널).send(embed=access_embed, components=
                ActionRow(
                    [access, deny],
                )
                                                        )
                while True:
                    interaction = await client.wait_for("button_click",
                                                        check=lambda inter: inter.custom_id != "",
                                                        timeout=None)
                    if interaction.custom_id == '승인':
                        await a_m.delete()
                        write_bet(user_id,0)
                        write_rolling(user_id,bonus_rolling)
                        add_chung1(user_id,float(money)*bonus_amplier)
                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                    (user_info[1] + float(money)*bonus_amplier, user_id))
                        con.commit()
                        ktotal += int(money)
                        con.close()
                        nojum = math.floor(float(money)*(bonus_amplier-1))
                        await client.get_user(user_id).send(embed=discord.Embed(title="계좌 충전 성공",
                                                                                description=f"{money}원이 충전되었습니다.\n\n**`이벤트로 인하여 {nojum}원이 추가로 지급되었습니다.`**",
                                                                                color=0x2f3136))
                        await client.get_channel(요청채널).send(
                            embed=discord.Embed(title="계좌 충전 성공", description=f"{interaction.user} \n\n<@{user_id}>님께 충전되었습니다. {money}원\n\n보너스 이벤트 {nojum}원\n선택 보너스 : {bonus_split[2]}",
                                                color=0x2f3136))
                        await client.get_channel(요청채널).send(f"{sct} <@{user_id}> 충전 스크린\n예금주는 {name}이었어용.")
                        log_id = 환전액로그
                        log_ch = client.get_channel(int(log_id))
                        await log_ch.send(f"<@{user_id}>님이 {int(money)}원을 충전하셨습니다! [보너스 이벤트 {nojum}원 추가지급]")
                        await asyncio.sleep(5)
                        guild = client.get_guild(int(1103334101043396669))
                        log = ""

                        id = 환전액로그
                        channel = client.get_channel(int(id))
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
                        number = int(money)
                        if number < 0 or number >= 1500000:
                            return
                        elif number < 3000:
                            return
                        elif number < 15000:
                            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 1')
                        elif number < 50000:
                            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 2')
                        elif number < 150000:
                            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 3')
                        elif number < 350000:
                            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 4')
                        elif number < 800000:
                            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 5')
                        elif number < 1500000:
                            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 6')
                        else:
                            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 7')

                        if role is None:
                            return
                        elif role in member.roles:
                            return
                        else:
                            await member.add_roles(role)
                            await client.get_user(user_id).send(f"RICHLAND 잔액 {number}원 누적 충전으로 인해 {role.name} 등급을 부여 받았습니다.")
                        
                    if interaction.custom_id == '거부':
                        await client.get_channel(요청채널).send(f"{sct} <@{user_id}> 충전 실패 스크린\n예금주는 {name}이었어용.")
                        await a_m.delete()
                        await client.get_user(user_id).send(
                            embed=discord.Embed(title="계좌 충전 실패", description=f"{interaction.user} 관리자님께서 충전을 거부하셨습니다.",
                                                color=0x2f3136))
                        await client.get_channel(요청채널).send(
                            embed=discord.Embed(title="계좌 충전 실패", description=f"{interaction.user}\n\n<@{user_id}>님의 계좌 충전이 거부되었습니다.",
                                                color=0x2f3136))

            else:
                await interaction.user.send(embed=talmoembed("🎲 계좌 충전", "**올바른 액수를 입력해주세요.**"))
    
    if interaction.custom_id == "culturelanddeposit":
        user_id = interaction.user.id
        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                interaction.user.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        user_info = cur.fetchone()
        try:
            ditto = await interaction.user.send(embed=discord.Embed(title="문화상품권 충전", description=f"문화상품권 핀번호를 `-`를 포함해서 입력해주세요.", color=0x5c6cdf))
            await interaction.respond(embed=discord.Embed(title="전송 성공", description="DM을 확인해주세요.", color=0x00ff00))
        except:
            await interaction.respond(embed=discord.Embed(title="문화상품권 충전 실패", description="DM을 차단하셨거나 메시지 전송 권한이 없습니다.", color=0xff0000))
            
            return None

        def check(msg):
            return (isinstance(msg.channel, discord.channel.DMChannel) and (len(msg.content) == 21 or len(msg.content) == 19) and (interaction.user.id == msg.author.id))
        try:
            msg = await client.wait_for("message", timeout=60, check=check)
            await ditto.delete()
        except asyncio.TimeoutError:
            try:
                await interaction.user.send(embed=discord.Embed(title="문화상품권 충전 실패", description="시간이 초과되었습니다.", color=0xff0000))
                
            except:
                pass
            return None
        
        bonus_m = await interaction.user.send(embed=talmoembed("🎲 문화상품권 충전", "**선택하실 보너스를 선택해주세요.**"),
                                                  components=[Select(placeholder="선택하실 보너스를 입력해주세요",
                                                            options=bonus_selection,custom_id="계좌충전 보너스")])
            
        def check(bonus):
            return (isinstance(bonus.channel, discord.channel.DMChannel) and (
                    interaction.user.id == bonus.author.id) and (bonus.custom_id == "계좌충전 보너스"))
        bonus_amplier = 0
        bonus_rolling = 0
        try:
            bonus = await client.wait_for("select_option", timeout=60, check=check)
            bonus_split = bonus.values[0].split("-")
            bonus_amplier = float(bonus_split[0])
            bonus_rolling = int(bonus_split[1])
            await bonus_m.delete()
        except asyncio.TimeoutError:
            try:
                await interaction.user.send(embed=talmoembed("🎲 문화상품권 충전", "```yaml\n시간 초과되었습니다.```"))
            except:
                pass
            return None

        access_embed = discord.Embed(title='문화상품권 충전 요청',
                                description=f'디스코드 닉네임 : <@{interaction.user.id}>({interaction.user})\n핀번호 : {msg.content}',
                                color=0x5c6cdf)
        await interaction.user.send(embed=discord.Embed(title="RICHLAND", description=f"**충전신청이 완료되었습니다.**\n승인이 빨리 되지 않는다면, 관리자에게 문의하세요.", color=0x00ff00))
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
            if interaction.custom_id == '승인':
                await a_m.delete()
                await client.get_channel(요청채널).send("충전된 문화상품권의 금액만 입력해주세요.")
                try:
                    msg1 = await client.wait_for("message", timeout=60)
                    msg1 = int(msg1.content)
                except asyncio.TimeoutError:
                    try:
                        await interaction.user.send(embed=discord.Embed(title="문화상품권 충전 승인 실패", description="시간이 초과되었습니다.", color=0xff0000))
                    except:
                        pass
                write_bet(user_id,0)
                write_rolling(user_id,bonus_rolling)
                add_chung1(user_id,float(msg1)*bonus_amplier)
                cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                            (user_info[1] + float(msg1)*bonus_amplier, user_id))
                con.commit()
                ktotal += int(msg1)
                con.close()
                nojum = math.floor(float(msg1)*(bonus_amplier-1))
                user = await client.fetch_user(user_id)
                await user.send(embed=discord.Embed(title="성공", description=f"충전되었습니다. {msg1}원", color=0x00ff00))

                await client.get_channel(요청채널).send(
                    embed=discord.Embed(title="문화상품권 충전 성공", description=f"<@{user_id}>님께 충전되었습니다. {msg1}원",
                                        color=0x5c6cdf))
                log_id = 환전액로그
                log_ch = client.get_channel(int(log_id))
                await log_ch.send(f"<@{user_id}>님이 {int(msg1)}원을 충전하셨습니다! [보너스 이벤트 {nojum}원 추가지급]")
                await asyncio.sleep(5)
                guild = client.get_guild(int(1103334101043396669))
                log = ""

                id = 환전액로그
                channel = client.get_channel(int(id))
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
                number = int(money)
                if number < 0 or number >= 1500000:
                    return
                elif number < 3000:
                    return
                elif number < 15000:
                    role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 1')
                elif number < 50000:
                    role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 2')
                elif number < 150000:
                    role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 3')
                elif number < 350000:
                    role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 4')
                elif number < 800000:
                    role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 5')
                elif number < 1500000:
                    role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 6')
                else:
                    role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 7')

                if role is None:
                    return
                elif role in member.roles:
                    return
                else:
                    await member.add_roles(role)
                    await client.get_user(user_id).send(f"RICHLAND 잔액 {number}원 누적 충전으로 인해 {role.name} 등급을 부여 받았습니다.")
            if interaction.custom_id == '거부':
                await a_m.delete()
                user = await client.fetch_user(user_id)
                await user.send(embed=discord.Embed(title="실패", description=f"잘못되거나 이미 사용된 문화상품권 입니다.", color=0xff0000))
                await client.get_channel(요청채널).send(
                    embed=discord.Embed(title="문화상품권 충전 실패", description=f"<@{user_id}>님의 문화상품권 충전이 거부되었습니다.",
                                        color=0x5c6cdf))

    if interaction.custom_id == "toss":
        user_id = interaction.user.id
        user = interaction.user
        user = interaction.user.id
        name = interaction.user.name

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                interaction.user.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            try:
                nam = await interaction.user.send(embed=talmoembed("🎲 TossPayments 충전", "**익명 송금 입금자명을 입력해주세요.**"))
                await interaction.respond(embed=talmoembed("🎲 TossPayments 충전", "**DM을 확인해주세요.**"))
            except:
                await interaction.respond(embed=talmoembed("🎲 TossPayments 충전", "**DM을 허용해주세요.**"))

            def check(name):
                return (isinstance(name.channel, discord.channel.DMChannel) and (interaction.user.id == name.author.id))

            try:
                name = await client.wait_for("message", timeout=60, check=check)
                await nam.delete()
                name = name.content
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 TossPayments 충전", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None

            mone = await interaction.user.send(embed=talmoembed("🎲 TossPayments 충전", "**충전할 금액을 입력해주세요.**"))

            def check(money):
                return (isinstance(money.channel, discord.channel.DMChannel) and (
                        interaction.user.id == money.author.id))

            try:
                money = await client.wait_for("message", timeout=60, check=check)
                await mone.delete()
                money = money.content
                if int(money) < 1:
                    await interaction.user.send(embed=talmoembed("🎲 TossPayments 충전", "**최소 충전금액은 `1,000원` 이어야 합니다.**"))
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 TossPayments 충전", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None
            bonus_m = await interaction.user.send(embed=talmoembed("🎲 TossPayments 충전", "**선택하실 보너스를 선택해주세요.**"),
                                                  components=[Select(placeholder="선택하실 보너스를 입력해주세요",
                                                            options=bonus_selection,custom_id="계좌충전 보너스")])
            
            def check(bonus):
                return (isinstance(bonus.channel, discord.channel.DMChannel) and (
                        interaction.user.id == bonus.author.id) and (bonus.custom_id == "계좌충전 보너스"))
            bonus_amplier = 0
            bonus_rolling = 0
            try:
                bonus = await client.wait_for("select_option", timeout=60, check=check)
                bonus_split = bonus.values[0].split("-")
                bonus_amplier = float(bonus_split[0])
                bonus_rolling = int(bonus_split[1])
                await bonus_m.delete()
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 TossPayments 충전", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None
            if money.isdigit():
                
                access = Button(label="✅ 완료", custom_id="finished", style=ButtonStyle.green)
                bankmsg = await interaction.user.send(embed=discord.Embed(title="토스 자동충전",
                                                                description=f"```입금 링크 : {tossbanks}/{money}\n\n입금자명 : {name}\n입금할 금액 : {money}```",
                                                                color=0x00ff00))
                await interaction.user.send("입금자명 변경 안내 ✅\n\nhttps://i.imgur.com/HJFZrhU.png\n만약 입금자명 변경이 안된다면, 토스 앱에서 바로 송금 하지 말고, 브라우저로 입금 링크를 접속해 익명 송금을 누른 후 입금자명을 변경하시길 바랍니다.\n\n`메시지 쓰기는 입금자명 변경이 아닙니다.`")
                                                                
                sex = await interaction.user.send("송금 후 `완료`를 입력해주세요."
                ,
                components = [
                    [
                    Button(label = "입금 링크", style=ButtonStyle.URL, url=f"{tossbanks}/{money}")]
                ])

                def check(file):
                    return (isinstance(file.channel, discord.channel.DMChannel) and (file.author.id == interaction.user.id) and (file.content == "완료"))

                try:
                    file = await client.wait_for("message", timeout=300, check=check)
                    await sex.delete()
                except asyncio.TimeoutError:
                    try:
                        await sex.delete()
                        await bankmsg.delete()
                        await interaction.user.send(embed=talmoembed("🎲 TossPayments 충전", "```yaml\n시간 초과되었습니다.```"))
                    except:
                        pass
                    return None

                waitmsg = await interaction.user.send(
                    embed=discord.Embed(title="충전 요청 성공 ✅", description=f"```yaml\n잠시만 기다려주세요.```",
                                        color=0x2f3136))
                res = toss.check(name.strip(), int(money))
                await asyncio.sleep(2)
                print(f"{interaction.user.name} 토스 자충 결과는 다음과 같습니다 : {res}")
                if res['msg'] == "입금 미확인":
                    access_embed = discord.Embed(title='토스 자동충전 요청',
                                                description=f'디스코드 닉네임 : <@{interaction.user.id}>({interaction.user})\n입금자명 : {name}\n입금 금액 : {money}\n\n결과 : 입금 미확인.',
                                                color=0xff0000)
                    a_m = await client.get_channel(요청채널).send(embed=access_embed)
                    await waitmsg.delete()
                    await interaction.user.send(embed=discord.Embed(title="충전 실패 ❌", description=f"**다음 사유로 충전이 거부되었습니다.\n사유 : `입금 미확인`**",color=0x2f3136))
                    return None
                if res['msg'] == "USER_IP_TEMPORARILY_BLOCKED 서비스를 일시적으로 이용할 수 없습니다.":
                    access_embed = discord.Embed(title='토스 자동충전 요청',
                                                description=f'디스코드 닉네임 : <@{interaction.user.id}>({interaction.user})\n입금자명 : {name}\n입금 금액 : {money}\n\n결과 : USER_IP_TEMPORARILY_BLOCKED 서비스를 일시적으로 이용할 수 없습니다..',
                                                color=0xff0000)
                    a_m = await client.get_channel(요청채널).send(embed=access_embed)
                    await waitmsg.delete()
                    await interaction.user.send(embed=discord.Embed(title="충전 실패 ❌", description=f"**다음 사유로 충전이 거부되었습니다.\n사유 : `일시적인 서비스 장애가 발생하였습니다.`\n\n관리자에게 문의하세요.**",color=0x2f3136))
                    return None
                elif res['result'] == True:
                    write_bet(user_id,0)
                    write_rolling(user_id,bonus_rolling)
                    add_chung1(user_id,float(money)*bonus_amplier)
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                (user_info[1] + float(money)*bonus_amplier, user_id))
                    con.commit()
                    ktotal += int(money)
                    con.close()
                    nojum = math.floor(float(money)*(bonus_amplier-1))
                    access_embed = discord.Embed(title='토스 자동충전 요청',
                                                description=f'디스코드 닉네임 : <@{interaction.user.id}>({interaction.user})\n입금자명 : {name}\n입금 금액 : {money}\n\n결과 : 성공적으로 충전완료\n{bonus_split} 보너스가 적용되었습니다.',
                                                color=0x00ff00)
                    a_m = await client.get_channel(요청채널).send(embed=access_embed)
                    await waitmsg.delete()
                    
                    log_id = 환전액로그
                    log_ch = client.get_channel(int(log_id))
                    await log_ch.send(f"<@{interaction.user.id}>님이 {int(money)}원을 충전하셨습니다! [보너스 이벤트 {nojum}원 추가지급]")
                    await interaction.user.send(embed=discord.Embed(title="Order Accepted", description=f"충전 자동 승인 되었습니다.\n주문번호: {res['id']}"))
                    await interaction.user.send(embed=discord.Embed(title="충전 성공 ✅", description=f"**성공적으로 `{money}원`이 충전 되었습니다.\n`이벤트로 인하여 {nojum}원이 추가로 지급되었습니다.`**",color=0x2f3136))
                    guild = client.get_guild(int(1103334101043396669))
                    log = ""

                    id = 환전액로그
                    channel = client.get_channel(int(id))
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
                    number = int(money)
                    if number < 0 or number >= 1500000:
                        return
                    elif number < 3000:
                        return
                    elif number < 15000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 1')
                    elif number < 50000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 2')
                    elif number < 150000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 3')
                    elif number < 350000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 4')
                    elif number < 800000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 5')
                    elif number < 1500000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 6')
                    else:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 7')

                    if role is None:
                        return
                    elif role in member.roles:
                        return
                    else:
                        await member.add_roles(role)
                        await client.get_user(user_id).send(f"RICHLAND 잔액 {number}원 누적 충전으로 인해 {role.name} 등급을 부여 받았습니다.")
                    return None

            else:
                await interaction.user.send(embed=talmoembed("🎲 TossPayments 충전", "**올바른 액수를 입력해주세요.**"))


    if using == 1:
        if interaction.user.id == player_id:
            if interaction.custom_id == bomb: 
                grid = ['⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏']
                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님 게임 실패 총`{user_info[1]}`원")
                response = webhook.execute()
                cur.execute("UPDATE users SET money = ? WHERE id == ?;",(user_info[1] - int(amount), interaction.user.id))
                con.commit()
                cur.execute("UPDATE users SET bet_money = ? WHERE id == ?;",(amount, interaction.user.id))
                con.commit()
                embed=discord.Embed(title=f"패배",description=f"```yaml\n{bomb}번 버튼은 폭탄이었습니다 \n💎 : {count}개```",color=0xff0000)
                await interaction.edit_origin(embed=embed,components = [])
                조작해제 = 0
                count = 0 
                using = 0 
                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님 게임 종료")
                response = webhook.execute()
            else:
                if interaction.custom_id in already_used:
                    grid = ['⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏']
                    if count == 1:
                        prize = 1.02
                    elif count == 2:
                        prize = 1.04
                    elif count == 3:
                        prize = 1.06
                    elif count == 4:
                        prize = 1.08
                    elif count == 5:
                        prize = 1.1
                    else:
                        prize = round(count * 0.2, 1)
                    afamount = float(user_info[48]) * prize
                    con = sqlite3.connect("./database/database.db")
                    cur = con.cursor()
                    cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
                    user_info = cur.fetchone()
                    if not (user_info[5] == 3):

                        cur.execute("UPDATE users SET money = ? WHERE id == ?;",(user_info[1]+afamount, interaction.user.id))
                        con.commit()
                        cur.execute("UPDATE users SET bet_money = ? WHERE id == ?;",(0, interaction.user.id))
                        con.commit()
                        con.close()

                        con = sqlite3.connect("./database/database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
                        user_info = cur.fetchone()
                        embed=discord.Embed(title=f"이기셨습니다",description=f"```yaml\nx{prize}배\n💎 : {count}개 \n💣 : {bomb}번 버튼\n{betmoney}원 -> {afamount}원```",color=0x00ff00)
                        con.close()
                        await interaction.edit_origin(embed=embed,components = [])
                        webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님 게임 우승 `{betmoney}`원 -> `{afamount}`원 총`{user_info[1]}`원")
                        response = webhook.execute()
                        
                    조작해제 = 0
                    count = 0 
                    using = 0 
                    prize = 0
                    webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님 게임 종료 ")
                    response = webhook.execute()
                else:
                    #if interaction.user.id in admin_id and 조작해제 == 0:
                    #if not interaction.user.id in admin_id and 조작해제 == 0:
                    if 조작해제 == 0:
                        if count == 1:
                            ra = random.randint(1, 10)
                            if ra == 1:
                                bomb = interaction.custom_id
                                print(f"{interaction.user}님의 게임에서 1조작 발동 / {bomb}터짐처리")
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님의 게임에서 1조작 발동 / {bomb}터짐처리")
                                response = webhook.execute()
                                조작해제 = 0
                                betmoney = 0
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님 게임 실패 총`{user_info[1]}`원")
                                response = webhook.execute()
                            else:
                                print(f"{interaction.user}님의 게임에서 1조작 발동 / 생존처리")
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님의 게임에서 1조작 발동 / 생존처리")
                                response = webhook.execute()
                        if count >= 5:
                            ra = random.randint(1, 4)
                            if ra == 1:
                                bomb = interaction.custom_id
                                print(f"{interaction.user}님의 게임에서 5조작 발동 / {bomb}터짐처리")
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님의 게임에서 5조작 발동 / {bomb}터짐처리")
                                response = webhook.execute()
                                조작해제 = 0
                                betmoney = 0
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님 게임 실패 총`{user_info[1]}`원")
                                response = webhook.execute()
                            else:
                                print(f"{interaction.user}님의 게임에서 5조작 발동 / 생존처리")
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님의 게임에서 5조작 발동 / 생존처리")
                                response = webhook.execute()
                        if count >= 10:
                            ra = random.randint(1, 5)
                            if ra == 1:
                                bomb = interaction.custom_id
                                print(f"{interaction.user}님의 게임에서 10조작 발동 / {bomb}터짐처리")
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님의 게임에서 10조작 발동 / {bomb}터짐처리")
                                response = webhook.execute()
                                조작해제 = 0
                                betmoney = 0
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님 게임 실패 총`{user_info[1]}`원")
                                response = webhook.execute()
                            else:
                                print(f"{interaction.user}님의 게임에서 10조작 발동 / 생존처리")
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님의 게임에서 10조작 발동 / 생존처리")
                                response = webhook.execute()
                        if count >= 15:
                            ra = random.randint(1, 4)
                            if ra == 1:
                                bomb = interaction.custom_id
                                print(f"{interaction.user}님의 게임에서 15조작 발동 / {bomb}터짐처리")
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님의 게임에서 15조작 발동 / {bomb}터짐처리")
                                response = webhook.execute()
                                조작해제 = 0
                                betmoney = 0
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님 게임 실패 총`{user_info[1]}`원")
                                response = webhook.execute()
                            else:
                                print(f"{interaction.user}님의 게임에서 15조작 발동 / 생존처리")
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님의 게임에서 15조작 발동 / 생존처리")
                                response = webhook.execute()
                        if count >= 20:
                            ra = random.randint(1, 3)
                            if ra == 1:
                                bomb = interaction.custom_id
                                print(f"{interaction.user}님의 게임에서 20조작 발동 / {bomb}터짐처리")
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님의 게임에서 20조작 발동 / {bomb}터짐처리")
                                response = webhook.execute()
                                조작해제 = 0
                                betmoney = 0
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님 게임 실패 총`{user_info[1]}`원")
                                response = webhook.execute()
                            else:
                                print(f"{interaction.user}님의 게임에서 20조작 발동 / 생존처리")
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님의 게임에서 20조작 발동 / 생존처리")
                                response = webhook.execute()
                        if count >= 22:
                            ra = random.randint(1, 2)
                            if ra == 1:
                                bomb = interaction.custom_id
                                print(f"{interaction.user}님의 게임에서 22조작 발동 / {bomb}터짐처리")
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님의 게임에서 22조작 발동 / {bomb}터짐처리")
                                response = webhook.execute()
                                조작해제 = 0
                                betmoney = 0
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님 게임 실패 총`{user_info[1]}`원")
                                response = webhook.execute()
                            else:
                                print(f"{interaction.user}님의 게임에서 22조작 발동 / 생존처리")
                                webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님의 게임에서 22조작 발동 / 생존처리")
                                response = webhook.execute()

                        if interaction.custom_id == bomb: 
                            grid = ['⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏']
                            webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님 게임 실패 총`{user_info[1]}`원")
                            response = webhook.execute()
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",(user_info[1] - int(amount), interaction.user.id))
                            con.commit()
                            cur.execute("UPDATE users SET bet_money = ? WHERE id == ?;",(amount, interaction.user.id))
                            con.commit()
                            embed=discord.Embed(title=f"패배",description=f"```yaml\n{bomb}번 버튼은 폭탄이었습니다 \n💎 : {count}개```",color=0xff0000)
                            await interaction.edit_origin(embed=embed,components = [])
                            조작해제 = 0
                            count = 0 
                            using = 0 
                            betmoney = 0
                            webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님 게임 종료")
                            response = webhook.execute()
                        else:
                            pass
                    else:
                        pass
                    count += 1 
                    already_used.append(interaction.custom_id)
                    csid = int(interaction.custom_id)-1
                    grid[csid] = "💎"
                    if count== 24:
                        grid = ['⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏','⛏'] 
                        #await interaction.edit_origin(f"**퍼펙트!**\nx50.0\n💎 : {count}개 \n💣 : {bomb}번 버튼",components = [])
                        prize = 50
                        afamount = (float(user_info[48]) * prize)
                        con = sqlite3.connect("./database/database.db")
                        cur = con.cursor()
                        cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
                        user_info = cur.fetchone()
                        if not (user_info[3] == 3):
                            cur.execute("UPDATE users SET money = ? WHERE id == ?;",(user_info[1]+afamount, interaction.user.id))
                            con.commit()
                            cur.execute("UPDATE users SET bet_money = ? WHERE id == ?;",(0, interaction.user.id))
                            con.commit()
                            con.close()

                            con = sqlite3.connect("./database/database.db")
                            cur = con.cursor()
                            cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
                            user_info = cur.fetchone()
                            embed=discord.Embed(title=f"퍼펙트!",description=f"```yaml\nx50배\n💎 : {count}개 \n💣 : {bomb}번 버튼\n{betmoney}원 -> {afamount}원```",color=0x00ff00)
                            con.close()

                            await interaction.edit_origin(embed=embed,components = [])
                            webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님 게임 퍼펙트 `{betmoney}`원 -> `{afamount}`원 총`{user_info[1]}`원")
                            response = webhook.execute()
                        조작해제 = 0
                        count = 0
                        using = 0
                        prize = 0
                        betmoney = 0
                        webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님 게임 종료")
                        response = webhook.execute()
                if count == 1:
                    배당 = 1.02
                elif count == 2:
                    배당 = 1.04
                elif count == 3:
                    배당 = 1.06
                elif count == 4:
                    배당 = 1.08
                elif count == 5:
                    배당 = 1.1
                else:
                    배당 = round(count * 0.2, 1)
                embed=discord.Embed(title=f"Alpha Land",description=f"```yaml\nx{배당}\n배팅금 : {betmoney}\n💎 : {count}\n\n다이아몬드 버튼을 눌러 배팅을 멈추십시오.```",color=0x34c6eb)
                await interaction.edit_origin(
                    embed=embed,
                    components = [
                    [
                        Button(label = grid[0], custom_id = "1"),
                        Button(label = grid[1], custom_id = "2"),
                        Button(label = grid[2], custom_id = "3"),
                        Button(label = grid[3], custom_id = "4"),
                        Button(label = grid[4], custom_id = "5"),
                    ],[
                        Button(label = grid[5], custom_id = "6"),
                        Button(label = grid[6], custom_id = "7"),
                        Button(label = grid[7], custom_id = "8"),
                        Button(label = grid[8], custom_id = "9"),
                        Button(label = grid[9], custom_id = "10"),
                    ],[
                        Button(label = grid[10], custom_id = "11"),
                        Button(label = grid[11], custom_id = "12"),
                        Button(label = grid[12], custom_id = "13"),
                        Button(label = grid[13], custom_id = "14"),
                        Button(label = grid[14], custom_id = "15"),
                    ],[
                        Button(label = grid[15], custom_id = "16"),
                        Button(label = grid[16], custom_id = "17"),
                        Button(label = grid[17], custom_id = "18"),
                        Button(label = grid[18], custom_id = "19"),
                        Button(label = grid[19], custom_id = "20"),
                    ],[
                        Button(label = grid[20], custom_id = "21"),
                        Button(label = grid[21], custom_id = "22"),
                        Button(label = grid[22], custom_id = "23"),
                        Button(label = grid[23], custom_id = "24"),
                        Button(label = grid[24], custom_id = "25"),
                    ]
                ]
                )
        elif not interaction.user.id == player_id and interaction.user.id in admin_id:
            조작해제 = 1
            print(f"{interaction.user}님이 {player_name}님의 게임에서 조작을 풀었습니다")
            webhook = DiscordWebhook(url=게임로그웹훅, content=f"{interaction.user}님이 {player_name}님의 게임에서 조작을 풀었습니다")
            response = webhook.execute()

    
    if interaction.custom_id == "ticket": #기본문의 버튼이 눌렸다면

        i = 0
        for channel in interaction.guild.channels:
            if str(channel.name) == f'{common}' + (str(interaction.user).lower()).replace("#", ""):
                print(channel.name)
                i = 1
                break

        if i == 0:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            channel = await interaction.guild.create_text_channel(f'{common}' + str(interaction.user).lower(), overwrites=overwrites, category=interaction.guild.get_channel(1115243462313398272))
            await interaction.respond(embed=discord.Embed(title="**RICH Land**", description=f" :ok_hand:  <#{str(channel.id)}>로 이동해주세요.", color=0x010101), components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])
            await channel.send(embed=discord.Embed(title="**RICH Land**", description=f"<@{str(interaction.user.id)}>\n\n**안녕하세요! 일반 문의 티켓을 여셨어요.\n장난 개설이거나 모르고 눌렀다면 아래 버튼을 눌러 닫아주세요.\n관리자에게 알림을 보냈으니 멘션할 필요는 없으실 거에요!\n 감사합니다. 용건을 말씀해주세요.**", color=0x010101), components=[[Button(label="💥티켓닫기", custom_id="close", style=ButtonStyle.red)]])
            await channel.send(f"<@{interaction.user.id}>")
            for i in range(0,int(len(admin_id))):
                user = await client.fetch_user(admin_id[i])
                await user.send(f'<@{str(interaction.user.id)}> 님이 일반 문의티켓을 열었습니다', components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])
        else:
            await interaction.respond(embed=discord.Embed(title="**RICH Land**", description=f"❌ <#{str(channel.id)}>\n이미 티켓 채널이 존재합니다.", color=0x010101))

    if interaction.custom_id == "charge":

        i = 0
        for channel in interaction.guild.channels:
            if str(channel.name) == f'{charge}' + (str(interaction.user).lower()).replace("#", ""):
                print(channel.name)
                i = 1
                break

        if i == 0:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            channel = await interaction.guild.create_text_channel(f'{charge}' + str(interaction.user).lower(), overwrites=overwrites, category=interaction.guild.get_channel(1115243462313398272))
            await interaction.respond(embed=discord.Embed(title="**RICH Land**", description=f" :ok_hand:  <#{str(channel.id)}>로 이동해주세요.", color=0x010101), components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])
            await channel.send(embed=discord.Embed(title="**RICH Land**", description=f"<@{str(interaction.user.id)}>\n\n**안녕하세요! 충전문의 티켓을 여셨어요.\n장난 개설이거나 잘못 누르셨다면 아래 버튼을 눌러 닫아주세요.\n문화상품권 충전이라면, 여기에 핀 번호를 남겨주세요! [컬쳐랜드 번호]\n계좌 충전이라면, 충전 채널을 확인해주세요!\n감사합니다.**", color=0x010101), components=[[Button(label="💥티켓닫기", custom_id="close", style=ButtonStyle.red)]])
            await channel.send(f"<@{interaction.user.id}>")
            for i in range(0,int(len(admin_id))):
                user = await client.fetch_user(admin_id[i])
                await user.send(f'<@{str(interaction.user.id)}> 님이 충전 문의티켓을 열었습니다', components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])

        else:
            await interaction.respond(embed=discord.Embed(title="**RICH Land**", description=f"❌ <#{str(channel.id)}>\n이미 티켓 채널이 존재합니다.", color=0x010101))

    if interaction.component.custom_id == "p":

        i = 0
        for channel in interaction.guild.channels:
            if str(channel.name) == f'{qs}' + (str(interaction.user).lower()).replace("#", ""):
                print(channel.name)
                i = 1
                break

        if i == 0:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            channel = await interaction.guild.create_text_channel(f'{qs}' + str(interaction.user).lower(), overwrites=overwrites, category=interaction.guild.get_channel(1115243462313398272))
            await interaction.respond(embed=discord.Embed(title="**RICH Land**", description=f" :ok_hand:  <#{str(channel.id)}>로 이동해주세요.", color=0x010101), components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])
            await channel.send(embed=discord.Embed(title="**RICH Land**", description=f"<@{str(interaction.user.id)}>\n\n**안녕하세요! 환전문의를 여셨어요.\n아래 양식에 따라 작성해 주시면, 차근차근 처리해 드려요!\n예금주, 계좌번호, 환전할 금액, 전화번호를 작성해주세요!\n만약 3자 입금, 및 대포 계좌[미인증 시]였다면 몰수에요!\n\n환전 요청을 관리자에게 알림을 전송했으니, 재촉은 안돼요! 자칫하다간 몰수 될 수 있어요!\n감사합니다! 환전 후 후기는 꼭!**", color=0x010101), components=[[Button(label="💥티켓닫기", custom_id="close", style=ButtonStyle.red)]])
            await channel.send(f"<@{interaction.user.id}>")
            for i in range(0,int(len(admin_id))):
                user = await client.fetch_user(admin_id[i])
                await user.send(f'<@{str(interaction.user.id)}> 님이 환전문의 티켓 열었습니다', components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])

        else:
            await interaction.respond(embed=discord.Embed(title="**RICH Land**", description=f"❌ <#{str(channel.id)}>\n이미 티켓 채널이 존재합니다.", color=0x010101))

    if interaction.component.custom_id == "bankwithdraw":

        i = 0
        for channel in interaction.guild.channels:
            if str(channel.name) == f'{qs}' + (str(interaction.user).lower()).replace("#", ""):
                print(channel.name)
                i = 1
                break

        if i == 0:
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
            user_info = cur.fetchone()

            try:
                bankbb = await interaction.user.send(embed=talmoembed("🎲 계좌 환전", f"**출금을 진행할 은행을 선택해주세요.**"),
                                                    components=[Select(placeholder="은행을 선택해주세요",
                                                                options=bank_selection,custom_id="은행 선택")])
                await interaction.respond(embed=talmoembed("🎲 계좌 환전", "**DM을 확인해주세요.**"))
            except:
                
                await interaction.respond(embed=talmoembed("🎲 계좌 환전", "**DM을 허용해주세요.**"))
                                                        
            
            def check(bankdd):
                return (interaction.user.id == bankdd.author.id) and (bankdd.custom_id == "은행 선택")
            try:
                bank = await client.wait_for("select_option", timeout=60, check=check)
                bankname = bank.values
                await bankbb.delete()
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 계좌 환전", f"**시간 초과되었습니다.**"))
                except:
                    pass
                return None
            
            nam = await interaction.user.send(embed=talmoembed("🎲 계좌 환전", "**환전 받으실 계좌번호를 입력해 주세요.**"))
                

            def check(name):
                return (isinstance(name.channel, discord.channel.DMChannel) and (interaction.user.id == name.author.id))

            try:
                name = await client.wait_for("message", timeout=60, check=check)
                await nam.delete()
                name = name.content

                
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 계좌 환전", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None

            mone = await interaction.user.send(embed=talmoembed("🎲 계좌 환전", "**환전할 금액을 입력해주세요.**"))

            def check(money):
                return (isinstance(money.channel, discord.channel.DMChannel) and (
                        interaction.user.id == money.author.id))

            try:
                money = await client.wait_for("message", timeout=60, check=check)
                await mone.delete()
                money = money.content
                
                if int(money) < 5000:
                    await interaction.user.send(embed=talmoembed("🎲 계좌 환전", "**최소 환전금액은 `5,000원` 이어야 합니다.**"))
                    return None
                if int(money) % 1000 != 0:
                    await interaction.user.send(embed=talmoembed("🎲 계좌 환전", "**환전 단위은 `1,000원` 이어야 합니다.**"))
                    return None
                if int(money) > user_info[1]:
                    await interaction.user.send(embed=talmoembed("🎲 계좌 환전", "**보유 잔액이 부족합니다.**"))
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 계좌 환전", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None
            
            phon = await interaction.user.send(embed=talmoembed("🎲 전화번호 인증", "**전화번호 인증이 왜 필요한가요?**\n3자사기 방지를 위해 전화번호 인증이 필요합니다.\n수집된 정보는 사기 관련 이외의 용도로는 사용되지 않습니다.\n**전화번호를 입력해주세요.**\n숫자로만 입력해주세요."))

            def check(phone):
                return (isinstance(phone.channel, discord.channel.DMChannel) and (
                        interaction.user.id == phone.author.id))

            try:
                phone = await client.wait_for("message", timeout=60, check=check)
                await phon.delete()
                phone = phone.content
                if not phone.startswith("010") or not len(phone) == 11:
                    await interaction.user.send(embed=talmoembed("🎲 전화번호 인증", "**제대로 된 전화번호를 입력해주세요.**"))
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 전화번호 인증", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None
            
            verifycode = random.randint(100000,999999)
            verifymsg = f"RICHLAND 환전 요청 인증번호입니다. {interaction.user}님이 아니라면 무시해주세요!\n\n기다려 주셔서 감사해요! {verifycode}가 인증코드랍니다.\n디스코드에 돌아가서 인증번호를 입력해주세요!\n\n위 인증번호를 타인에게 알려주지 마세요!"

            jphone = smssend.JmunjaPhone(uid, upw)
            presult = jphone.send(subject, verifymsg, phone)

            jweb = smssend.JmunjaWeb(uid, upw)
            wresult = jweb.send(subject, verifymsg, phone, callback)

            vcod = await interaction.user.send(embed=talmoembed("🎲 전화번호 인증", "**인증코드를 전송했습니다.\n전송된 6자리 인증코드를 `5분 내`에 입력해주세요.\n\n인증코드가 오지 않았다면 `스팸함`을 확인해주세요.**"))

            def check(vcode):
                return (isinstance(vcode.channel, discord.channel.DMChannel) and (
                        interaction.user.id == vcode.author.id))

            try:
                vcode = await client.wait_for("message", timeout=300, check=check)
                await vcod.delete()
                vcode = vcode.content
                if int(vcode) != int(verifycode):
                    await interaction.user.send(embed=talmoembed("🎲 전화번호 인증", "**인증코드가 올바르지 않습니다.**"))
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 전화번호 인증", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=False, send_messages=False),
            }
            channel = await interaction.guild.create_text_channel(f'{qs}' + str(interaction.user).lower(), overwrites=overwrites, category=interaction.guild.get_channel(1115616337524437083))
            await interaction.user.send(embed=discord.Embed(title="**RICH Land**", description=f":white_check_mark: 요청이 성공적으로 생성되었습니다.", color=0x010101), components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])
            await channel.send(embed=discord.Embed(title="**RICH Land**", description=f"<@{str(interaction.user.id)}>\n\n환전 될 계좌\n```{bankname} {name}```\n\n환전 금액 {money}원\n\n휴대 전화 번호 : {phone}", color=0x010101), components=[[Button(label="💥환전요청 닫기", custom_id="close", style=ButtonStyle.red)]])
            await channel.send(f"<@{interaction.user.id}>")
            for i in range(0,int(len(admin_id))):
                user = await client.fetch_user(admin_id[i])
                await user.send(f'<@{str(interaction.user.id)}> 님이 환전요청했습니다', components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])

        else:
            await interaction.respond(embed=discord.Embed(title="**RICH Land**", description=f"**❌ 이미 환전 신청이 처리되고 있습니다.**", color=0x010101))

    if interaction.component.custom_id == "culturewithdraw":

        i = 0
        for channel in interaction.guild.channels:
            if str(channel.name) == f'{qs}' + (str(interaction.user).lower()).replace("#", ""):
                print(channel.name)
                i = 1
                break

        if i == 0:
            con = sqlite3.connect("./database/database.db")
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE id == ?;", (interaction.user.id,))
            user_info = cur.fetchone()
            

            mone = await interaction.user.send(embed=talmoembed("🎲 문화상품권 환전", "**환전할 금액을 입력해주세요.**"))

            def check(money):
                return (isinstance(money.channel, discord.channel.DMChannel) and (
                        interaction.user.id == money.author.id))

            try:
                money = await client.wait_for("message", timeout=60, check=check)
                await mone.delete()
                money = money.content
                if int(money) < 5000:
                    await interaction.user.send(embed=talmoembed("🎲 문화상품권 환전", "**최소 환전금액은 `5,000원` 이어야 합니다.**"))
                    return None
                if int(money) % 1000 != 0:
                    await interaction.user.send(embed=talmoembed("🎲 문화상품권 환전", "**환전 단위은 `1,000원` 이어야 합니다.**"))
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 문화상품권 환전", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None
            
            phon = await interaction.user.send(embed=talmoembed("🎲 전화번호 인증", "**전화번호 인증이 왜 필요한가요?**\n3자사기 방지를 위해 전화번호 인증이 필요합니다.\n수집된 정보는 사기 관련 이외의 용도로는 사용되지 않습니다.\n**전화번호를 입력해주세요.**\n숫자로만 입력해주세요."))

            def check(phone):
                return (isinstance(phone.channel, discord.channel.DMChannel) and (
                        interaction.user.id == phone.author.id))

            try:
                phone = await client.wait_for("message", timeout=60, check=check)
                await phon.delete()
                phone = phone.content
                if not phone.startswith("010") or not len(phone) == 11:
                    await interaction.user.send(embed=talmoembed("🎲 전화번호 인증", "**제대로 된 전화번호를 입력해주세요.**"))
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 전화번호 인증", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None
            
            verifycode = random.randint(100000,999999)
            verifymsg = f"RICHLAND 환전 요청 인증번호입니다. {interaction.user}님이 아니라면 무시해주세요!\n\n기다려 주셔서 감사해요! {verifycode}가 인증코드랍니다.\n디스코드에 돌아가서 인증번호를 입력해주세요!\n\n위 인증번호를 타인에게 알려주지 마세요!"

            jphone = smssend.JmunjaPhone(uid, upw)
            presult = jphone.send(subject, verifymsg, phone)

            jweb = smssend.JmunjaWeb(uid, upw)
            wresult = jweb.send(subject, verifymsg, phone, callback)

            vcod = await interaction.user.send(embed=talmoembed("🎲 전화번호 인증", "**인증코드를 전송했습니다.\n전송된 6자리 인증코드를 `5분 내`에 입력해주세요.\n\n인증코드가 오지 않았다면 `스팸함`을 확인해주세요.**"))

            def check(vcode):
                return (isinstance(vcode.channel, discord.channel.DMChannel) and (
                        interaction.user.id == vcode.author.id))

            try:
                vcode = await client.wait_for("message", timeout=300, check=check)
                await vcod.delete()
                vcode = vcode.content
                if int(vcode) != int(verifycode):
                    await interaction.user.send(embed=talmoembed("🎲 전화번호 인증", "**인증코드가 올바르지 않습니다.**"))
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 전화번호 인증", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None

            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            channel = await interaction.guild.create_text_channel(f'{qs}' + str(interaction.user).lower(), overwrites=overwrites, category=interaction.guild.get_channel(1115616337524437083))
            await interaction.user.send(embed=discord.Embed(title="**RICH Land**", description=f" :ok_hand:  <#{str(channel.id)}> 에 성공적으로 환전 요청이 생성되었습니다.\n예상 소요시간 : 약 `48시간 이내`", color=0x010101), components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])
            await channel.send(embed=discord.Embed(title="**RICH Land**", description=f"<@{str(interaction.user.id)}>\n\```문화상품권 환전```\n\n환전 금액 {money}원\n\n휴대 전화 번호 : {phone}", color=0x010101), components=[[Button(label="💥환전요청 닫기", custom_id="close", style=ButtonStyle.red)]])
            await channel.send(f"<@{interaction.user.id}>")
            for i in range(0,int(len(admin_id))):
                user = await client.fetch_user(admin_id[i])
                await user.send(f'<@{str(interaction.user.id)}> 님이 문상 환전요청했습니다', components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])

        else:
            await interaction.respond(embed=discord.Embed(title="**RICH Land**", description=f"❌ <#{str(channel.id)}>\n이미 티켓 채널이 존재합니다.", color=0x010101))

    if interaction.component.custom_id == "coinwithdraw":
        await interaction.respond(embed=discord.Embed(title="**RICH Land**", description=f"❌ 코인 환전은 일반문의를 열어 관리자 문의하세요.", color=0x010101))

    if interaction.component.custom_id == "q":

        i = 0
        for channel in interaction.guild.channels:
            if str(channel.name) == f'{purchase}' + (str(interaction.user).lower()).replace("#", ""):
                print(channel.name)
                i = 1
                break

        if i == 0:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            channel = await interaction.guild.create_text_channel(f'{purchase}' + str(interaction.user).lower(), overwrites=overwrites, category=interaction.guild.get_channel(1115243462313398272))
            await interaction.respond(embed=discord.Embed(title="**RICH Land**", description=f" :ok_hand:  <#{str(channel.id)}>로 이동해주세요.", color=0x010101), components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])
            await channel.send(embed=discord.Embed(title="**RICH Land**", description=f"<@{str(interaction.user.id)}>\n\n**안녕하세요! 버그문의 티켓을 여셨어요.\n장난 개설이거나 잘못 눌렀으면 아래 버튼으로 닫아주세요.\n버그와 간단한 스크린샷을 첨부해 주시면, 간단한 소소한 포상금을 드려요!\n감사합니다.**", color=0x010101), components=[[Button(label="💥티켓닫기", custom_id="close", style=ButtonStyle.red)]])
            await channel.send(f"<@{interaction.user.id}>")
            for i in range(0,int(len(admin_id))):
                user = await client.fetch_user(admin_id[i])
                await user.send(f'<@{str(interaction.user.id)}> 님이 버그 문의티켓을 열었습니다', components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])

        else:
            await interaction.respond(embed=discord.Embed(title="**RICH Land**", description=f"❌ <#{str(channel.id)}>\n이미 티켓 채널이 존재합니다.", color=0x010101))
    
    if interaction.component.custom_id == "zz11z":
        try:
            nam = await interaction.user.send(embed=talmoembed("🎲 배팅방 참가", "**초대 받은 개인배팅방 채널의 비밀번호를 입력해주세요.**"))
            await interaction.respond(embed=talmoembed("🎲 배팅방 참가", "**DM을 확인해주세요.**"))
        except:
            await interaction.respond(embed=talmoembed("🎲 배팅방 참가", "**DM을 허용해주세요.**"))
        
        def check(m):
                return (isinstance(m.channel, discord.channel.DMChannel) and (interaction.user.id == m.author.id))
        msg = await client.wait_for('message', check=check)
        password = msg.content
        conn = sqlite3.connect('passwords.db')
        co = conn.cursor()
        co.execute("SELECT * FROM passwords WHERE password=?", (password,))
        result = co.fetchone()
        if result:
            channel_id = result[0]
            private_channel = client.get_channel(channel_id)
            await nam.delete()
            await private_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            await interaction.user.send(embed=talmoembed("🎲 배팅방 참가", f"**{private_channel.name} 배팅채널에 참가하였습니다.**"))
        else:
            await interaction.user.send(embed=talmoembed("🎲 배팅방 참가", "**비밀번호가 일치하지 않습니다.**"))


    if interaction.component.custom_id == "zzz":

        i = 0
        for channel in interaction.guild.channels:
            if str(channel.name) == f'{bozi}' + (str(interaction.user).lower()).replace("#", ""):
                print(channel.name)
                i = 1
                break

        if i == 0:
            conn = sqlite3.connect('passwords.db')
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS passwords
                        (channel_id INTEGER, password TEXT)''')
            password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            }
            channel = await interaction.guild.create_text_channel(f'{bozi}' + str(interaction.user).lower(), overwrites=overwrites, category=interaction.guild.get_channel(1115616337704787971))
            await interaction.respond(embed=discord.Embed(title="**RICH Land**", description=f" :ok_hand:  <#{str(channel.id)}>로 이동해주세요.", color=0x010101), components = [
                [
                Button(label = "💌 TICKET", style=ButtonStyle.URL, url=f"https://discord.com/channels/{interaction.guild.id}/{channel.id}")]
            ])
            
            c.execute("INSERT INTO passwords VALUES (?, ?)", (channel.id, password))
            conn.commit()
            await channel.send(embed=discord.Embed(title="**RICH Land**", description=f"<@{str(interaction.user.id)}>\n\n**안녕하세요! 여기는 개인배팅 채널입니다!\n사람을 초대하고 싶으면 관리자를 호출하세요 :)\n이 채널은 1일 간 외부 활동이 없으면 자동삭제 됩니다.\n\n초대 비밀번호 : ||{password}||**", color=0x010101), components=[[Button(label="💥티켓닫기", custom_id="close", style=ButtonStyle.red)]])
            await channel.send(f"<@{interaction.user.id}>")

        else:
            await interaction.respond(embed=discord.Embed(title="**RICH Land**", description=f"❌ <#{str(channel.id)}>이미 개인배팅 채널이 존재합니다.", color=0x010101))

    if interaction.component.custom_id == "close":
        embed = discord.Embed(title="**RICH Land**", description=f"**```아래 버튼을 눌러 티켓을 닫아주세요.```**", color=0x2f3136)
        await interaction.respond(
                embed=embed,
                components = [
                    ActionRow(
                        Button(style=ButtonStyle.gray,label="❌ 취소",custom_id="cancle"),
                        Button(style=ButtonStyle.red,label="✅ 닫기",custom_id="close1"),
                    )
                ]
            )

    if interaction.component.custom_id == "cancle":
        await interaction.message.delete()
        await interaction.respond(content="> 티켓 닫기가 취소되었습니다.")
        a3 = discord.Embed(title="**RICH Land**",
                           description=f"```diff\n- 티켓 닫기가 취소되었습니다```  <@{interaction.user.id}>님이 티켓닫기를 취소하셨습니다. ",
                           color=0x2f3136)
        cancle_message = await interaction.channel.send(embed=a3)
        await asyncio.sleep(3)
        await cancle_message.delete()
    if interaction.component.custom_id == "close1":
        await interaction.respond(content="> 10초 후 상담 종료됩니다.")
        a2 = discord.Embed(title="**RICH Land**",
                           description=f"```💥 10초후에 티켓이 삭제됩니다.```  <@{interaction.user.id}>님이 티켓을 닫았습니다. ",
                           color=0x2f3136)
        await interaction.channel.send(embed=a2)
        await asyncio.sleep(10)
        await interaction.channel.delete()
        return
    if interaction.component.custom_id == "coin":
        embed = discord.Embed(title="**RICH Land**", description=f"**```코인 종류를 선택해주세요.```**", color=0x34c6eb)
        await interaction.respond(
                embed=embed,
                components = [
                    ActionRow(
                        Button(style=ButtonStyle.red,label="Bitcoin",custom_id="btc"),
                        Button(style=ButtonStyle.blue,label="Litecoin",custom_id="ltc"),
                        Button(style=ButtonStyle.blue,label="Ethereum",custom_id="eth"),
                    )
                ]
            )
    if interaction.component.custom_id == "sex":
        embed = discord.Embed(title="**계좌를 사용한 잔액 충전/입금**", description=f"**```계좌 충전 종류를 선택해주세요.```**", color=0x34c6eb)
        await interaction.respond(
                embed=embed,
                components = [
                    ActionRow(
                        Button(style=ButtonStyle.red,label="계좌 이체",custom_id="계좌충전"),
                        Button(style=ButtonStyle.blue,label="토스",custom_id="toss"),
                    )
                ]
            )
    
    if interaction.component.custom_id == "btc":
        user_id = interaction.user.id
        
        user = interaction.user.id
        name = interaction.user.name
        member = interaction.user

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                interaction.user.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            try:
                nam = await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**비트코인 송금은 3자 사기 및 3자 송금 확인이 어렵습니다.\n단, 본인은 양심에 따라 이용약관을 지켰음을 맹세합니다.\n`네/아니오`**"))
                await interaction.respond(embed=talmoembed("🎲 코인 충전", "**DM을 확인해주세요.**"))
            except:
                await interaction.respond(embed=talmoembed("🎲 코인 충전", "**DM을 허용해주세요.**"))

            def check(name):
                return (isinstance(name.channel, discord.channel.DMChannel) and (interaction.user.id == name.author.id))

            try:
                name = await client.wait_for("message", timeout=60, check=check)
                await nam.delete()
                name = name.content
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**시간 초과되었습니다.**"))
                except:
                    pass
                return None

            mone = await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**충전할 비트코인 액수를 입력해주세요.\n`달러나 원 단위가 아닌, 비트코인 액수를 입력해주세요.`**"))

            def check(money):
                return (isinstance(money.channel, discord.channel.DMChannel) and (
                        interaction.user.id == money.author.id))

            try:
                money = await client.wait_for("message", timeout=60, check=check)
                await mone.delete()
                
                livecoin_key = "72d66bed-eb47-4b26-bebb-0b8b1ce28780"#livecoinwatch.com 에서 무료 발급되긴 하는데 혹시라도 ratelimit 제한되면 니가 발급받고 바꾸셈
                btc_data_for = {"currency":"KRW","code":"BTC","meta":True}#코인 바꿀거면 BTC 를 다른거로
                header_dict = {'content-type':'application/json','x-api-key':livecoin_key}#json 선언 및 api key 전달

                get_btc_price = requests.post("https://api.livecoinwatch.com/coins/single",headers=header_dict,data=json.dumps(btc_data_for)).json()#해당 url 에 header , data 와 함께 post 후 결과값을 json 화

                btc_rate = get_btc_price['rate']

                money = money.content
                money = btc_rate*float(money)
                if int(money) < 1000:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**최소 충전 BTC 충전금액은 `한국 환율 1,000원` 이어야 합니다.**"))
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**시간 초과되었습니다.**"))
                except:
                    pass
                return None
            bonus_m = await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**선택하실 보너스를 선택해주세요.**"),
                                                  components=[Select(placeholder="선택하실 보너스를 입력해주세요",
                                                            options=bonus_selection,custom_id="계좌충전 보너스")])
            
            def check(bonus):
                return (isinstance(bonus.channel, discord.channel.DMChannel) and (
                        interaction.user.id == bonus.author.id) and (bonus.custom_id == "계좌충전 보너스"))
            bonus_amplier = 0
            bonus_rolling = 0
            try:
                bonus = await client.wait_for("select_option", timeout=60, check=check)
                bonus_split = bonus.values[0].split("-")
                bonus_amplier = float(bonus_split[0])
                bonus_rolling = int(bonus_split[1])
                await bonus_m.delete()
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None
            await interaction.user.send(embed=discord.Embed(title="BTC 충전",
                                                            description=f"**입금 계좌 : `{btcwallet}`**\n─────────────\n비트코인 약관 동의 : `{name}`\n한국환율로 입금 금액 : `{money}`원",
                                                            color=0x2f3136))
            screenshot = await interaction.user.send(
                embed=discord.Embed(description=f"송금 후 스크린샷을 5분 내에 보내주세요.", color=0x2f3136))

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
                            embed=discord.Embed(title="코인 충전 실패", description="올바른 사진 형식이 아닙니다.",
                                                color=0x2f3136))
                    except:
                        pass
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**시간 초과되었습니다.**"))
                except:
                    pass
                return None

            access_embed = discord.Embed(title='코인 충전 요청',
                                        description=f'디스코드 닉네임 : <@{interaction.user.id}>({interaction.user})\n이용약관 동의 : {name}\n비트코인 환율 한국돈으로 : {money}',
                                        color=0x2f3136)
            try:
                access_embed.set_image(url=sct)
            except:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**올바른 사진 형식이 아닙니다..**"))
                except:
                    pass
                return None
            await interaction.user.send(
                embed=discord.Embed(title="충전 요청 성공 ✅", description=f"관리자의 승인을 기다려주세요.",
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
                if interaction.custom_id == '승인':
                    await a_m.delete()
                    write_bet(user_id,0)
                    write_rolling(user_id,bonus_rolling)
                    add_chung1(user_id,float(money)*bonus_amplier)
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                (user_info[1] + float(money)*bonus_amplier, user_id))
                    con.commit()
                    ktotal += int(money)
                    con.close()
                    nojum = math.floor(float(money)*(bonus_amplier-1))
                    await client.get_user(user_id).send(embed=discord.Embed(title="코인 충전 성공",
                                                                            description=f"{money}원이 충전되었습니다.\n\n**`이벤트로 인하여 {nojum}원이 추가로 지급되었습니다.`**",
                                                                            color=0x2f3136))
                    await client.get_channel(요청채널).send(
                        embed=discord.Embed(title="코인 충전 성공", description=f"{interaction.user} \n\n<@{user_id}>님께 충전되었습니다. {money}원\n\n보너스 이벤트 {nojum}원\n선택 보너스 : {bonus_split[2]}",
                                            color=0x2f3136))
                    await client.get_channel(요청채널).send(f"{sct} <@{user_id}> 코인 충전 스크린")
                    log_id = 환전액로그
                    log_ch = client.get_channel(int(log_id))
                    await log_ch.send(f"<@{user_id}>님이 {int(money)}원을 충전하셨습니다! [보너스 이벤트 {nojum}원 추가지급]")
                    await asyncio.sleep(5)
                    guild = client.get_guild(int(1103334101043396669))
                    log = ""

                    id = 환전액로그
                    channel = client.get_channel(int(id))
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
                    number = int(money)
                    if number < 0 or number >= 1500000:
                        return
                    elif number < 3000:
                        return
                    elif number < 15000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 1')
                    elif number < 50000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 2')
                    elif number < 150000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 3')
                    elif number < 350000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 4')
                    elif number < 800000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 5')
                    elif number < 1500000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 6')
                    else:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 7')

                    if role is None:
                        return
                    elif role in member.roles:
                        return
                    else:
                        await member.add_roles(role)
                        await client.get_user(user_id).send(f"RICHLAND 잔액 {number}원 누적 충전으로 인해 {role.name} 등급을 부여 받았습니다.")
                if interaction.custom_id == '거부':
                    await client.get_channel(요청채널).send(f"{sct} <@{user_id}> 충전 실패 스크린\n돈은 {money}이었어용.")
                    await a_m.delete()
                    await client.get_user(user_id).send(
                        embed=discord.Embed(title="코인 충전 실패", description=f"{interaction.user} 관리자님께서 충전을 거부하셨습니다.",
                                            color=0x2f3136))
                    await client.get_channel(요청채널).send(
                        embed=discord.Embed(title="코인 충전 실패", description=f"{interaction.user}\n\n<@{user_id}>님의 코인 충전이 거부되었습니다.",
                                            color=0x2f3136))

    if interaction.component.custom_id == "ltc":
        user_id = interaction.user.id
        
        user = interaction.user.id
        name = interaction.user.name
        member = interaction.user

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                interaction.user.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            try:
                nam = await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**라이트코인 송금은 3자 사기 및 3자 송금 확인이 어렵습니다.\n단, 본인은 양심에 따라 이용약관을 지켰음을 맹세합니다.\n`네/아니오`**"))
                await interaction.respond(embed=talmoembed("🎲 코인 충전", "**DM을 확인해주세요.**"))
            except:
                await interaction.respond(embed=talmoembed("🎲 코인 충전", "**DM을 허용해주세요.**"))

            def check(name):
                return (isinstance(name.channel, discord.channel.DMChannel) and (interaction.user.id == name.author.id))

            try:
                name = await client.wait_for("message", timeout=60, check=check)
                await nam.delete()
                name = name.content
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**시간 초과되었습니다.**"))
                except:
                    pass
                return None

            mone = await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**충전할 라이트코인 액수를 입력해주세요.\n`달러나 원 단위가 아닌, 라이트코인 액수를 입력해주세요.`**"))

            def check(money):
                return (isinstance(money.channel, discord.channel.DMChannel) and (
                        interaction.user.id == money.author.id))

            try:
                money = await client.wait_for("message", timeout=60, check=check)
                await mone.delete()
                
                livecoin_key = "72d66bed-eb47-4b26-bebb-0b8b1ce28780"#livecoinwatch.com 에서 무료 발급되긴 하는데 혹시라도 ratelimit 제한되면 니가 발급받고 바꾸셈
                btc_data_for = {"currency":"KRW","code":"LTC","meta":True}#코인 바꿀거면 BTC 를 다른거로
                header_dict = {'content-type':'application/json','x-api-key':livecoin_key}#json 선언 및 api key 전달

                get_btc_price = requests.post("https://api.livecoinwatch.com/coins/single",headers=header_dict,data=json.dumps(btc_data_for)).json()#해당 url 에 header , data 와 함께 post 후 결과값을 json 화

                btc_rate = get_btc_price['rate']

                money = money.content
                money = btc_rate*float(money)
                if int(money) < 1000:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**최소 충전 LTC 충전금액은 `한국 환율 1,000원` 이어야 합니다.**"))
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**시간 초과되었습니다.**"))
                except:
                    pass
                return None
            bonus_m = await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**선택하실 보너스를 선택해주세요.**"),
                                                  components=[Select(placeholder="선택하실 보너스를 입력해주세요",
                                                            options=bonus_selection,custom_id="계좌충전 보너스")])
            
            def check(bonus):
                return (isinstance(bonus.channel, discord.channel.DMChannel) and (
                        interaction.user.id == bonus.author.id) and (bonus.custom_id == "계좌충전 보너스"))
            bonus_amplier = 0
            bonus_rolling = 0
            try:
                bonus = await client.wait_for("select_option", timeout=60, check=check)
                bonus_split = bonus.values[0].split("-")
                bonus_amplier = float(bonus_split[0])
                bonus_rolling = int(bonus_split[1])
                await bonus_m.delete()
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None
            await interaction.user.send(embed=discord.Embed(title="LTC 충전",
                                                            description=f"**입금 계좌 : `{ltcwallet}`**\n─────────────\n한국환율로 입금 금액 : `{money}`원",
                                                            color=0x2f3136))
            screenshot = await interaction.user.send(
                embed=discord.Embed(description=f"송금 후 스크린샷을 5분 내에 보내주세요.", color=0x2f3136))

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
                            embed=discord.Embed(title="코인 충전 실패", description="올바른 사진 형식이 아닙니다.",
                                                color=0x2f3136))
                    except:
                        pass
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**시간 초과되었습니다.**"))
                except:
                    pass
                return None

            access_embed = discord.Embed(title='코인 충전 요청',
                                        description=f'디스코드 닉네임 : <@{interaction.user.id}>({interaction.user})\n이용약관 동의 : {name}\n라이트코 환율 한국돈으로 : {money}',
                                        color=0x2f3136)
            try:
                access_embed.set_image(url=sct)
            except:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**올바른 사진 형식이 아닙니다..**"))
                except:
                    pass
                return None
            await interaction.user.send(
                embed=discord.Embed(title="충전 요청 성공 ✅", description=f"관리자의 승인을 기다려주세요.",
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
                if interaction.custom_id == '승인':
                    await a_m.delete()
                    write_bet(user_id,0)
                    write_rolling(user_id,bonus_rolling)
                    add_chung1(user_id,float(money)*bonus_amplier)
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                (user_info[1] + float(money)*bonus_amplier, user_id))
                    con.commit()
                    ktotal += int(money)
                    con.close()
                    nojum = math.floor(float(money)*(bonus_amplier-1))
                    await client.get_user(user_id).send(embed=discord.Embed(title="코인 충전 성공",
                                                                            description=f"{money}원이 충전되었습니다.\n\n**`이벤트로 인하여 {nojum}원이 추가로 지급되었습니다.`**",
                                                                            color=0x2f3136))
                    await client.get_channel(요청채널).send(
                        embed=discord.Embed(title="코인 충전 성공", description=f"{interaction.user} \n\n<@{user_id}>님께 충전되었습니다. {money}원\n\n보너스 이벤트 {nojum}원\n선택 보너스 : {bonus_split[2]}",
                                            color=0x2f3136))
                    await client.get_channel(요청채널).send(f"{sct} <@{user_id}> 코인 충전 스크린")
                    log_id = 환전액로그
                    log_ch = client.get_channel(int(log_id))
                    await log_ch.send(f"<@{user_id}>님이 {int(money)}원을 충전하셨습니다! [보너스 이벤트 {nojum}원 추가지급]")
                    await asyncio.sleep(5)
                    guild = client.get_guild(int(1103334101043396669))
                    log = ""

                    id = 환전액로그
                    channel = client.get_channel(int(id))
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
                    number = int(money)
                    if number < 0 or number >= 1500000:
                        return
                    elif number < 3000:
                        return
                    elif number < 15000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 1')
                    elif number < 50000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 2')
                    elif number < 150000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 3')
                    elif number < 350000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='  • LV 4')
                    elif number < 800000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 5')
                    elif number < 1500000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 6')
                    else:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 7')

                    if role is None:
                        return
                    elif role in member.roles:
                        return
                    else:
                        await member.add_roles(role)
                        await client.get_user(user_id).send(f"RICHLAND 잔액 {number}원 누적 충전으로 인해 {role.name} 등급을 부여 받았습니다.")
                if interaction.custom_id == '거부':
                    await client.get_channel(요청채널).send(f"{sct} <@{user_id}> 충전 실패 스크린\n돈은 {money}이었어용.")
                    await a_m.delete()
                    await client.get_user(user_id).send(
                        embed=discord.Embed(title="코인 충전 실패", description=f"{interaction.user} 관리자님께서 충전을 거부하셨습니다.",
                                            color=0x2f3136))
                    await client.get_channel(요청채널).send(
                        embed=discord.Embed(title="코인 충전 실패", description=f"{interaction.user}\n\n<@{user_id}>님의 코인 충전이 거부되었습니다.",
                                            color=0x2f3136))
    
    if interaction.component.custom_id == "등급받기":
        guild = client.get_guild(int(1103334101043396669))
        user = interaction.user.id
        name = interaction.user.name
        member = interaction.user
        log = ""

        id = 환전액로그
        channel = client.get_channel(int(id))
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
        number = int(money)
        if number < 0 or number >= 1500000:
            await interaction.respond(content="받으실 등급이 없습니다.")
            return
        elif number < 3000:
            await interaction.respond(content="받으실 등급이 없습니다.")
            return
        elif number < 15000:
            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 1')
        elif number < 50000:
            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 2')
        elif number < 150000:
            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 3')
        elif number < 350000:
            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 4')
        elif number < 800000:
            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 5')
        elif number < 1500000:
            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 6')
        else:
            role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 7')

        if role is None:
            await interaction.respond(content="받으실 등급이 없습니다.")
        elif role in member.roles:
            await interaction.respond(content="받으실 등급이 없습니다.")
        else:
            await member.add_roles(role)
            await interaction.respond(content=f"{role.name} 등급을 부여 받았습니다.")
        

    if interaction.component.custom_id == "eth":
        user_id = interaction.user.id
        
        user = interaction.user.id
        name = interaction.user.name
        member = interaction.user

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        user_info = cur.fetchone()

        if (user_info == None):
            cur.execute("INSERT INTO users Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (
                interaction.user.id, 0, None, 0, 0, 0, None, None, None, None, None, None, None, None, None, None, None,
                None,
                None, None, None, None, None, None, None, None, None, None, None, None))
            con.commit()
            con.close()

        con = sqlite3.connect("./database/database.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id == ?;", (user_id,))
        user_info = cur.fetchone()

        if not (user_info == None):
            try:
                nam = await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**이더리움 송금은 3자 사기 및 3자 송금 확인이 어렵습니다.\n단, 본인은 양심에 따라 이용약관을 지켰음을 맹세합니다.\n`네/아니오`**"))
                await interaction.respond(embed=talmoembed("🎲 코인 충전", "**DM을 확인해주세요.**"))
            except:
                await interaction.respond(embed=talmoembed("🎲 코인 충전", "**DM을 허용해주세요.**"))

            def check(name):
                return (isinstance(name.channel, discord.channel.DMChannel) and (interaction.user.id == name.author.id))

            try:
                name = await client.wait_for("message", timeout=60, check=check)
                await nam.delete()
                name = name.content
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**시간 초과되었습니다.**"))
                except:
                    pass
                return None

            mone = await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**충전할 이더리움 액수를 입력해주세요.\n`달러나 원 단위가 아닌, 이더리움 액수를 입력해주세요.`**"))

            def check(money):
                return (isinstance(money.channel, discord.channel.DMChannel) and (
                        interaction.user.id == money.author.id))

            try:
                money = await client.wait_for("message", timeout=60, check=check)
                await mone.delete()
                
                livecoin_key = "72d66bed-eb47-4b26-bebb-0b8b1ce28780"#livecoinwatch.com 에서 무료 발급되긴 하는데 혹시라도 ratelimit 제한되면 니가 발급받고 바꾸셈
                btc_data_for = {"currency":"KRW","code":"ETH","meta":True}#코인 바꿀거면 BTC 를 다른거로
                header_dict = {'content-type':'application/json','x-api-key':livecoin_key}#json 선언 및 api key 전달

                get_btc_price = requests.post("https://api.livecoinwatch.com/coins/single",headers=header_dict,data=json.dumps(btc_data_for)).json()#해당 url 에 header , data 와 함께 post 후 결과값을 json 화

                btc_rate = get_btc_price['rate']

                money = money.content
                money = btc_rate*float(money)
                if int(money) < 1000:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**최소 충전 ETH 충전금액은 `한국 환율 1,000원` 이어야 합니다.**"))
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**시간 초과되었습니다.**"))
                except:
                    pass
                return None
            bonus_m = await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**선택하실 보너스를 선택해주세요.**"),
                                                  components=[Select(placeholder="선택하실 보너스를 입력해주세요",
                                                            options=bonus_selection,custom_id="계좌충전 보너스")])
            
            def check(bonus):
                return (isinstance(bonus.channel, discord.channel.DMChannel) and (
                        interaction.user.id == bonus.author.id) and (bonus.custom_id == "계좌충전 보너스"))
            bonus_amplier = 0
            bonus_rolling = 0
            try:
                bonus = await client.wait_for("select_option", timeout=60, check=check)
                bonus_split = bonus.values[0].split("-")
                bonus_amplier = float(bonus_split[0])
                bonus_rolling = int(bonus_split[1])
                await bonus_m.delete()
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "```yaml\n시간 초과되었습니다.```"))
                except:
                    pass
                return None

            await interaction.user.send(embed=discord.Embed(title="ETH 충전",
                                                            description=f"**입금 계좌 : `{btcwallet}`**\n─────────────\n한국환율로 입금 금액 : `{money}`원",
                                                            color=0x2f3136))
            screenshot = await interaction.user.send(
                embed=discord.Embed(description=f"송금 후 스크린샷을 5분 내에 보내주세요.", color=0x2f3136))

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
                            embed=discord.Embed(title="코인 충전 실패", description="올바른 사진 형식이 아닙니다.",
                                                color=0x2f3136))
                    except:
                        pass
                    return None
            except asyncio.TimeoutError:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**시간 초과되었습니다.**"))
                except:
                    pass
                return None

            access_embed = discord.Embed(title='코인 충전 요청',
                                        description=f'디스코드 닉네임 : <@{interaction.user.id}>({interaction.user})\n이용약관 동의 : {name}\n이더리움 환율 한국돈으로 : {money}',
                                        color=0x2f3136)
            try:
                access_embed.set_image(url=sct)
            except:
                try:
                    await interaction.user.send(embed=talmoembed("🎲 코인 충전", "**올바른 사진 형식이 아닙니다..**"))
                except:
                    pass
                return None
            await interaction.user.send(
                embed=discord.Embed(title="충전 요청 성공 ✅", description=f"관리자의 승인을 기다려주세요.",
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
                if interaction.custom_id == '승인':
                    await a_m.delete()
                    write_bet(user_id,0)
                    write_rolling(user_id,rolling)
                    add_chung1(user_id,float(money))
                    cur.execute("UPDATE users SET money = ? WHERE id == ?;",
                                (user_info[1] + float(money)*event1, user_id))
                    con.commit()
                    ktotal += int(money)
                    con.close()
                    nojum = math.floor(float(money)*event2)
                    await client.get_user(user_id).send(embed=discord.Embed(title="코인 충전 성공",
                                                                            description=f"{money}원이 충전되었습니다.\n\n**`보너스 이벤트로 인하여 {nojum}원이 추가로 지급되었습니다.`\n\n불이익을 당하지 않게 반드시 이용약관을 읽어주세요.**",
                                                                            color=0x2f3136))
                    await client.get_channel(요청채널).send(
                        embed=discord.Embed(title="코인 충전 성공", description=f"{interaction.user} \n\n<@{user_id}>님께 충전되었습니다. {money}원\n\n보너스 이벤트 {nojum}원",
                                            color=0x2f3136))
                    await client.get_channel(요청채널).send(f"{sct} <@{user_id}> 충전 스크린 <@790413552413573120>\n돈 {money}이었어용.")
                    log_id = 환전액로그
                    log_ch = client.get_channel(int(log_id))
                    await log_ch.send(f"<@{user_id}>님이 {int(money)}원을 충전하셨습니다! [보너스 이벤트 {nojum}원 추가지급]")
                    await asyncio.sleep(5)
                    guild = client.get_guild(int(1103334101043396669))
                    log = ""

                    id = 환전액로그
                    channel = client.get_channel(int(id))
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
                    number = int(money)
                    if number < 0 or number >= 1500000:
                        return
                    elif number < 3000:
                        return
                    elif number < 15000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 1')
                    elif number < 50000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 2')
                    elif number < 150000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 3')
                    elif number < 350000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 4')
                    elif number < 800000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 5')
                    elif number < 1500000:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 6')
                    else:
                        role = discord.utils.get(client.get_guild(int(1103334101043396669)).roles, name='ㆍLV 7')

                    if role is None:
                        return
                    elif role in member.roles:
                        return
                    else:
                        await member.add_roles(role)
                        await client.get_user(user_id).send(f"RICHLAND 잔액 {number}원 누적 충전으로 인해 {role.name} 등급을 부여 받았습니다.")
                if interaction.custom_id == '거부':
                    await client.get_channel(요청채널).send(f"{sct} <@{user_id}> 충전 실패 스크린\n돈은 {money}이었어용.")
                    await a_m.delete()
                    await client.get_user(user_id).send(
                        embed=discord.Embed(title="코인 충전 실패", description=f"{interaction.user} 관리자님께서 충전을 거부하셨습니다.",
                                            color=0x2f3136))
                    await client.get_channel(요청채널).send(
                        embed=discord.Embed(title="코인 충전 실패", description=f"{interaction.user}\n\n<@{user_id}>님의 코인 충전이 거부되었습니다.",
                                            color=0x2f3136))
                    
    


client.run(봇토큰)
