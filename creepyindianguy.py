import discord
import discord.game
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from itertools import cycle
import youtube_dl
import feedparser
import json
import os

Client = discord.Client()
client = commands.Bot(command_prefix = "bob.")
client.remove_command('help')
os.chdir(r'/home/lavie/code/creepyindianguy.py') #NEED THE CORRECT PATH

channelname = '519348806467321858'

#Connected guilds
mhs_guild = client.get_server(519348806467321856)

#For bot's status 
status = [' bitch lasagna', ' bob.help for help', ' Roblox']

#For audio
players = {}
queues = {}

#Actually playing the song that's next on queue
def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id] = player
        player.start()

#Status cycle
async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(20)

#On ready
@client.event
async def on_ready():
    #await client.change_presence(game=discord.Game(name=" bitch lasagna")) #make bitch lasagna the help command
    print("Bot is ready for kiss bob!")

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

#Log messages internally (in console)
@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    await client.process_commands(message)

    if message.content.lower() == "indianguy.logout":
        await client.close()

    with open('users.json', 'r') as f:
        users = json.load(f)
    
    await update_data(users, message.author)
    await add_experience(users, message.author, 5)
    await level_up(users, message.author, message.channel)

    with open('users.json', 'w') as f:
        json.dump(users, f)

    await client.process_commands(message)

#We need a way to allow and disallow reactions by the user (perhaps a command that switches it on and off)

#Log reaction
@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await client.send_message(channel, '{} has added {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))

#Log removal of reaction
@client.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    await client.send_message(channel, '{} has removed {} from the message: {}'.format(user.name, reaction.emoji, reaction.message.content))

'''Level system'''
@client.event
async def on_member_join(member):
    server = member.server
    fmt = 'Welcome {0.mention} to {1.name}!'
    await client.send_message(channelname, fmt.format(member, server.get_channel))

    with open('users.json', 'r') as f:
        users = json.load(f)
    
    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)

async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 1

async def add_experience(users, user, exp):
    users[user.id]['experience'] += exp

async def level_up(users, user, channel):
    experience = users[user.id]['experience']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience ** (1/6))

    if lvl_start < lvl_end:
        await client.send_message(channel, "{} has leveled up to level {} mafia (#that's how the mafia works)".format(user.mention, lvl_end))
        users[user.id]['level'] = lvl_end

#We don't really need this on-delete functionality if we have logger, unless we can replace it. Still useful in general.
@client.event
async def on_message_delete(message):
    await client.send_message(message.channel, f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    await client.process_commands(message)

#MISSING PERMISSIONS ERROR @client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='W1GG3R5')
    await client.add_roles(member, role)

#Help command
@client.command(pass_contenxt=True)
async def help():
    embed = discord.Embed(
        
        description = 'Prefix is bob.',
        colour = discord.Colour.blue()
    )

    embed.set_footer(text='Bobs or vegana?')
    embed.set_image(url='http://www.pmslweb.com/the-blog/wp-content/uploads/2018/03/14-funny-Indian-tech-support-meme.jpg')
    embed.set_author(name='Creepy Indian Guy Commands')
    
    embed.add_field(name='Logout Bot', value='indianguy.logout', inline=False)
    embed.add_field(name='Functionality', value='bob.clear, bob.play, bob.join, bob.leave', inline=False)
    embed.add_field(name='Voice Channels', value='bob.play, bob.join, bob.leave', inline=False)
    embed.add_field(name='Other', value='bob.ping, bob.echo', inline=False)

    await client.say(embed = embed)

#Ping command
@client.command()
async def ping():
    await client.say('Pong!')

#Echo command
@client.command()
async def echo(*args):
    output = ''
    for word in args:
        output += word
        output += ' '
    await client.say(output)
   
#NEW pewdiepie video command
@client.command()
async def pewds():
    Feed = feedparser.parse('https://www.youtube.com/feeds/videos.xml?channel_id=UC-lHJZR3Gqxm24_Vd_AJ5Yw')
    entry = Feed.entries[1]
    output = entry.link
    await client.say(output)

#Clear command
@client.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit=int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
    await client.say('Messages deleted.')

#Joining a voice channel (the user must be logged into a channel (send a message of this and put on help page))
@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

#Leaving a voice channel
@client.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()
    
#Playing YouTube videos
@client.command(pass_context=True)
async def play (ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()

#Pause audio
@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()

#Resume audio
@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()

#Stop audio
@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()

#Song queueing
@client.command(pass_context=True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('Video queued. I hope you send bobs.')

#Member count
@client.command(pass_context=True)
async def member_count():
        await client.say(f"{mhs_guild.member_count}")


#For the status cycler
client.loop.create_task(change_status())

#Bot's token
client.run("NTMxMDQ1ODcxNDUwNzE4MjA5.DyCTow.LRGTi9OizIe1E0STFRCFmrOSJV0")
