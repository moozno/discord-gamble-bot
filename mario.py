import requests, time, random, json, sqlite3
from Setting import *

while True:
    try:
        # res = requests.get("https://bepick.net/live/result/jw_supermario?_="+str(time.time()).split(".")[0], headers={
        #             "Cookie": f"PHPSESSID=8j6q{random.randint(100,999)}2vba{random.randint(100,999)}kgtk626{random.randint(100,999)}r1; __cfruid=669704593{random.randint(100,999)}d435{random.randint(100,999)}191986d7{random.randint(100,999)}56d704b189-1{random.randint(100,999)}927909; open_chat_tab=lottery; best_family_master=fipn6{random.randint(100,999)}b351cf3a2c9d3f8c570{random.randint(100,999)}5d536f8be4; top_family_master=5mn6v1yi31ae4a7d34{random.randint(100,999)}21d0{random.randint(100,999)}a950263412f1; best=1p6ns293ba5e586be1b9dea5d84{random.randint(100,999)}b33d889e02; _ga=GA1.2.2010{random.randint(100,999)}188.1651927914; _gid=GA1.2.14{random.randint(100,999)}60696.16{random.randint(100,999)}27914",
        #     # "Host": "ntry.com",
        #     # "Referer": "http://ntry.com/scores/power_ladder/live.php",
        #     "User-Agent": f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4{random.randint(100,999)}.54 Safari/537.{random.randint(1,211)}",
        #     "X-Requested-With": "XMLHttpRequest",
        # }).json()
        import urllib.request

        url = 'https://bepick.net/live/result/jw_supermario'

        # User Agent 설정
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        # URL에서 JSON 데이터 가져오기
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)

        # 응답 데이터 읽기
        data = response.read()

        # JSON 데이터를 파이썬 객체로 변환
        res = json.loads(data)
        old_data = {}
        resp=res
        with open("./mario.json", "r", encoding="utf8") as fp:
            old_data = json.loads(fp.read().strip())
        if( old_data == res ):
            pass
        else:
            with open("./mario.json", "w", encoding="utf8") as fp:
               # ow=int(res["fd1"])
               # con = sqlite3.connect("./database/database.db")
               # cur = con.cursor()
                #cur.execute("SELECT * FROM users WHERE id == ?;", (687467109243945121,))
               # user_info = cur.fetchone()
              #  if user_info[12]!=None:
                   # print(user_info[12])

                    
                fp.write(json.dumps(res))
                fields = []
                fields.append({'name': '파이프패턴', 'value': f'{ "금" if int(res["fd1"]) % 2 == 0 else "은" }'})
                fields.append({'name': '마리오패턴', 'value': f'{ "대" if int(res["fd2"]) % 2 == 0 else "소" }'})
                embed = { 'title': '슈퍼마리오 결과', 'description': f'{res["round"]}회차', 'fields': fields }
                requests.post(마리오, json={'username': f'{res["round"]}회차 슈퍼마리오 결과', "embeds": [embed]})

        # print(res)
                conn = sqlite3.connect('./database/database.db')
                c = conn.cursor()
                list_a = list(c.execute("SELECT * FROM users"))
                conn.close()
                pipe = "금" if int(res["fd1"]) % 2 == 0 else "은"
                sojae = "대" if int(res["fd1"]) % 2 == 0 else "소"
                for i in list_a:
                    if(i[44] == None):
                        # print("none")
                        continue
                    
                    print("found")

                    conn = sqlite3.connect('./database/database.db')
                    c = conn.cursor()



                    if(i[44] == sojae or i[44] == pipe):
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
                        embed = { 'title': f'적중', 'description': f'```배팅 게임 : 슈퍼마리오\n배팅 회차 : {resp["round"]}\n배팅 내역 : {i[44]}\n배팅 금액 : {i[45]}원\n─────────────\n적중 금액 : {round(i[45] * 0.98)}\n남은 금액 : {i[1] + round(i[45] * 1.98)}```', 'color' : 0x00FF00}
                        req = requests.post(f"https://discordapp.com/api/v9/channels/{dm_channel_id}/messages",
                        headers=headers, json={
                        'content' : f"<@{i[0]}> ", 'embed' : embed})
                        c.execute("UPDATE users SET money = money + ? where id=?", (round(i[45] * 1.98), i[0],))
                        f = open(f"./bet_log/{i[0]}.txt", "a", encoding="utf-8-sig")
                        f.write(
                            f'''                
    배팅게임 : 슈퍼마리오
    배팅회차 : {resp["round"]}
    배팅내역 : {i[44]}
    배팅금 : {i[45]}
    적중 / 미적중 : 적중
    적중 금액 : {round(i[45] * 0.98)}
    남은 금액 : {i[1] + round(i[45] * 1.98)}
    ======================
    ''')
                        f.close()
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
                        embed = { 'title': f'미적중', 'description': f'```배팅 게임 : 슈퍼마리오\n배팅 회차 : {resp["round"]}\n배팅 내역 : {i[44]}\n배팅 금액 : {i[45]}원\n─────────────\n적중 금액 : 0\n남은 금액 : {i[1]}```', 'color' : 0xFF0000}
                        req = requests.post(f"https://discordapp.com/api/v9/channels/{dm_channel_id}/messages",
                        headers=headers, json={
                        'content' : f"<@{i[0]}> ", 'embed' : embed})
                        f = open(f"./bet_log/{i[0]}.txt", "a", encoding="utf-8-sig")
                        f.write(
                            f'''                
    배팅게임 : 슈퍼마리오
    배팅회차 : {resp["round"]}
    배팅내역 : {i[44]}
    배팅금 : {i[45]}
    적중 / 미적중 : 미적중
    남은 금액 : {i[1]}
    ======================
    ''')
                        f.close()
                    c.execute("UPDATE users SET kino_ladder_pick = ? where id=?", (None, i[0],))
                    c.execute("UPDATE users SET kino_ladder_money = ? where id=?", (None, i[0],))
                    conn.commit()
                    conn.close()

        time.sleep(5)
    except:
        pass