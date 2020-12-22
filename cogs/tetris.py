import discord
from discord.ext import commands
import random
import asyncio
import copy

LENGTH = 20
WIDTH = 10
DEFAULT_TICK_RATE = 0.2
DEFAULT_TPD = 5 / (DEFAULT_TICK_RATE / 0.2)  # default ticks per down
START_TEXT = "Combinable commands:\n" \
             "'a', 's', 'd': move left, down, right\n" \
             "'q': rotate anti-clockwise, 'e': rotate clockwise\n" \
             "'f': move down all the way\n" \
             "Enter one only:\n" \
             "'p': pause the game\n" \
             "'o': sends a new game message\n" \
             "'end': ends the game"


class vec2:
    def __init__(self, a, b):
        self.x = a
        self.y = b

    def on_screen_y(self):
        return 0 <= self.y < WIDTH

    def on_screen_x(self):
        return 0 <= self.x < LENGTH

    def on_screen(self):
        return self.on_screen_x() and self.on_screen_y()


bc = [
    [[0, 0], [0, 1], [1, 0], [1, 1]],
    [[0, -1], [0, 0], [0, 1], [0, 2]],
    [[0, 0], [0, 1], [1, -1], [1, 0]],
    [[0, -1], [0, 0], [1, 0], [1, 1]],
    [[0, -1], [0, 0], [0, 1], [1, -1]],
    [[0, -1], [0, 0], [0, 1], [1, 1]],
    [[0, -1], [0, 0], [0, 1], [1, 0]]
]

addscore = [40, 100, 300, 1200]

emj = [":white_large_square:", ":yellow_square:", ":blue_square:", ":red_square:", ":green_square:",
       ":brown_square:", ":orange_square:", ":purple_square:"]


