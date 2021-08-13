import discord
import os

def isCodeRight(input_s):
    n_count = 0
    e_count = 0
    for c in input_s:
        if ord('a') <= ord(c.lower()) <= ord('z'):
            e_count+=1
        elif ord('0') <= ord(c.lower()) <= ord('9'):
            n_count+=1
    return True if n_count + e_count == 5 else False

admin_id=os.environ["ADMIN_ID"]
mmlist=os.environ["MMLIST"]
room=os.environ["ROOM"]

client = discord.Client()
guild = discord.Guild

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="-도움"))
    print("Ready")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    elif message.content.startswith('-'):

        cmd = message.content.split()[0].replace("-","")

        if len(message.content.split()) > 1:
            parameters = message.content.split()[1:]

        # if cmd == 'dm':
        #     user = await client.fetch_user(int(parameters[0]))
        #     await user.create_dm()
        #     channel = user.dm_channel
        #     await channel.send("test")
        if cmd == 'mm':
            channel = client.get_channel(mmlist)

            try:
                print(parameters)
                if message.author.id==admin_id:
                    user = await client.fetch_user(int(parameters[0]))
                    name=user.name
                    async for msg in channel.history(limit=None):
                        content = msg.content
                        if content == parameters[0]:
                            await msg.delete()
                            await message.channel.send(name+"님이 mathcmaker에서 제거되었습니다.")
                            return

                    await channel.send(parameters[0])
                    await message.channel.send(name+"님이 matchmaker에 등록되었습니다.")
                    return

                else:
                    await message.channel.send("권한이 없습니다.")
                    return
                    
            except:
                async for msg in channel.history(limit=None):
                    content = msg.content
                    if content == str(message.author.id):
                        await msg.delete()
                        await message.channel.send("mathcmaker에서 제거되었습니다.")
                        return

                await channel.send(message.author.id)
                await message.channel.send("matchmaker에 등록되었습니다.")
                return

        if cmd == '도움':
            embed=discord.Embed(title="도움말", color=0x602dd9)
            embed.add_field(name="-방 생성", value="방을 생성합니다", inline=True)
            embed.add_field(name="-방 삭제", value="방을 삭제합니다", inline=True)
            embed.add_field(name="-방 조회", value="현재 있는 방을 나열합니다", inline=True)
            await message.channel.send(embed=embed)

        if cmd == '방':            
        
            if parameters[0] == '삭제':
                channel = client.get_channel(room)
                        
                
                if len(parameters)>1 and message.author.id==admin_id:
                    async for msg in channel.history(limit=None):
                        sources=msg.content.split("|")
                        if sources[0]==parameters[1]:
                            await msg.delete()
                            await message.channel.send("방을 성공적으로 지웠습니다.")
                            return
                    await message.channel.send("존재하지 않는 방입니다.")

                elif len(parameters)>1:
                    await message.channel.send("권한이 없습니다.")

                else:
                    async for msg in channel.history(limit=None):
                        sources=msg.content.split("|")
                        if sources[3]==str(message.author.id):
                            await msg.delete()
                            await message.channel.send("방을 성공적으로 지웠습니다.")
                            return
                        await message.channel.send("아직 방을 세우지 않았습니다.")

            if parameters[0] == '조회':
                channel = client.get_channel(room)
                isRoom = False
                cnt=0
                # sheet[A(n)] = 방장 닉네임
                # sheet[B(n)] = 코드
                # sheet[C(n)] = 비밀번호
                # sheet[D(n)] = user id(식별용)
                # sheet[E(n)] = user name
                async for msg in channel.history(limit=None):
                    isRoom = True
                    cnt+=1

                    sources=msg.content.split("|")

                    host = sources[0]
                    code = sources[1]
                    pw = sources[2]
                    usr_name=sources[4]

                    embed=discord.Embed(title="Room No."+str(cnt), color=0x602dd9)
                    embed.add_field(name="Host", value=host+"("+usr_name+")", inline=False)
                    embed.add_field(name="Room Code", value=code.upper(), inline=True)
                    embed.add_field(name="Password", value=pw, inline=True)
                      
                    await message.channel.send(embed=embed)

                if(isRoom is False):
                    await message.channel.send("방이 없습니다!")

            if parameters[0] == '생성':

                if len(parameters) < 4:
                    embed=discord.Embed(title="도움말")
                    embed.add_field(name="방 생성 방법", value="-방 생성 인게임id 방코드 비밀번호", inline=True)
                    
                    await message.channel.send(embed=embed)

                else:
                    #print(parameters)
                    if len(parameters[2]) != 5:
                        await message.channel.send("방 코드는 5자리의 숫자/영문으로 이루어져 있어야 합니다.")
                        return
                    
                    if isCodeRight(parameters[2])==False:
                        await message.channel.send("방 코드는 5자리의 숫자/영문으로 이루어져 있어야 합니다.")
                        return
                    elif len(parameters[3])>8:
                        await message.channel.send("비밀번호는 8자리 이하입니다.")
                        return
                    
                    try:
                        int(parameters[3])
                    except:
                        await message.channel.send("비밀번호는 정수여야 합니다.")
                        return
                    
                    
                    else:
                        # sheet[A(n)] = 방장 닉네임
                        # sheet[B(n)] = 코드
                        # sheet[C(n)] = 비밀번호
                        # sheet[D(n)] = user id(식별용)
                        # sheet[E(n)] = user name

                        channel = client.get_channel(room)
                        
                        async for msg in channel.history(limit=None):
                            sources=msg.content.split("|")
                            if sources[0]==parameters[1]:
                                await msg.delete()
                                break
                            if sources[3]==message.author.id:
                                await msg.delete()
                                break
                        content = parameters[1]+"|"+parameters[2]+"|"+parameters[3]+"|"+str(message.author.id)+"|"+message.author.name
                        await channel.send(content)

                        await message.channel.send("방 등록이 완료됐습니다")
                        
                        channel = client.get_channel(mmlist)
                        async for msg in channel.history(limit=None):
                            user = await client.fetch_user(int(msg.content))
                            await user.create_dm()
                            tmpchannel = user.dm_channel
                            await tmpchannel.send(parameters[1]+"님의 방이 생성되었습니다. -방 조회")

access_token=os.environ["BOT_TOKEN"]
client.run(access_token)
