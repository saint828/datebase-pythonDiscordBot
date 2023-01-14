import discord
import os
from dotenv import load_dotenv
import sqlite3
import datetime
from func import download_image_class

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def search(name,guildid):
    con=sqlite3.connect("charaDB.db")
    result = con.execute("SELECT * FROM chara where name=? and guildID=?;",(name,guildid))
    for row in result:
        return row
    return 0
def searchLike(name,guildid):
    con=sqlite3.connect("charaDB.db")
    result = con.execute("SELECT * FROM chara where name like ? and guildID=?;",("%"+name+"%",guildid))
    return result

def searchDelete(name,guildid,authorid):
    con=sqlite3.connect("charaDB.db")
    try:
       con.execute("DELETE FROM chara where name=? and guildID=? and autorID=? ;",(name,guildid,authorid))
    except sqlite3.IntegrityError:
        con.rollback()
    finally:
        con.commit()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith("/delill "):
        msg=message.content.split(" ")
        searchDelete(msg[1],message.guild.id,message.author.id)
    if message.content.startswith("/delill　"):
        msg=message.content.split("　")
        searchDelete(msg[1],message.guild.id,message.author.id)
    if message.content.startswith("/serill "):
        msg=message.content.split(" ")
        print(msg[1])
        result=searchLike(msg[1],message.guild.id)
        if result!=0:
            for row in result:
                await message.channel.send(row[0])
    if message.content.startswith("/serill　"):
        msg=message.content.split("　")
        print(msg[1])
        result=searchLike(msg[1],message.guild.id)
        if result!=0:
            for row in result:
                await message.channel.send(row[0])
    if message.content.startswith("/ill "):
        msg=message.content.split(" ")
        print(msg[1])
        result=search(msg[1],message.guild.id)
        if result!=0:
          filepass=result[3]
          await message.channel.send(file=discord.File(filepass))
    if message.content.startswith("/ill　"):
        msg=message.content.split("　")
        result=search(msg[1],message.guild.id)
        if result!=0:
          filepass=result[3]
          await message.channel.send(file=discord.File(filepass))
    if message.content.startswith("/addill "):
        msg=message.content.split(" ")
        result=search(msg[1],message.guild.id)
        if result==0:
            date = datetime.datetime.now()
            con=sqlite3.connect("charaDB.db")
            filepass="img/"+date.strftime("%Y%m%d%H%M%S") + ".png"
            try:
                con.execute("INSERT INTO chara VALUES (?, ?, ? ,?)",(msg[1],message.guild.id,message.author.id,filepass))
            except sqlite3.IntegrityError:
                con.rollback()
            finally:
                con.commit()
                download_image_class(message,filepass)
        else:
            await message.channel.send("その名前は既に登録されています。")
    if message.content.startswith("/addill　"):
        msg=message.content.split("　")
        result=search(msg[1],message.guild.id)
        if result==0:
            date = datetime.datetime.now()
            con=sqlite3.connect("charaDB.db")
            filepass="img/"+date.strftime("%Y%m%d%H%M%S") + ".png"
            try:
                con.execute("INSERT INTO chara VALUES (?, ?, ? ,?)",(msg[1],message.guild.id,message.author.id,filepass))
            except sqlite3.IntegrityError:
                con.rollback()
            finally:
                con.commit()
                download_image_class(message,filepass)
        else:
            await message.channel.send("その名前は既に登録されています。")

load_dotenv()
client.run(os.getenv("DISCORD_TOKEN"))