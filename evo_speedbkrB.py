from PIL import Image, ImageDraw
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


GRID_SIZE = (12, 6)
ICON_SIZE = (30, 30)
ICON_SPACING = 3  # 아이콘 간의 간격을 조정합니다.

# 색상 정의
B_COLOR = "red"
P_COLOR = "blue"
T_COLOR = "green"

# 결과를 저장할 리스트
results = []

# 결과를 추가하는 함수
def add_result(result):
    results.append(result)

# 그리드 이미지를 생성하는 함수
def create_grid():
    icon_width = ICON_SIZE[0]
    icon_height = ICON_SIZE[1]
    grid_width = GRID_SIZE[0] * (icon_width + ICON_SPACING)
    grid_height = GRID_SIZE[1] * (icon_height + ICON_SPACING)

    grid_image = Image.open("wtf.png")  # wtf.png 파일을 엽니다.
    grid_image = grid_image.resize((grid_width, grid_height))  # 그리드 크기로 리사이즈합니다.
    draw = ImageDraw.Draw(grid_image)

    x = 0
    y = 0

    for result in results:
        if result == "B":
            color = B_COLOR
        elif result == "P":
            color = P_COLOR
        elif result == "T":
            color = T_COLOR

        draw_icon(draw, x, y, color)

        y += icon_height + ICON_SPACING

        if y >= grid_height:
            y = 0
            x += icon_width + ICON_SPACING

    return grid_image

# 아이콘을 그리는 함수
def draw_icon(draw, x, y, color):
    icon_width = ICON_SIZE[0]
    icon_height = ICON_SIZE[1]
    icon_size = (int(icon_width * 0.5), int(icon_height * 0.5))
    icon_offset = (int((icon_width - icon_size[0]) / 2), int((icon_height - icon_size[1]) / 2))
    circle_box = (
        x + icon_offset[0],
        y + icon_offset[1],
        x + icon_offset[0] + icon_size[0],
        y + icon_offset[1] + icon_size[1],
    )

    draw.ellipse(circle_box, fill=None, outline=color, width=2)

    # 아이콘 간격을 추가합니다.
    x += icon_width + ICON_SPACING

    return x, y

def reset_results():
    results.clear()


session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
try:
 with open('save/save6.txt', 'rb') as f:
    session.cookies.update(pickle.load(f))
except:
  pass
#저장된 로그인 쿠키가 있는 경우 다시 로그인을 시도하지 않고 저장된 쿠키로 시도
r = session.get("https://oraksil-7979.com/account/messages", headers=headers) 
if('200' not in r):
 #로그인 시도
 #안파랑 씨발아
 payload = {
    'userid': 'qhdns123',
    'password': 'qhdns123',
    }
 r = session.post("https://api.support-oraksil.com/users", headers=headers, data=json.dumps(payload))
 with open('save/save6.txt', 'wb') as f:
  pickle.dump(session.cookies, f)

#카지노 로드
 payload = {
    'gamecode': 'top_games',
    'thirdpartycode': '1',
    }
r = session.put("https://api.support-oraksil.com/casino", headers=headers, data=json.dumps(payload))
nomu = r.json()
r = session.get(nomu['data']['link'], headers=headers)
#이 위로 수정 ㄴ
r = session.get("https://babylonvg.evo-games.com/frontend/evo/r3/#category=baccarat_sicbo&game=baccarat&table_id=lv2kzclunt2qnxo5", headers=headers)
#여기만 수정 table_id=테이블 아이디
#여기부터 수정 ㄴㄴ
headers['Sec-WebSocket-Key'] = str(base64.b64encode(bytes([random.randint(0, 255) for _ in range(16)])), 'ascii')
headers['Sec-WebSocket-Version'] = '13'
headers['Upgrade'] = 'websocket'

def replace_cards(lst):
    for i in range(len(lst)):
        if "C" in lst[i]:
            lst[i] = lst[i].replace("C", " 클로버")
        if "H" in lst[i]:
            lst[i] = lst[i].replace("H", " 하트")
        if "D" in lst[i]:
            lst[i] = lst[i].replace("D", " 다이아")
        if "S" in lst[i]:
            lst[i] = lst[i].replace("S", " 스페이드")
        if "T" in lst[i]:
            lst[i] = lst[i].replace("T", "10")
    return lst

