import discord
from discord.ext import commands
import asyncio
import random

ballres = ["As I see it, yes.",
           "Ask again later.",
           "Better not tell you now.",
           "Cannot predict now.",
           "Concentrate and ask again.",
           "Don’t count on it.",
           "It is certain.",
           "It is decidedly so.",
           "Most likely.",
           "My reply is no.",
           "My sources say no.",
           "Outlook not so good.",
           "Outlook good.",
           "Reply hazy, try again.",
           "Signs point to yes.",
           "Very doubtful.",
           "Without a doubt.",
           "Yes.",
           "Yes – definitely.",
           "You may rely on it.",
           ]

get_id = {
    'eri': 636833602964815882,
    'dom': 712563817250291762,
    'hew': 590454138597539840,
    'fra': 592339387283537931,
    'dam': 644423043443064852,
    'jer': 462093413119164437,
    'rya': 403885864075395072,
    'tho': 404472518104317963,
    'ak1': 564383078030639104,
    'ak2': 754971586381217833,
    'luc': 644415652404396032,
    'ada': 403919905310638081,
    'jos': 499139164210462730,
    'spe': 704293644638748692,
    'cle': 321270814467162114,
    'jus': 403918298116259858
}

rm1id = 793904326748799056
rm2id = 793904357716131860


class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['cs'])
    async def changestatus(self, ctx, *, status=""):
        if status == "":
            return
        if status == "reset":
            status = "/cal [expression]"
        await self.client.change_presence(activity=discord.Game(name=status))
        await ctx.send(f"Changed status to {status}.")

    @commands.command(aliases=["cn"])
    async def changenick(self, ctx, member: discord.Member, *, newName=""):
        if newName == "reset":
            newName = None
        elif newName == "":
            await ctx.send("Please enter a name!")
            return
        await member.edit(nick=newName)
        await ctx.send("Changed")

    @commands.command()
    async def ask(self, ctx, *, message=""):
        if message == "":
            return
        else:
            await ctx.send(random.choice(ballres))

    @commands.command()
    async def con(self, ctx, member: discord.User):
        if member.id == 403918298116259858:
            await ctx.send("You can't con the creator!")
            return
        await ctx.send(f'{member.mention} is conned by {ctx.author.mention}.')

    @commands.command()
    async def mention(self, ctx, member: discord.User, times: int):
        if times <= 0:
            await ctx.send('Please enter an integer larger than 0.')
            return
        if times > 10:
            await ctx.send('You are so annoying! max:10')
            times = 10
        for _ in range(times):
            await ctx.send(member.mention)
        # await ctx.send('shut the fuck up!!!')

    @commands.command()
    async def shownames(self, ctx):
        txt = ""
        for name, myid in get_id.items():
            try:
                txt += f'{name}: {ctx.guild.get_member(myid).name}\n'
            except Exception as e:
                txt += f'Unable to find {name}: {myid} in {ctx.guild.id}\n'
                print(e)
        emb = discord.Embed(title='Short names:', description=txt)
        await ctx.send(embed=emb)

    @commands.command()
    async def split(self, ctx, *, msg=""):
        if msg == "":
            await ctx.send('Enter some text!')
            return
        server = ctx.guild
        rm1, rm2 = msg.split(';')
        if rm1.strip() != "":
            for guy in rm1.split(','):
                guy = guy.strip()
                if guy not in get_id:
                    await ctx.send(f'Unknown name: {guy}, /shownames to see names')
                    return
                try:
                    await server.get_member(get_id[guy]).move_to(server.get_channel(rm1id))
                except discord.HTTPException as e:
                    if e.status == 400:
                        await ctx.send(f'Error: {guy} is not connected to voice.')
                except AttributeError:
                    if server.get_member(get_id[guy]) is None:
                        await ctx.send(f'Error: {guy} is not in this server.')
        if rm2.strip() != "":
            for guy in rm2.split(','):
                guy = guy.strip()
                if guy not in get_id:
                    await ctx.send(f'Unknown name: {guy}, /shownames to see names')
                    return
                try:
                    await server.get_member(get_id[guy]).move_to(server.get_channel(rm2id))
                except discord.HTTPException as e:
                    if e.status == 400:
                        await ctx.send(f'Error: {guy} is not connected to voice.')
                except AttributeError:
                    if server.get_member(get_id[guy]) is None:
                        await ctx.send(f'Error: {guy} is not in this server.')

    @commands.command()
    async def moveall(self, ctx, channel: discord.VoiceChannel):
        for mem in ctx.guild.members:
            try:
                await mem.move_to(channel)
            except discord.HTTPException:
                pass

    @commands.command()
    async def deb(self, ctx):
        server = self.client.get_guild(403917475588079617)
        for cha in server.channels:
            if type(cha) is discord.channel.VoiceChannel and len(cha.members) > 0:
                print(f'{cha.name}({[mem.name for mem in cha.members]}): {cha.id}')

    @commands.command()
    async def clear(self, ctx, amount=0, *, args=""):
        if ctx.author.id != 403918298116259858 and ctx.author.id != 403885864075395072:
            await ctx.send('Only Justin the Great can use this command! (to prevent troll)')
            return
        if type(amount) is not int or amount < 0:
            await ctx.send('Please enter an integer that is >0.')
            return
        argdict = {}
        if args != "":
            for arg in args.split(';'):
                arglist = arg.split('=')
                tarlist = arglist[1].split(',')
                argdict[arglist[0]] = tarlist

        def mycheck(m):
            if args == "":
                return True
            for arg, tarlist in argdict.items():
                if arg == "user":
                    for tar in tarlist:
                        tar = tar.strip('<@!> ')
                        if m.author.id == int(tar):
                            return True
                elif arg == "startswith":
                    for tar in tarlist:
                        tar = tar.strip()
                        if m.content.startswith(tar):
                            return True
            return False

        msgs = await ctx.channel.purge(limit=int(amount) + 1, check=mycheck)
        await ctx.send(f'Cleared {len(msgs)} messages by {ctx.author.name}')

    @commands.command(name='r')
    async def repeat(self, ctx, *, text=""):
        print(text)
        if text == "":
            await ctx.send('where text')
            return
        try:
            await asyncio.gather(ctx.send(text), ctx.message.delete())
        except discord.Forbidden:
            pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 695542908538978346:
            await message.channel.send('bio gay')

    @commands.command()
    async def run(self, ctx, *, code=""):
        if code == "":
            await ctx.send('Please enter some code.')
            return
        if ctx.author.id != 403918298116259858:
            await ctx.send('Only Justin the Great can use this command!')
            return
        try:
            exec(code)
        except Exception as e:
            await ctx.send(f'Error: {e}')
            return


def setup(client):
    client.add_cog(Misc(client))
