import discord
import discord.game
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from itertools import cycle

Client = discord.Client()
client = commands.Bot(command_prefix = "bob.")

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name=" bitch lasagna")) #make bitch lasagna the help command
    print("Bot is ready for kiss bob!")

@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    await client.process_commands(message)

    if message.content.lower() == "indianguy.logout":
        await client.close()

#We don't really need this on-delete functionality if we have logger, unless we can replace it. Still useful in general.
#@client.event
# sync def on_message_delete(message):
    #await client.send_message(message.channel, f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    #await client.process_commands(message)

#MISSING PERMISSIONS ERROR @client.event
#async def on_member_join(member):
    #role = discord.utils.get(member.server.roles, name='W1GG3R5')
    #await client.add_roles(member, role)

@client.command()
async def ping():
    await client.say('Pong!')

@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)

@client.command(pass_context=True)
async def clear(ctx, amount=10):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Messages deleted.')



client.run("NTMxMDQ1ODcxNDUwNzE4MjA5.DyCTow.LRGTi9OizIe1E0STFRCFmrOSJV0")