class tpiece:
    blocks = [vec2(0, 0)] * 4
    mid = vec2(0, 0)

    def __init__(self, tgamei, ttype):
        if ttype == -1:
            return
        self.ttype = ttype
        avai = []
        self.tgameinst = tgamei
        for i in range(WIDTH):
            mi = vec2(0, i)
            puttable = 1
            for j in range(4):
                vec2t = vec2(mi.x + bc[ttype][j][0], mi.y + bc[ttype][j][1])
                if not vec2t.on_screen_y():
                    puttable = 0
                    break
                if tgamei.getblock(vec2t) != 0:
                    puttable = 0
                    break
            if puttable:
                avai.append(i)
        if len(avai) == 0:
            tgamei.gaming = 0
            return
        self.mid = vec2(0, random.choice(avai))
        for i in range(4):
            self.blocks[i] = vec2(self.mid.x + bc[ttype][i][0], self.mid.y + bc[ttype][i][1])
            self.tgameinst.setblock(self.blocks[i], ttype + 1)

    def movedown(self):
        can = 1
        for xy in self.blocks:
            self.tgameinst.setblock(xy, 0)
        newblocks = copy.deepcopy(self.blocks)
        for i in range(4):
            newblocks[i].x += 1
            if not newblocks[i].on_screen_x():
                can = 0
                break
            if self.tgameinst.getblock(newblocks[i]) != 0:
                can = 0
                break
        if can:
            self.blocks = copy.deepcopy(newblocks)
            self.mid.x += 1
        for xy in self.blocks:
            self.tgameinst.setblock(xy, self.ttype + 1)
        return can

    def moveleft(self):
        can = 1
        for xy in self.blocks:
            self.tgameinst.setblock(xy, 0)
        newblocks = copy.deepcopy(self.blocks)
        for i in range(4):
            newblocks[i].y -= 1
            if not newblocks[i].on_screen_y():
                can = 0
                break
            if self.tgameinst.getblock(newblocks[i]) != 0:
                can = 0
                break
        if can:
            self.blocks = copy.deepcopy(newblocks)
            self.mid.y -= 1
        for xy in self.blocks:
            self.tgameinst.setblock(xy, self.ttype + 1)

    def moveright(self):
        can = 1
        for xy in self.blocks:
            self.tgameinst.setblock(xy, 0)
        newblocks = copy.deepcopy(self.blocks)
        for i in range(4):
            newblocks[i].y += 1
            if not newblocks[i].on_screen_y():
                can = 0
                break
            if self.tgameinst.getblock(newblocks[i]) != 0:
                can = 0
                break
        if can:
            self.blocks = copy.deepcopy(newblocks)
            self.mid.y += 1
        for xy in self.blocks:
            self.tgameinst.setblock(xy, self.ttype + 1)

    def rotate(self):
        if self.ttype == 0:
            return
        can = 1
        for xy in self.blocks:
            self.tgameinst.setblock(xy, 0)
        newblocks = copy.deepcopy(self.blocks)
        for i in range(4):
            dx = self.blocks[i].x - self.mid.x
            dy = self.blocks[i].y - self.mid.y
            newblocks[i] = vec2(self.mid.x + dy, self.mid.y - dx)
            if not newblocks[i].on_screen_y():
                can = 0
                break
            if self.tgameinst.getblock(newblocks[i]) != 0:
                can = 0
                break
        if can:
            self.blocks = copy.deepcopy(newblocks)
        for xy in self.blocks:
            self.tgameinst.setblock(xy, self.ttype + 1)

    def crotate(self):
        if self.ttype == 0:
            return
        can = 1
        for xy in self.blocks:
            self.tgameinst.setblock(xy, 0)
        newblocks = copy.deepcopy(self.blocks)
        for i in range(4):
            dx = self.blocks[i].x - self.mid.x
            dy = self.blocks[i].y - self.mid.y
            newblocks[i] = vec2(self.mid.x - dy, self.mid.y + dx)
            if not newblocks[i].on_screen_y():
                can = 0
                break
            if self.tgameinst.getblock(newblocks[i]) != 0:
                can = 0
                break
        if can:
            self.blocks = copy.deepcopy(newblocks)
        for xy in self.blocks:
            self.tgameinst.setblock(xy, self.ttype + 1)

    def drop(self):
        for xy in self.blocks:
            self.tgameinst.setblock(xy, 0)
        for i in range(1, LENGTH):
            can = 1
            for xy in self.blocks:
                if xy.x + i >= LENGTH:
                    can = 0
                    break
                if self.tgameinst.screen[xy.x + i][xy.y] != 0:
                    can = 0
                    break
            if not can:
                for xy in self.blocks:
                    xy.x += i - 1
                self.mid.x += i - 1
                break
        for xy in self.blocks:
            self.tgameinst.setblock(xy, self.ttype + 1)

    def deb(self):
        for xy in self.blocks:
            print([xy.x, xy.y], end=' ')
        print()