cookies = session.cookies.get_dict()
print("OK")
#수정 ㄴㄴ 여기까지
def on_message1(ws1, message):
        filename = "evobkrA.txt"
        
        if "dealer.changed" in message:
            msg = json.loads(message)
            wi1 = msg['args']['dealer']['screenName']
            try:
              webhook = DiscordWebhook(url=에볼루션스피드바카라B, username="스피드 바카라 B")
              embed = DiscordEmbed(title="**스피드 바카라 B**", description="딜러 변경 : "+str(wi1))
              webhook.add_embed(embed)
              response = webhook.execute()
            except:
                pass

        elif "baccarat.cardDealt" in message:
           msg = json.loads(message)
           id = msg['args']['gameId']
           global pformattedcard, bformattedcard
           pscore = msg['args']['gameData']['playerHand']['score']
           bscore = msg['args']['gameData']['bankerHand']['score']
           pcard = msg['args']['gameData']['playerHand']['cards']
           bcard = msg['args']['gameData']['bankerHand']['cards']
           try:
              pformattedcard = replace_cards(pcard)
              bformattedcard = replace_cards(bcard)
              webhook = DiscordWebhook(url=에볼루션스피드바카라B, username=id)
              embed = DiscordEmbed(title="**스피드 바카라 B**", description="**```d\nPlayer : "+str(pscore)+f"\n{pformattedcard}\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\nBanker : "+str(bscore)+f"\n{bformattedcard}```**")
              webhook.add_embed(embed)
              response = webhook.execute()
           except Exception as e:
                print(e)
                pass
           

        elif "widget.resolved" in message:
            msg = json.loads(message)
            id = msg['args']['gameId']
            wi = msg['args']['result']['winner']
            ps = msg['args']['result']['playerScore']
            bs = msg['args']['result']['bankerScore']
            pf = msg['args']['result']['playerPair']
            bf = msg['args']['result']['bankerPair']
            if(str(pf) == 'True'):
               pp = "플레이어 페어"
               justp = "페어 O"
            else:
               pp = "X"
               justp = "X"
            
            
            if(str(bf) == 'True'):
               bp = "뱅커 페어"
               justb = "페어 O"
            else:
               bp = "X"
               justb = "X"
            if(str(wi) == 'Player'):
              ukor = '플레이어'
              배당 = 2
              add_result("P")

              grid_image = create_grid()

              grid_image.save("grid3.png")
              # resultemoji += f" :blue_circle:"
              
            elif(str(wi) == 'Banker'):
              ukor = '뱅커'
              배당 = 1.95
              add_result("B")

              grid_image = create_grid()

              grid_image.save("grid3.png")
              # resultemoji += f" :red_circle:"
            else:
              ukor = '타이'
              배당 = 8
              add_result("T")

              grid_image = create_grid()

              grid_image.save("grid3.png")
            try:
              conn = sqlite3.connect('./database/database.db')
              c = conn.cursor()
              list_a = list(c.execute("SELECT * FROM users"))
              conn.close()
              webhook = DiscordWebhook(url=에볼루션스피드바카라B, username=id)
              embed = DiscordEmbed(title="**스피드 바카라 B**", description="**```d\nPlayer : "+str(ps)+f"\n{pformattedcard}\nㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ\nBanker : "+str(bs)+f"\n{bformattedcard}```\n```d\nPlayer Pair : {justp}\nBanker Pair : {justb}```\n\nWinner : `{str(wi)}`**")
              webhook.add_embed(embed)
              response = webhook.execute()
              for i in list_a:
                if(i[84] == None):
                  # print("none")
                  continue

                conn = sqlite3.connect('./database/database.db')
                c = conn.cursor()

                if i[84] == ukor:
                  headers = {
                      "Authorization": f"Bot {봇토큰}"
                  }
                  js = {
                      "recipient_id": i[0]
                  }
                  headers = headers
                  res = requests.post(url="https://discordapp.com/api/v9/users/@me/channels", json=js,
                                      headers=headers)
                  data = res.json()
                  dm_channel_id = data['id']
                  
                  embed = { 'title': f'적중', 'description': f'```배팅 게임 : 에볼루션 스피드바카라 B\n배팅 내역 : {i[84]}\n배팅 금액 : {i[85]}원\n─────────────\n적중 금액 : {round(i[85] * (배당-1))}\n남은 금액 : {i[1] + round(i[85] * 배당)}```', 'color' : 0x00FF00}
                  req = requests.post(f"https://discordapp.com/api/v9/channels/{dm_channel_id}/messages",
                  headers=headers, json={
                  'content' : f"<@{i[0]}> ", 'embed' : embed})
                  c.execute("UPDATE users SET money = ? WHERE id == ?;", (i[1] + round(i[85] * 배당), i[0]))
                elif i[84] == pp or i[84] == bp:
                    headers = {
                        "Authorization": f"Bot {봇토큰}"
                    }
                    js = {
                        "recipient_id": i[0]
                    }
                    headers = headers
                    res = requests.post(url="https://discordapp.com/api/v9/users/@me/channels", json=js,
                                        headers=headers)
                    data = res.json()
                    dm_channel_id = data['id']

                    embed = { 'title': f'적중', 'description': f'```배팅 게임 : 에볼루션 코리안스피드바카라 B\n배팅 내역 : {i[86]}\n배팅 금액 : {i[87]}원\n─────────────\n적중 금액 : {round(i[87] * 11)}\n남은 금액 : {i[1] + round(i[87] * 12)}```', 'color' : 0x00FF00}
                    req = requests.post(f"https://discordapp.com/api/v9/channels/{dm_channel_id}/messages",
                    headers=headers, json={
                    'content' : f"<@{i[0]}> ", 'embed' : embed})
                    c.execute("UPDATE users SET money = ? WHERE id == ?;", (i[1] + round(i[87] * 12), i[0]))
                else:
                  if ukor == "타이":
                    headers = {
                        "Authorization": f"Bot {봇토큰}"
                    }
                    js = {
                        "recipient_id": i[0]
                    }
                    headers = headers
                    res = requests.post(url="https://discordapp.com/api/v9/users/@me/channels", json=js,
                                        headers=headers)
                    data = res.json()
                    dm_channel_id = data['id']
                    embed = { 'title': f'무승부', 'description': f'```배팅 게임 : 에볼루션 스피드바카라 B\n배팅 내역 : {i[84]}\n배팅 금액 : {i[85]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {i[1] + i[85]}```', 'color' : 0xFF0000}
                    req = requests.post(f"https://discordapp.com/api/v9/channels/{dm_channel_id}/messages",
                    headers=headers, json={
                    'content' : f"<@{i[0]}> ", 'embed' : embed})
                    c.execute("UPDATE users SET money = ? WHERE id == ?;", (i[1] + round(i[85]), i[0]))
                  else:
                    headers = {
                        "Authorization": f"Bot {봇토큰}"
                    }
                    js = {
                        "recipient_id": i[0]
                    }
                    headers = headers
                    res = requests.post(url="https://discordapp.com/api/v9/users/@me/channels", json=js,
                                        headers=headers)
                    data = res.json()
                    dm_channel_id = data['id']
                    embed = { 'title': f'미적중', 'description': f'```배팅 게임 : 에볼루션 스피드바카라 B\n배팅 내역 : {i[84]}\n배팅 금액 : {i[85]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {i[1]}```', 'color' : 0xFF0000}
                    req = requests.post(f"https://discordapp.com/api/v9/channels/{dm_channel_id}/messages",
                    headers=headers, json={
                    'content' : f"<@{i[0]}> ", 'embed' : embed})
                    
                c.execute("UPDATE users SET evobkrB_pick = ? where id=?", (None, i[0],))
                c.execute("UPDATE users SET evobkrB_money = ? where id=?", (None, i[0],))
                conn.commit()
                conn.close()      
            except Exception as e:
              print(e)
              pass

        elif "baccarat.gameState" in message:
            msg = json.loads(message)
            id = msg['args']['gameId']
            tasty = msg['args']['dealing']
            if(tasty == 'Dealing'):
                #반드시 베팅을 막아야합니다.
                #여기에 코드를 넣으세요.
                
                with open(filename, 'w') as file:
                  file.write("1")
                try:
                  webhook = DiscordWebhook(url=에볼루션스피드바카라B, username=id)
                  embed = DiscordEmbed(title="**스피드 바카라 B**", description="**```diff\n- 배팅마감, 딜러가 딜링을 시작합니다.```**")
                  webhook.add_embed(embed)
                  response = webhook.execute()
                except:
                   pass   
            elif(tasty == 'Finished'):
             #딜링이 끝났고 베팅이 가능한 상태입니다.
             
              with open(filename, 'w') as file:
                  file.write("0")
              try:
                webhook = DiscordWebhook(url=에볼루션스피드바카라B, username=id)
                embed = DiscordEmbed(title="**스피드 바카라 B**", description=f"**```diff\n+ 딜링이 끝났습니다, 배팅이 가능하십니다.```**")
                webhook.add_embed(embed)
                response = webhook.execute()
                image_path = "grid3.png"
                webhook_url = 에볼루션스피드바카라B

                with open(image_path, "rb") as image_file:
                    image_data = image_file.read()

                payload = {
                    "file": ("grid3.png", image_data)
                }

                response = requests.post(webhook_url, files=payload)
              except:
                pass


           
                  

