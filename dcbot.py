import discord
from discord.ext import commands
import os

with open("token.txt", "r") as fi:
    my_token = fi.read()

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='/', intents=intents)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="/cal [expression]"))
    print('Bot is online.')


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms.')


@client.command(aliases=["tts", "ts", "tss", "tst"])
async def say(ctx, *, message=""):
    if message == "":
        return
    else:
        memClient = ctx.guild.get_member(678828033305608204)
        selfname = memClient.nick
        await memClient.edit(nick=ctx.author.nick)
        await ctx.send(message, tts=True)
        await memClient.edit(nick=selfname)


@client.command()
async def afk(ctx):
    await ctx.send(f"{ctx.author.mention} is now afk.")


@client.command(aliases=['?'])
async def _help(ctx, cmd=""):
    if cmd == "":
        await ctx.send('Commands available: help, ping, cal\nType /? [command] for more info')
    if cmd == "?":
        await ctx.send('Displays info about a command.\nSyntax: /? [command]\nType /? to display all commands.')
    elif cmd == 'ping':
        await ctx.send('Shows the latency of me. 200-300ms is a normal range.\nSyntax: /ping')
    elif cmd == 'cal':
        await ctx.send('Calculator.\nSyntax: /cal [expression]')
    # print(type(ctx))


@client.command()
async def unload(ctx, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
    except commands.ExtensionNotLoaded:
        await ctx.send(f'{extension} is already unloaded or is not found.')
        return
    await ctx.send(f'Unloaded {extension}.')


@client.command()
async def load(ctx, extension):
    try:
        client.load_extension(f'cogs.{extension}')
    except commands.ExtensionNotFound:
        await ctx.send(f'{extension} is not found.')
        return
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(f'{extension} is already loaded.')
        return
    except:
        await ctx.send(f'The code in {extension} is written badly.')
        return
    await ctx.send(f'Loaded {extension}.')


@client.command()
async def reload(ctx, extension):
    try:
        client.reload_extension(f'cogs.{extension}')
    except commands.ExtensionNotLoaded:
        await load(ctx, extension)
        return
    except commands.ExtensionNotFound:
        await ctx.send(f'{extension} is not found.')
        return
    except:
        await ctx.send(f'The code in {extension} is written badly.')
        return
    await ctx.send(f'Reloaded {extension}.')


for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        if not file == 'chrome.py':
            client.load_extension(f'cogs.{file[:-3]}')

client.run(my_token)