class tgame:
    def __init__(self, level, msg, person):
        self.tpd = DEFAULT_TPD - level  # ticks per down
        self.falling = 0
        self.screen = [[0] * WIDTH for _ in range(LENGTH)]
        self.cur_tpiece = tpiece(self, -1)
        self.ttd = self.tpd  # ticks till down
        self.gaming = 1
        self.msg = msg
        self.userinput = ''
        self.score = 0
        self.level = level
        self.lines = 0
        self.person = person
        self.paused = False
        self.need_draw = False

    async def draw(self):
        descs = []
        desc = ""
        for i in range(10):
            for j in range(WIDTH):
                desc += emj[self.screen[i][j]]
            desc += '\n'
        rem = LENGTH - 10
        cur = 10
        while rem > 0:
            nam, des = "", ""
            for j in range(WIDTH):
                nam += emj[self.screen[cur][j]]
            cur += 1
            rem -= 1
            for i in range(cur, min(cur + 5, LENGTH)):
                for j in range(WIDTH):
                    des += emj[self.screen[i][j]]
                des += '\n'
            descs.append([nam, des])
            cur += 5
            rem -= 5
        ti = 'Tetris'
        if self.paused:
            ti += ' (paused)'
        emb = discord.Embed(title=ti, description=desc)
        emb.set_footer(text=f'Level: {self.level}, Score:{self.score}')
        for nam, des in descs:
            emb.add_field(name=nam, value=des, inline=False)
        await self.msg.edit(embed=emb)

    def logic(self):
        if self.falling:
            if len(self.userinput) > 0:
                self.need_draw = True
            while len(self.userinput):
                c = self.userinput[0]
                if c == 'a':
                    self.cur_tpiece.moveleft()
                elif c == 'd':
                    self.cur_tpiece.moveright()
                elif c == 'q':
                    self.cur_tpiece.crotate()
                elif c == 'e':
                    self.cur_tpiece.rotate()
                elif c == 's':
                    self.cur_tpiece.movedown()
                elif c == 'f':
                    self.cur_tpiece.drop()
                    self.ttd = 1
                self.userinput = self.userinput[1:]
            self.ttd -= 1
            if self.ttd == 0:
                self.need_draw = True
                if not self.cur_tpiece.movedown():
                    self.falling = 0
                    cleared = 0
                    i = LENGTH - 1
                    while i >= 0:
                        full = 1
                        for j in range(WIDTH):
                            if self.screen[i][j] == 0:
                                full = 0
                                break
                        if full:
                            cleared += 1
                            for i_ in range(i, 0, -1):
                                for j_ in range(WIDTH):
                                    self.screen[i_][j_] = self.screen[i_ - 1][j_]
                            for j in range(WIDTH):
                                self.screen[0][j] = 0
                            i += 1
                        if cleared == 4:
                            break
                        i -= 1
                    if cleared > 0:
                        self.score += addscore[cleared - 1] * (self.level + 1)
                    self.lines += cleared
                    if self.lines >= 5:
                        self.lines -= 5
                        self.level += 1
                        self.tpd = max(self.tpd - 1, 1)
                self.ttd = self.tpd
        else:
            self.need_draw = True
            self.cur_tpiece = tpiece(self, random.randint(0, 6))
            self.falling = 1
            self.ttd = self.tpd

    def getblock(self, v2: vec2):
        return self.screen[v2.x][v2.y]

    def setblock(self, v2: vec2, ttype):
        self.screen[v2.x][v2.y] = ttype

    async def refresh(self):
        await self.msg.delete()
        newmsg = await self.msg.channel.send(START_TEXT)
        self.msg = newmsg

    async def start(self):
        while self.gaming:
            if not self.paused:
                if self.need_draw:
                    await self.draw()
                    self.need_draw = False
                self.logic()
            await asyncio.sleep(DEFAULT_TICK_RATE)
        emb = discord.Embed(title='You Lose!', description=f'You died on level {self.level}\nYour score: {self.score}')
        await self.msg.channel.send(embed=emb)
        cur_games.pop(self.person)


cur_games = {}

cmds = ['a', 'f', 's', 'd', 'q', 'e']


class Tetris(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def tetris(self, ctx, level=0):
        if type(level) is not int or (not 0 <= level < DEFAULT_TPD):
            await ctx.send('You can only start at level 0-4!')
            return
        if (ctx.author.id in cur_games and cur_games[ctx.author.id].gaming == 0) or (ctx.author.id not in cur_games):
            msg = await ctx.send(START_TEXT)
            cur_games[ctx.author.id] = tgame(level, msg, ctx.author.id)
            await cur_games[ctx.author.id].start()

    @commands.command()
    async def debug(self, ctx):
        tgamei = tgame(20, ctx.channel, ctx.author.id)
        await tgamei.draw()

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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id in cur_games:
            if message.content == 'p':
                cur_games[message.author.id].paused = not cur_games[message.author.id].paused
                await cur_games[message.author.id].draw()
                await message.delete()
                return
            if message.content == 'o':
                await cur_games[message.author.id].refresh()
                await message.delete()
                return
            if message.content == 'end':
                cur_games[message.author.id].gaming = 0
                await message.delete()
                return
            can = 1
            for c in message.content:
                if c not in cmds:
                    can = 0
                    break
            if can and not cur_games[message.author.id].paused:
                cur_games[message.author.id].userinput += message.content
                await message.delete()


def setup(client):
    client.add_cog(Tetris(client))
