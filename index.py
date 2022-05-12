from email.errors import MessageError
import discord
import logging
import difflib
import asyncio
import time
import random
import requests
import json
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

client = discord.Client()
token = "OTY1NTgxNDUzMDUwMTQ2ODE2.GJMfZb.nLiJNtNhUPNUN5AS_EShApNOUsJN2Ddqt6TlxI"

badword = ['바보', '멍청이']

@client.event
async def on_ready():
    print("봇이 온라인으로 전환되었습니다.")

@client.event
#임베드 출력
async def on_message(message):
    if message.content == "!안녕":
        embed = discord.Embed(title="👋 안녕하세요!",
                              description=f"[ {message.author.mention} ]", color=0x00FFFF)
        embed.set_image(url="https://cdn.discordapp.com/attachments/970965273001742349/973480143404269618/pngwing.com_3.png")
        await message.channel.send(embed=embed)

#명령어 출력
    if message.content == "!명령어":
        embed = discord.Embed(title="명령어",description="!안녕/!날씨/!코로나/!청소/!타자연습", color=0xFF9900)
        await message.channel.send(embed=embed)

#날씨 출력
    if message.content == "!날씨":
        def check(m):
            return m.author == message.author and m.channel == message.channel
       
        embed1 = discord.Embed(title="‼지역을 입력하세요‼", description="서울, 수원, 부산, 대전, 대구", color=0xFFFF00)
        #await message.channel.send("입력하세요 : 서울, 수원, 부산, 대전, 대구")
        await message.channel.send(embed=embed1)
        msg = await client.wait_for("message", check=check, timeout=30)

        dictionary ={"서울":"Seoul", "수원":"Suwon", "부산":"Busan","대전":"Daejeon", "대구":"Daegu"}
        city = dictionary[msg.content] 
        
        apikey = "f6fe9e2744c7055b9e815531a456ac29"
        lang = "kr"
        api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apikey}&lang={lang}&units=metric"
        result = requests.get(api)
        data = json.loads(result.text)

        weather = data["weather"][0]["description"]
        maintemp = data["main"]["temp"]
        feeltemp = data["main"]["feels_like"]
        mintemp = data["main"]["temp_min"]
        maxtemp = data["main"]["temp_max"]
        humidtiy = data["main"]["humidity"]

        # _result = f"날씨 : {weather}\n현재 온도 : {int(maintemp)}\n체감 온도 : {int(feeltemp)}\n최저 온도 : {int(mintemp)}\n최고 온도 : {int(maxtemp)}\n습도 : {humidtiy}%"
        # await message.channel.send(_result)

        embed = discord.Embed(title="오늘의 날씨", description="", color=0xFFFF00)
        embed.set_author(name="OpenWeather", url="https://openweathermap.org/weather-conditions", icon_url="http://openweathermap.org/img/wn/10d@2x.png")
        embed.add_field(name="날씨", value = weather , inline=True)
        embed.add_field(name="현재온도", value = f"{int(maintemp)}°C" , inline=True)
        embed.add_field(name="체감온도", value = f"{int(feeltemp)}°C" , inline=True)
        embed.add_field(name="최소온도", value = f"{int(mintemp)}°C" , inline=True)
        embed.add_field(name="최대온도", value = f"{int(maxtemp)}°C" , inline=True)
        embed.add_field(name="습도", value = f"{humidtiy}%" , inline=True)
        if weather == '맑음':
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/970965273001742349/973471612429017118/pngwing.com_2.png")
        elif weather == '튼구름':
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/970965273001742349/973468800844435456/pngwing.com_1.png")
        elif weather == '실 비':
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/970965273001742349/973468696146223114/pngwing.com.png")
        else:
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/970965273001742349/973468696146223114/pngwing.com.png")
        embed.set_footer(text="자세한 정보는 위의 프로필 버튼의 사이트를 방문해주세요.", icon_url="http://openweathermap.org/img/wn/10d@2x.png")
        await message.channel.send(embed=embed)