def on_error1(ws1, error):
    print(error)
    print("### ERROR ###")
    time.sleep(10)
    os.execv(sys.executable, ['python'] + sys.argv)
    #에볼루션은 주기적으로 비활성화 (베팅을 하지 않는 유저) 유저의 세션을 종료합니다. 그 경우 파일이 자동으로 재시작됩니다.


def on_close1(ws1, close_status_code, close_msg):
    time.sleep(10)
    os.execv(sys.executable, ['python'] + sys.argv)
    #에볼루션은 주기적으로 비활성화 (베팅을 하지 않는 유저) 유저의 세션을 종료합니다. 그 경우 파일이 자동으로 재시작됩니다.


def on_open1(ws1):
    print("Opened connection 1")

oki = cookies['EVOSESSIONID'][0:17]
#oki 수정하지 마세요
def wsjoa1():
 #테이블 아이디로 수정 /game/테이블아이디/socket?
 ws1 = websocket.WebSocketApp('wss://babylonvg.evo-games.com/public/baccarat/player/game/lv2kzclunt2qnxo5/socket?messageFormat=json&instance=bt1fz-'+str(oki)+'-leqhceumaq6qfoug&tableConfig=&EVOSESSIONID='+str(cookies['EVOSESSIONID'])+'&client_version=6.20230327.72627.23195-882f9014ff',
                       header=headers,
                       cookie="; ".join(["%s=%s" %(i, j) for i, j in cookies.items()]),
                       on_open=on_open1,
                       on_message=on_message1,
                       on_error=on_error1,
                       on_close=on_close1
 )

 ws1.run_forever()
wsjoa1()


