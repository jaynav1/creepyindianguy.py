import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time

Client = discord.Client()
client = commands.Bot(command_prefix = "bob.")

@client.event
async def on_ready():
    print("Bot is ready for kiss bob!")

@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    mhs_guild = client.get_guild(530704685708083201)

    if "indianguy.logout" == message.content.lower():
        await message.channel.send("'''py\n{0}'''".format(mhs_guild.member_count))

    elif "bob" in message.content.lower():
        await client.send_message(message.channel, "Did somebody say bobs? I'M KISS BOBS!!!")

    elif message.content.lower() == "indianguy.logout":
        await client.close()

#Why doesn't this work? How can I get it to work?
    # elif message.content.lower() == "indianguy.login":
       ## await client.open()

client.run("NTMxMDQ1ODcxNDUwNzE4MjA5.DyCTow.LRGTi9OizIe1E0STFRCFmrOSJV0")

#We need a help function (e.g. ".bob -help")
