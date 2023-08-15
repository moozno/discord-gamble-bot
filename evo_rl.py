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
    with open("save/save3.txt", "rb") as f:
        session.cookies.update(pickle.load(f))
except:
    pass
# 저장된 로그인 쿠키가 있는 경우 다시 로그인을 시도하지 않고 저장된 쿠키로 시도
r = session.get("https://oraksil-7979.com/account/messages", headers=headers)
if "200" not in r:
    # 로그인 시도
    # 안파랑 씨발아
    payload = {
        "userid": "alsrkdTm",
        "password": "alsrkddldmlqkqqjrj",
    }
    r = session.post(
        "https://api.support-oraksil.com/users",
        headers=headers,
        data=json.dumps(payload),
    )
    with open("save/save3.txt", "wb") as f:
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
    "https://babylonvg.evo-games.com/frontend/evo/r3/#category=roulette&game=roulette&table_id=vctlz20yfnmp1ylr",
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
    filename = "evo_rl.txt"

    if "dealer.changed" in message:
        msg = json.loads(message)
        wi1 = msg["args"]["dealer"]["screenName"]
        try:
            webhook = DiscordWebhook(url=에볼룰렛, username="룰렛")
            embed = DiscordEmbed(title="**룰렛**", description="딜러 변경 : " + str(wi1))
            webhook.add_embed(embed)
            response = webhook.execute()
        except:
            pass

    elif "roulette.tableState" in message:
        msg = json.loads(message)
        id = msg["args"]["gameId"]
        rlmsg = msg["args"]["state"]
        if rlmsg == "BETS_CLOSED_ANNOUNCED":
            with open(filename, "w") as file:
                file.write("1")
            try:
                webhook = DiscordWebhook(url=에볼룰렛, username=id)
                embed = DiscordEmbed(
                    title="**룰렛**", description="**```diff\n- 배팅마감, 룰렛이 돌아갑니다.```**"
                )
                webhook.add_embed(embed)
                response = webhook.execute()
            except Exception as e:
                print(e)
                pass
        elif rlmsg == "BETS_OPEN":
            with open(filename, "w") as file:
                file.write("0")
            try:
                webhook = DiscordWebhook(url=에볼룰렛, username=id)
                embed = DiscordEmbed(
                    title="**룰렛**",
                    description="**```diff\n+ 딜링이 끝났습니다, 배팅이 가능하십니다.```**",
                )
                webhook.add_embed(embed)
                response = webhook.execute()
            except Exception as e:
                print(e)
                pass
        elif rlmsg == "GAME_RESOLVED":
            rlnumber = int(msg["args"]["result"][0])
            holchak = ""

            rgb = ""

            if rlnumber % 2 == 0 and rlnumber != 0:
               holchak = "짝수"
            elif rlnumber % 2 == 1 and rlnumber != 0:
               holchak = "홀수"
            else:
               holchak = "0"

            red = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]

            if rlnumber == 0:
               rgb = "그린"
               배당 = 10
            elif rlnumber in red:
               rgb = "레드"
               배당 = 2
            elif not rlnumber in red and rlnumber != 0:
               rgb = "블랙"
               배당 = 2

            try:
               conn = sqlite3.connect("./database/database.db")
               c = conn.cursor()
               list_a = list(c.execute("SELECT * FROM users"))
               conn.close()
               webhook = DiscordWebhook(url=에볼룰렛, username=id)
               embed = DiscordEmbed(
                  title="**룰렛**",
                  description=f"**```d\n숫자 : {rlnumber}```\n```yaml\n결과 : {rgb} / {holchak}```**",
               )
               webhook.add_embed(embed)
               response = webhook.execute()
               for i in list_a:
                  if i[82] == None:
                     # print("none")
                     continue

                  conn = sqlite3.connect("./database/database.db")
                  c = conn.cursor()

                  if i[82] == rgb or i[82] == holchak:
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
                           "description": f"```배팅 게임 : 에볼루션 룰렛\n배팅 내역 : {i[82]}\n배팅 금액 : {i[83]}원\n─────────────\n적중 금액 : {round(i[83] * (배당-1))}\n남은 금액 : {i[1] + round(i[83] * 배당)}```",
                           "color": 0x00FF00,
                     }
                     req = requests.post(
                           f"https://discordapp.com/api/v9/channels/{dm_channel_id}/messages",
                           headers=headers,
                           json={"content": f"<@{i[0]}> ", "embed": embed},
                     )
                     c.execute(
                           "UPDATE users SET money = ? WHERE id == ?;",
                           (i[1] + round(i[83] * 배당), i[0]),
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
                           "description": f"```배팅 게임 : 에볼루션 룰렛\n배팅 내역 : {i[82]}\n배팅 금액 : {i[83]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {i[1]}```",
                           "color": 0xFF0000,
                     }
                     req = requests.post(
                           f"https://discordapp.com/api/v9/channels/{dm_channel_id}/messages",
                           headers=headers,
                           json={"content": f"<@{i[0]}> ", "embed": embed},
                     )

                  c.execute(
                     "UPDATE users SET evorl_pick = ? where id=?",
                     (
                           None,
                           i[0],
                     ),
                  )
                  c.execute(
                     "UPDATE users SET evorl_money = ? where id=?",
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
        "wss://babylonvg.evo-games.com/public/roulette/player/game/vctlz20yfnmp1ylr/socket?messageFormat=json&instance=bt1fz-"
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
