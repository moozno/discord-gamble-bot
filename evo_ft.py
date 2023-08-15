import sqlite3
import requests
from bs4 import BeautifulSoup
import base64
import random
import websocket
import time
import json
import re
import pickle
from Setting import *
import asyncio
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
import sys
import math
import schedule


session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
}
try:
    with open("save/save7.txt", "rb") as f:
        session.cookies.update(pickle.load(f))
except:
    pass
# 저장된 로그인 쿠키가 있는 경우 다시 로그인을 시도하지 않고 저장된 쿠키로 시도
r = session.get("https://oraksil-7979.com/account/messages", headers=headers)
if "200" not in r:
    # 로그인 시도
    # 안파랑 씨발아
    payload = {
        "userid": "dogbo0522",
        "password": "tprtmgkrhtlvek",
    }
    r = session.post(
        "https://api.support-oraksil.com/users",
        headers=headers,
        data=json.dumps(payload),
    )
    with open("save/save7.txt", "wb") as f:
        pickle.dump(session.cookies, f)

    # 카지노 로드
    payload = {
        "gamecode": "top_games",
        "thirdpartycode": "1",
    }
r = session.put(
    "https://api.support-oraksil.com/casino", headers=headers, data=json.dumps(payload)
)
nomu = r.json()
r = session.get(nomu["data"]["link"], headers=headers)
# 이 위로 수정 ㄴ
r = session.get(
    "https://babylonvg.evo-games.com/frontend/evo/r2/#category=top_games&game=fantan&table_id=FanTan0000000001",
    headers=headers,
)
# 여기만 수정 table_id=테이블 아이디
# 여기부터 수정 ㄴㄴ
headers["Sec-WebSocket-Key"] = str(
    base64.b64encode(bytes([random.randint(0, 255) for _ in range(16)])), "ascii"
)
headers["Sec-WebSocket-Version"] = "13"
headers["Upgrade"] = "websocket"

cookies = session.cookies.get_dict()
print("OK")


