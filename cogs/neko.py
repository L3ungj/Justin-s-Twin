import discord
from discord.ext import commands

import logging
import random
import requests
import datetime
import asyncio

logger = logging.getLogger(__name__)

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
        async def hourly_neko():
            while True:
                delta = datetime.timedelta(hours=1)
                now = datetime.datetime.now()
                next_hour = (now + delta).replace(microsecond=0, second=0, minute=0)
                wait_seconds = (next_hour - now).seconds
                print(wait_seconds)
                await asyncio.sleep(wait_seconds)
                emb = await self.get_neko_embed()
                emb.description = f"It's {next_hour.strftime('%X')} now! Time for your hourly neko."
                channel = cli.get_channel(724821718765404192)
                await channel.send(embed=emb)
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


    

def setup(client):
    client.add_cog(Neko(client))