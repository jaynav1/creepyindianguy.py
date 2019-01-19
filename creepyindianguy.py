import discord
import discord.game
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import time
from itertools import cycle

Client = discord.Client()
client = commands.Bot(command_prefix = "bob.")
client.remove_command('help')

status = [' bitch lasagna', ' bob.help for help', ' Roblox']

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

#Log messages internally (in console)
@client.event
async def on_message(message):
    print(f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    await client.process_commands(message)

    if message.content.lower() == "indianguy.logout":
        await client.close()


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

#We don't really need this on-delete functionality if we have logger, unless we can replace it. Still useful in general.
#@client.event
# sync def on_message_delete(message):
    #await client.send_message(message.channel, f"{message.channel}: {message.author}: {message.author.name}: {message.content}")
    #await client.process_commands(message)

#MISSING PERMISSIONS ERROR @client.event
#async def on_member_join(member):
    #role = discord.utils.get(member.server.roles, name='W1GG3R5')
    #await client.add_roles(member, role)

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
    embed.add_field(name='Functionality', value='bob.clear', inline=False)
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

#For the status cycler
client.loop.create_task(change_status())

#Bot's token
client.run("NTMxMDQ1ODcxNDUwNzE4MjA5.DyCTow.LRGTi9OizIe1E0STFRCFmrOSJV0")
