import discord
from discord.ext import commands

import logging
import random
import requests
import datetime
import asyncio
import os
import json

logger = logging.getLogger(__name__)
FILEPATH = 'neko.json'

# copied from wykoj
class NekosBestAPI:
    @staticmethod
    def get_url() -> str:
        try:
            url = "https://nekos.best/api/v2/" + random.choice(["waifu", "neko", "kitsune"])
            response = requests.Session().get(url)
        except Exception as e:
            logger.error(
                f"Error in fetching from nekos.best API:\n{e.__class__.__name__}: {str(e)}"
            )
            return "https://nekos.best/api/v2/neko/0378.png"

        data = response.json()
        return data["results"][0]["url"]

class Neko(commands.Cog):
    def __init__(self, cli):
        self.client = cli
        if not os.path.exists(FILEPATH):
            with open(FILEPATH, "w+") as f:
                f.write('[]')
        with open(FILEPATH, "r+") as f:
            self.hourly_neko_channels = json.load(f)
        async def hourly_neko():
            while True:
                delta = datetime.timedelta(hours=1)
                now = datetime.datetime.now()
                next_hour = (now + delta).replace(microsecond=0, second=0, minute=0)
                wait_seconds = (next_hour - now).seconds
                await asyncio.sleep(wait_seconds)
                emb = await self.get_neko_embed()
                emb.description = f"It's {next_hour.strftime('%X')} now! Time for your hourly neko."
                for channel_id in self.hourly_neko_channels:
                    channel = cli.get_channel(channel_id)
                    await channel.send(embed=emb)
                await asyncio.sleep(1.)
        loop=asyncio.get_event_loop()
        asyncio.ensure_future(hourly_neko(), loop=loop)

    async def get_neko_embed(self):
        emb = discord.Embed(
            title='Neko time!',
            description='',)
        emb.set_image(url=NekosBestAPI.get_url())
        return emb

    @commands.command()
    async def neko(self, ctx):
        await ctx.send(embed=await self.get_neko_embed())

    @commands.command()
    async def hourlyneko(self, ctx):
        if ctx.channel.id in self.hourly_neko_channels:
            self.hourly_neko_channels.remove(ctx.channel.id)
            await ctx.send(f"Channel {ctx.channel} are removed from the hourly neko service.")
        else:
            self.hourly_neko_channels.append(ctx.channel.id)
            await ctx.send(f"Channel {ctx.channel} are added in the hourly neko service.")
        with open(FILEPATH, "w") as f:
            json.dump(self.hourly_neko_channels, f, indent=2)

def setup(client):
    client.add_cog(Neko(client))
 