# 수정 ㄴㄴ 여기까지
def on_message1(ws1, message):
    filename = "evo_ft.txt"

    if "dealer.changed" in message:
        msg = json.loads(message)
        wi1 = msg["args"]["dealer"]["screenName"]
        try:
            webhook = DiscordWebhook(url=에볼판탄, username="판탄")
            embed = DiscordEmbed(title="**판탄**", description="딜러 변경 : " + str(wi1))
            webhook.add_embed(embed)
            response = webhook.execute()
        except:
            pass


    elif "fantan.gameResolved" in message:
        msg = json.loads(message)
        id = msg["args"]["gameId"]
        ftacc = int(msg["args"]["result"])
        holchak = ""
        updown = ""

        if ftacc % 2 == 0:
            holchak = "짝수"
        else:
            holchak = "홀수"
        
        if ftacc == 1 or ftacc == 2:
            updown = "낮은 수"
        else:
            updown = "높은 수"
        


        try:
            conn = sqlite3.connect("./database/database.db")
            c = conn.cursor()
            list_a = list(c.execute("SELECT * FROM users"))
            conn.close()
            webhook = DiscordWebhook(url=에볼판탄, username=id)
            embed = DiscordEmbed(
                title="**판탄**",
                description=f"**```d\n숫자 : {ftacc}```\n```yaml\n결과 : {holchak} / {updown}```**",
            )
            webhook.add_embed(embed)
            response = webhook.execute()
            for i in list_a:
                if i[88] == None:
                    # print("none")
                    continue

                conn = sqlite3.connect("./database/database.db")
                c = conn.cursor()

                if i[88] == holchak or i[88] == updown or i[88] == ftacc:
                    if i[88] == ftacc:
                        배당 = 3.85
                    else:
                        배당 = 1.95
                    headers = {"Authorization": f"Bot {봇토큰}"}
                    js = {"recipient_id": i[0]}
                    headers = headers
                    res = requests.post(
                        url="https://discordapp.com/api/v9/users/@me/channels",
                        json=js,
                        headers=headers,
                    )
                    data = res.json()
                    dm_channel_id = data["id"]

                    embed = {
                        "title": f"적중",
                        "description": f"```배팅 게임 : 에볼루션 판탄\n배팅 내역 : {i[88]}\n배팅 금액 : {i[89]}원\n─────────────\n적중 금액 : {round(i[89] * (배당-1))}\n남은 금액 : {i[1] + round(i[89] * 배당)}```",
                        "color": 0x00FF00,
                    }
                    req = requests.post(
                        f"https://discordapp.com/api/v9/channels/{dm_channel_id}/messages",
                        headers=headers,
                        json={"content": f"<@{i[0]}> ", "embed": embed},
                    )
                    c.execute(
                        "UPDATE users SET money = ? WHERE id == ?;",
                        (i[1] + round(i[89] * 배당), i[0]),
                    )
                else:
                    headers = {"Authorization": f"Bot {봇토큰}"}
                    js = {"recipient_id": i[0]}
                    headers = headers
                    res = requests.post(
                        url="https://discordapp.com/api/v9/users/@me/channels",
                        json=js,
                        headers=headers,
                    )
                    data = res.json()
                    dm_channel_id = data["id"]
                    embed = {
                        "title": f"미적중",
                        "description": f"```배팅 게임 : 에볼루션 판탄\n배팅 내역 : {i[88]}\n배팅 금액 : {i[89]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {i[1]}```",
                        "color": 0xFF0000,
                    }
                    req = requests.post(
                        f"https://discordapp.com/api/v9/channels/{dm_channel_id}/messages",
                        headers=headers,
                        json={"content": f"<@{i[0]}> ", "embed": embed},
                    )

                c.execute(
                    "UPDATE users SET evoft_pick = ? where id=?",
                    (
                        None,
                        i[0],
                    ),
                )
                c.execute(
                    "UPDATE users SET evoft_money = ? where id=?",
                    (
                        None,
                        i[0],
                    ),
                )
                conn.commit()
                conn.close()
        except Exception as e:
            print(e)
            pass

    
    elif "fantan.betsClosed" in message:
        msg = json.loads(message)
        id = msg["args"]["gameId"]
        with open(filename, "w") as file:
            file.write("1")
        try:
            webhook = DiscordWebhook(url=에볼판탄, username=id)
            embed = DiscordEmbed(
                title="**판탄**", description="**```diff\n- 배팅마감, 숫자를 셉니다.```**"
            )
            webhook.add_embed(embed)
            response = webhook.execute()
        except Exception as e:
            print(e)
            pass
    elif "fantan.betsOpen" in message:
        msg = json.loads(message)
        id = msg["args"]["gameId"]
        with open(filename, "w") as file:
            file.write("0")
        try:
            webhook = DiscordWebhook(url=에볼판탄, username=id)
            embed = DiscordEmbed(
                title="**판탄**",
                description="**```diff\n+ 딜링이 끝났습니다, 배팅이 가능하십니다.```**",
            )
            webhook.add_embed(embed)
            response = webhook.execute()
        except Exception as e:
            print(e)
            pass

def on_error1(ws1, error):
    print(error)
    print("### ERROR ###")
    time.sleep(10)
    os.execv(sys.executable, ["python"] + sys.argv)
    # 에볼루션은 주기적으로 비활성화 (베팅을 하지 않는 유저) 유저의 세션을 종료합니다. 그 경우 파일이 자동으로 재시작됩니다.


def on_close1(ws1, close_status_code, close_msg):
    time.sleep(10)
    os.execv(sys.executable, ["python"] + sys.argv)
    # 에볼루션은 주기적으로 비활성화 (베팅을 하지 않는 유저) 유저의 세션을 종료합니다. 그 경우 파일이 자동으로 재시작됩니다.


def on_open1(ws1):
    print("Opened connection 1")


oki = cookies["EVOSESSIONID"][0:17]


# oki 수정하지 마세요
def wsjoa1():
    # 테이블 아이디로 수정 /game/테이블아이디/socket?
    ws1 = websocket.WebSocketApp(
        "wss://babylonvg.evo-games.com/public/fantan/player/game/FanTan0000000001/socket?messageFormat=json&instance=bt1fz-"
        + str(oki)
        + "-leqhceumaq6qfoug&tableConfig=&EVOSESSIONID="
        + str(cookies["EVOSESSIONID"])
        + "&client_version=6.20230327.72627.23195-882f9014ff",
        header=headers,
        cookie="; ".join(["%s=%s" % (i, j) for i, j in cookies.items()]),
        on_open=on_open1,
        on_message=on_message1,
        on_error=on_error1,
        on_close=on_close1,
    )

    ws1.run_forever()


wsjoa1()