#비속어 필터
    _badword = message.content
    for i in badword:
        if i in _badword:
            await message.delete()
            msg = await message.channel.send(f"{message.author.mention} 님이 비속어를 사용하였습니다.")

#메시지 청소
    if message.content.startswith("!청소 "):
            purge_number = message.content.replace("!청소 ", "")
            check_purge_number = purge_number.isdigit()

            if check_purge_number == True:
                await message.channel.purge(limit=int(purge_number) + 1)
                msg = await message.channel.send(f"**{purge_number}개**의 메시지를 삭제했습니다.")
                await asyncio.sleep(2)
                await msg.delete()

            else:
                await message.channel.send("올바른 값을 입력해주세요.")

#타자 연습
    if message.content == "!타자연습":
        def check(m):
            return m.author == message.author and m.channel == message.channel

        sentence = ["가는 날이 장날이다.", "가는 말이 고와야 오는 말이 곱다.",
            "가랑비에 옷 젖는 줄 모른다.", "가재는 게 편이라."]
        await message.channel.send("**타자측정**\n준비 : 1, 취소 : 2")

        try:
            msg = await client.wait_for("message", check=check, timeout=15)

            if msg.content == "1":
                choice = random.choice(sentence)
                await message.channel.send(f"아래의 글을 입력하세요 :\n**{choice}**")
                startTime = time.time()
                try:
                    answer = await client.wait_for("message", check=check, timeout=30)

                    deltaTime = time.time() - startTime
                    accuracy = difflib.SequenceMatcher(None, choice, answer.content).ratio()
                    speed = len(choice) * accuracy * 3 / deltaTime * 60

                    await message.channel.send(f"**타자 : {round(speed)}타\n정확도: {accuracy * 100:0.1f}**")

                except asyncio.exceptions.TimeoutError:
                    await message.channel.send("시간이 초과되었습니다.")

            elif msg.content == "2":
                await message.channel.send("타자측정을 취소합니다.")

            else:
                await message.channel.send("올바른 값을 입력해주세요.")

        except asyncio.exceptions.TimeoutError:
            await message.channel.send("시간이 초과되었습니다.\n**!타자연습**을 입력해 다시 시도")

#코로나 불러오기
    if message.content.startswith("!코로나"):
            res = requests.get("http://ncov.mohw.go.kr").text
            soup = BeautifulSoup(res, "html.parser")

            day_corona = soup.find("table",{"class":"ds_table"}).find("tbody").find("tr").find_all("td")[3].text
            max_corona = soup.find("div",{"class":"occur_num"}).find_all("div",{"class":"box"})[1].text.replace("(누적)","").replace("확진","").replace("다운로드","")
            day_die = soup.find("table",{"class":"ds_table"}).find("tbody").find("tr").find_all("td")[0].text
            max_die = soup.find("div",{"class":"occur_num"}).find_all("div",{"class":"box"})[0].text.replace("(누적)","").replace("사망","")

            embed = discord.Embed(title="코로나 19 현황", description="", color=0xff0000)
            embed.add_field(name="일일 확진자", value = day_corona, inline=True)
            embed.add_field(name="누적 확진자", value = max_corona, inline=True)
            embed.add_field(name="일일 사망자", value = day_die, inline=True)
            embed.add_field(name="누적 사망자", value = max_die, inline=True)
            embed.set_author(name="코로나 바이러스 감염증(COVID-19)", url="http://ncov.mohw.go.kr/", icon_url="https://cdn.discordapp.com/attachments/779326874026377226/789094221533282304/Y5Tg6aur.png")
            embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/779326874026377226/789094221533282304/Y5Tg6aur.png")
            embed.set_footer(text="자세한 정보는 위의 프로필 버튼의 사이트를 방문해주세요.", icon_url="https://cdn.discordapp.com/attachments/779326874026377226/789098688315654164/Flag_of_South_Korea.png")
            await message.channel.send(embed=embed)


client.run(token)