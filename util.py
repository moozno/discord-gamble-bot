import requests, sys, asyncio
import discord

client = discord.Client()

from Setting import *
token = {봇토큰}

@client.event
async def on_ready():
  print(client.user)


@client.event
async def on_message(message):
    if message.content.startswith ("!청소"):
        if message.author.guild_permissions.administrator:
            amount = message.content.split(" ")[1]
            await message.delete()
            await message.channel.purge(limit=int(amount))
            embed = discord.Embed(color=0x2f3136, timestamp=message.created_at)
            embed = discord.Embed(title="코린랜드 청소봇", description="메시지 {}개를 {}님이 삭제하였습니다".format(amount, message.author), color=0x2f3136)
            msg = await message.channel.send(embed=embed)
            await asyncio.sleep(3)
            await msg.delete()
        else:
            await message.delete()
            await message.channel.send("{}, 당신은 권한이 없습니다! ".format(message.author.mention))

    if message.content.startswith("!웹훅생성"):
        if message.author.guild_permissions.administrator:
            dc = message.content.split(" ")[1]
            ch = client.get_channel(int(dc))
            webhook = await ch.create_webhook(name=message.author, reason='리틀뱅크 웹훅생성')
            await message.reply('웹훅 생성해왔습니다\n' + webhook.url)
        else:
            await message.channel.send("{}, 당신은 권한이 없습니다! ".format(message.author.mention))
            
    if message.content.startswith("!say"):
        if message.author.guild_permissions.administrator:
            dc = message.content[5:]
            await message.delete()
            await message.channel.send(dc)
        else:
            await message.channel.send("{}, 당신은 권한이 없습니다! ".format(message.author.mention))



client.run(봇토큰)