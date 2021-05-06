import discord
from discord.ext import commands
import json

FILENAME = 'orz.json'


class Orz(commands.Cog):
    def __init__(self, cli):
        self.client = cli

    @commands.command()
    async def orz(self, ctx, guy: discord.Member = None, *, reason="None"):
        memClient = ctx.guild.get_member(678828033305608204)
        selfname = memClient.nick
        if not guy:
            await memClient.edit(nick='᲼')
            await ctx.send('Wow. Ging!!!', tts=True)
            await memClient.edit(nick=selfname)
            return
        gid, pid, aid = map(str, [ctx.guild.id, guy.id, ctx.author.id])
        await memClient.edit(nick='᲼')
        await ctx.send(f'Wow {guy.mention}. Ging!!!\nReason: {reason}', tts=True, allowed_mentions=discord.AllowedMentions.none())
        await memClient.edit(nick=selfname)
        with open(FILENAME, 'r') as fi:
            orzdict = json.load(fi)
            if gid not in orzdict:
                orzdict[gid] = {}
            if pid not in orzdict[gid]:
                orzdict[gid][pid] = [0]
            orzdict[gid][pid][0] += 1
            if reason != "None":
                orzdict[gid][pid].insert(1, [reason, aid])
                if len(orzdict[gid][pid]) == 7:
                    orzdict[gid][pid].pop()
            with open(FILENAME, 'w') as fo:
                json.dump(orzdict, fo, indent=6)

    @commands.command()
    async def orzlist(self, ctx):
        gid = ctx.guild.id
        guild = self.client.get_guild(gid)
        ti = f'orzlist in {guild.name}:'
        de = ''
        with open(FILENAME, 'r+') as fi:
            orzdict = json.load(fi)
            for memid in orzdict[str(gid)]:
                mem = guild.get_member(int(memid))
                de += f'{mem.mention}: {orzdict[str(gid)][memid][0]}\n'
                for reason, author in orzdict[str(gid)][memid][1:]:
                    de += f'  "{reason}" by {guild.get_member(int(author)).mention}\n'
                de += '\n'
        emb = discord.Embed(title=ti, description=de)
        await ctx.send(embed=emb)




def setup(client):
    client.add_cog(Orz(client))
