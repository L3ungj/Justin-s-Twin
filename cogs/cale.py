import discord
from discord.ext import commands
from collections import OrderedDict
import math
from inspect import signature
from cal_expr import cale

def correct(expr:str):
    if expr.count('(') > expr.count(')'):
        expr += ')' * (expr.count('(') - expr.count(')'))
    expr = expr.replace('In', 'ln')
    return expr

class Cale(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def cal(self, ctx, *, expression=""):
        if expression == "":
            await ctx.send('You must enter an expression!')
            return
        new_expr = correct(expression)
        if new_expr != expression:
            expression = new_expr
            await ctx.send(f'Assuming {expression} ,')
        await ctx.send(f'Calculating {expression} ...')
        try:
            result = cale(expression)
        except Exception as inst:
            await ctx.send(f'Error: {inst}')
            return
        if type(result) is str:
            await ctx.send(f'Error: {result}')
        else:
            global lastresult
            lastresult = result
            try:
                await ctx.send(f'The result is {result}.')
            except Exception as inst:
                await ctx.send(f'Error: {inst}')


def setup(client):
    client.add_cog(Cale(client))
