import discord
from discord.ext import commands
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import asyncio

driver = webdriver.Chrome('C:\\Users\\justi\\Documents\\chromedriver')
wait = WebDriverWait(driver, 10)
SLEEP_TIME = 7


def transform(s):
    news = ""
    for c in s:
        if c.isalnum():
            news += c
        elif c == '.':
            news += c
        elif c == ' ':
            news += '+'
        else:
            news += '%' + hex(ord(c))[2:]
    return news


class Chrome(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def wa(self, ctx, *, expr=""):
        if expr == "":
            await ctx.send('You must enter an expression!')
            return
        driver.switch_to.window(driver.window_handles[0])
        driver.get('https://www.wolframalpha.com/input/?i=' + transform(expr))
        await asyncio.sleep(SLEEP_TIME)
        for arg in ['Input', 'Input interpretation']:
            try:
                ans_t = driver.find_element_by_xpath(f'//section[header/h2 = "{arg}:"]/div/div/img')
            except NoSuchElementException:
                continue
            emb = discord.Embed(title=arg, description=ans_t.get_attribute('alt'))
            emb.set_image(url=ans_t.get_attribute('src'))
            await ctx.send(embed=emb)
        for arg in ['Solution', 'Solutions', 'Result', 'Results', 'Decimal approximation', 'Exact result',
                    'Definite integral', 'Indefinite integral', 'Derivative', 'Definitions', 'Definition', 'Limit',
                    'Plot', 'Plots']:
            try:
                ans_t = driver.find_element_by_xpath(f'//section[header/h2 = "{arg}:"]/div/div/img')
            except NoSuchElementException:
                continue
            emb = discord.Embed(title=arg, description=ans_t.get_attribute('alt'))
            emb.set_image(url=ans_t.get_attribute('src'))
            await ctx.send(embed=emb)

    # @commands.command()
    # async def wal(self, ctx, *, expr=""):
    #     if expr == "":
    #         await ctx.send('You must enter an expression!')
    #         return
    #     driver.switch_to.window(driver.window_handles[0])
    #     driver.get('https://www.wolframalpha.com/input/?i=' + transform(expr))
    #     await asyncio.sleep(SLEEP_TIME)
    #     out_t = []
    #     for out_ele in driver.find_elements_by_xpath('//h2'):
    #         out_t.append(out_ele.text)
    #     print(out_t)
    #     f = True
    #     emb = discord.Embed()
    #     for arg in out_t:
    #         try:
    #             ans_t = driver.find_element_by_xpath(f'//section[header/h2 = "{arg}"]/div/div/img').get_attribute('alt')
    #         except NoSuchElementException:
    #             continue
    #         if f:
    #             emb.title = arg
    #             emb.description = ans_t
    #             f = False
    #         else:
    #             emb.add_field(name=arg, value=ans_t, inline=False)
    #     await ctx.send(embed=emb)

    @commands.command()
    async def wal(self, ctx, *, expr=""):
        if expr == "":
            await ctx.send('You must enter an expression!')
            return
        driver.switch_to.window(driver.window_handles[0])
        driver.get('https://www.wolframalpha.com/input/?i=' + transform(expr))
        await asyncio.sleep(SLEEP_TIME)
        out_t = []
        for out_ele in driver.find_elements_by_xpath('//h2'):
            out_t.append(out_ele.text)
        print(out_t)
        f = True
        for arg in out_t:
            try:
                ans_t = driver.find_element_by_xpath(f'//section[header/h2 = "{arg}"]/div/div/img')
            except NoSuchElementException:
                continue
            emb = discord.Embed(title=arg, description=ans_t.get_attribute('alt'))
            emb.set_image(url=ans_t.get_attribute('src'))
            await ctx.send(embed=emb)


    @commands.command(aliases=['w'])
    async def wts(self, ctx, *, inp):
        driver.switch_to.window(driver.window_handles[1])
        temp = inp.split(',')
        exchange = {'self': 'Handsomes', 'class': '華仁智障集中營'}
        target = temp[0]
        message = temp[1]
        if target in exchange: target = exchange[target]
        x_arg = '//div[@class="_3FRCZ copyable-text selectable-text"]'
        title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
        title.click()
        title.send_keys(target)
        se_arg = f'//span[@title="{target}"]'
        se_con = wait.until(EC.presence_of_element_located((By.XPATH, se_arg)))
        se_con.click()
        inp_xpath = '//div[@class="_3FRCZ copyable-text selectable-text"][@spellcheck="true"]'
        input_box = wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))
        input_box.send_keys(message + Keys.ENTER)
        await ctx.send(f'sent {message} to {target}')


def setup(client):
    client.add_cog(Chrome(client))
    driver.get("https://www.wolframalpha.com")
    driver.execute_script("window.open('https://web.whatsapp.com');")


def teardown(client):
    driver.quit()
