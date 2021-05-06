import discord
from discord.ext import commands

class Debug(commands.Cog):
    def __init__(self, cli):
        self.client = cli

    @commands.command()
    async def deb(self, ctx):
        server = self.client.get_guild(403917475588079617)
        for cha in server.channels:
            if type(cha) is discord.channel.VoiceChannel and len(cha.members) > 0:
                print(f'{cha.name}({[mem.name for mem in cha.members]}): {cha.id}')

    @commands.command()
    async def link(self, ctx):
        emb = discord.Embed(title='HI', description='[press me](https://discord.gg/A8gzksVt)')
        await ctx.send(embed=emb)

    @commands.command()
    async def oops(self, ctx):
        serv = self.client.get_guild(403917475588079617)
        me = serv.get_member(403918298116259858)
        await me.add_roles(discord.Object(796114400930037790))




def setup(client):
    client.add_cog(Debug(client))
