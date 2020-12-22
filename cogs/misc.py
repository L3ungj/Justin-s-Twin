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
        if times >10:
            await ctx.send('You are so annoying! max:10')
            times = 10
        for _ in range(times):
            await ctx.send(member.mention)
        # await ctx.send('shut the fuck up!!!')

    # @commands.command()
    # async def clear(self, ctx, amount=0):
    #     if type(amount) != int or amount < 0:
    #         await ctx.send('Please enter an amount:int that is >0.')
    #         return
    #     await ctx.channel.purge(limit=int(amount) + 1)
    #     await ctx.send(f'Cleared {amount} messages by {ctx.author.name}')

    @commands.command(name='r')
    async def repeat(self, ctx, *, text=""):
        if text == "":
            await ctx.send('where text')
            return
        try:
            await asyncio.gather(ctx.send(text), ctx.message.delete())
        except Forbidden:
            pass



def setup(client):
    client.add_cog(Misc(client))
