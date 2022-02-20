import discord
from discord.ext import commands
import datetime
import json

CURYEAR: int = 2021
FILENAME = "events.json"

class Events(commands.Cog):
    def __init__(self, cli):
        self.client = cli

    @commands.command(aliases=['ae'])
    async def addevent(self, ctx, indate="", *, namedesc=""):
        gid = str(ctx.guild.id)
        datelist = indate.split('/')
        d, m, y = 0, 0, 0
        if len(datelist) < 2:
            await ctx.send('Please enter a day and month.')
            return
        elif len(datelist) == 2:
            d, m, y = int(datelist[0]), int(datelist[1]), CURYEAR
        elif len(datelist) == 3:
            d, m, y = int(datelist[0]), int(datelist[1]), int(datelist[2])
        else:
            await ctx.send('Invalid date.')
            return
        if namedesc == "":
            await ctx.send('You must enter an event name.')
            return
        eventdate = datetime.date(y, m, d)
        with open(FILENAME) as fi:
            eventdict = json.load(fi)
            if gid not in eventdict:
                eventdict[gid] = {}
            if str(eventdate) not in eventdict[gid]:
                eventdict[gid][str(eventdate)] = []
            eventdict[gid][str(eventdate)].append(namedesc)
            with open(FILENAME, 'w') as fo:
                json.dump(eventdict, fo, indent=2)
        await ctx.send(f'Added event on {eventdate.strftime("%a, %d/%m/%y")}, {namedesc}')

    @commands.command(aliases=['se', 'el', 'eventlist'])
    async def showevents(self, ctx):
        gid = str(ctx.guild.id)
        na = f"Event list of {self.client.get_guild(int(gid)).name}"
        desc = ""
        with open(FILENAME) as fi:
            eventdict = json.load(fi)
            eventdates = list(eventdict[gid].keys())
            eventdates.sort()
            today = str(datetime.date.today())
            for date in eventdates:
                if date < today:
                    eventdict[gid].pop(date)
            for date in eventdates:
                if date in eventdict[gid]:
                    desc += f'{datetime.date.fromisoformat(date).strftime("%a, %d/%m/%y")}:\n'
                    for nade in eventdict[gid][date]:
                        desc += f'  {nade}\n'
                desc += '\n'
            with open(FILENAME, 'w') as fo:
                json.dump(eventdict, fo, indent=2)
        emb = discord.Embed(title=na, description=desc)
        await ctx.send(embed=emb)






def setup(client):
    client.add_cog(Events(client))
