import discord
from discord.ext import commands
import os
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome('C:\\Users\\justi\\Documents\\chromedriver')
driver.get("https://www.wolframalpha.com")
driver.execute_script("window.open('https://web.whatsapp.com');")
wait = WebDriverWait(driver, 10)

client = commands.Bot(command_prefix='/')
lastresult = 0
def cale(expr):
    def precedence(op):
        if op == '*' or op == '/':
            return 12
        elif op == '+' or op == '-':
            return 11
        elif op == '(':
            return 0
        return 15

    from collections import OrderedDict
    import math
    from inspect import signature
    ops = OrderedDict([
        ("+", lambda x, y: x + y),
        ("-", lambda x, y: x - y),
        ("/", lambda x, y: x / y),
        ("*", lambda x, y: x * y),
        ("^", lambda x, y: x ** y),
        ("sin", lambda x: math.sin(math.radians(x))),
        ("cos", lambda x: math.cos(math.radians(x))),
        ("tan", lambda x: math.tan(math.radians(x))),
        ("ln", lambda x: math.log(x)),
        ("sqrt", lambda x: math.sqrt(x)),
        ("!", lambda x: math.factorial(x)),
        ("asin", lambda x: math.degrees(math.asin(x))),
        ("acos", lambda x: math.degrees(math.acos(x))),
        ("atan", lambda x: math.degrees(math.atan(x))),
        ("exp", lambda x: math.exp(x)),
        ("C", lambda x, y: math.factorial(x)/math.factorial(y)/math.factorial(x-y))
    ])
    a = []
    b = []
    lastop = True
    neg = False
    lastnum = False
    n = len(expr)
    i = 0
    constants = {
        'e': math.e,
        'pi': math.pi,
        'ans': lastresult
    }
    while i < n:
        if expr[i] == ' ' or expr[i] == ',':
            i += 1
            continue
        elif expr[i].isdigit() or expr[i] == '.':
            j = 0
            temp = ""
            while i + j < n and expr[i + j].isdigit():
                temp += expr[i + j]
                j += 1
            if i + j < n and expr[i + j] == '.':
                i += j
                j = 1
                temp += '.'
                while i + j < n and expr[i + j].isdigit():
                    temp += expr[i + j]
                    j += 1
            temp = float(temp)
            if neg:
                temp *= -1
                neg = False
            lastop = False
            lastnum = True
            a.append(temp)
            i += j - 1
        elif expr[i] in ops or expr[i].isalpha():
            if expr[i].isalpha():
                j = 0
                func: str = ""
                while i + j < n and expr[i + j].isalpha():
                    func += expr[i + j]
                    j += 1
                if func in ops:
                    while len(b) and 15 <= precedence(b[-1]):
                        a.append(b[-1])
                        b.pop(-1)
                    b.append(func)
                elif func in constants:
                    temp = constants[func]
                    if neg:
                        temp *= -1
                        neg = False
                    if lastnum:
                        b.append('*')
                    a.append(temp)
                    lastop = False
                    lastnum = True
                else:
                    return f"The function or constant '{func}' doesn't exist."
                i += j - 1
            elif lastop and expr[i] == '-':
                neg = not neg
                i += 1
                continue
            elif len(b) == 0 or precedence(expr[i]) > precedence(b[-1]):
                b.append(expr[i])
            else:
                while len(b) and precedence(expr[i]) <= precedence(b[-1]):
                    a.append(b[-1])
                    b.pop(-1)
                b.append(expr[i])
            lastop = True
            lastnum = False
            if expr[i] == '!':
                lastop = False
                lastnum = True
        elif expr[i] == '(':
            if lastnum:
                b.append('*')
            b.append('(')
            lastnum = False
            lastop = True
        elif expr[i] == ')':
            while len(b) and b[-1] != '(':
                a.append(b[-1])
                b.pop(-1)
            if len(b) == 0:
                return "Missing '('"
            b.pop(-1)
            lastnum = True
        else:
            return 'Unknown character: %s' % (expr[i])
        i += 1
    while len(b):
        a.append(b[-1])
        b.pop(-1)
    # eval
    print(a)
    while len(a):
        if type(a[0]) is float or type(a[0]) is int:
            b.append(a[0])
            a.pop(0)
        elif type(a[0]) is str:
            if a[0] == '(':
                return "Missing ')'"
            func = ops[a[0]]
            params = len(signature(func).parameters)
            if params == 1:
                try:
                    temp = func(b[-1])
                    print(f'applying {a[0]} at {b[-1]}')
                except IndexError:
                    return "Missing numbers/ Too many operators"
                except ValueError:
                    return f"'{a[0]}' is not defined for {b[-1]}."
                b[-1] = temp
            if params == 2:
                try:
                    temp = func(b[-2], b[-1])
                    print(f'applying {a[0]} at {b[-2]}, {b[-1]}')
                except ZeroDivisionError:
                    return "You can't divide by 0!"
                except IndexError:
                    return "Missing numbers/ Too many operators"
                b.pop(-1)
                b[-1] = temp
            a.pop(0)
        else:
            return f"Error type: {type(a[0])}"
    if len(b) == 1:
        ans = b[0]
        if ans % 1 == 0:
            ans = int(ans)
        return ans
    else:
        return "Too many numbers/ Missing operators"

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


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="/cal [expression]"))
    print('Bot is online.')

@client.command(aliases=['cs'])
async def changestatus(ctx, *, status=""):
    if status == "":
        return
    if status == "reset":
        status = "/cal [expression]"
    await client.change_presence(activity=discord.Game(name=status))
    await ctx.send(f"Changed status to {status}.")
    

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms.')


@client.command(aliases=["tts","ts","tss","tst"])
async def say(ctx,*, message=""):
    if message == "":
        return
    else:
        memClient = ctx.guild.get_member(678828033305608204)
        selfname = memClient.nick
        await memClient.edit(nick=ctx.author.nick)
        await ctx.send(message, tts=True)
        await memClient.edit(nick=selfname)

@client.command(aliases=["cn"])
async def changeNick(ctx, member: discord.Member, *, newName):
    await member.edit(nick=newName)
    await ctx.send("Changed")

@client.command()
async def ask(ctx,*, message=""):
    if message == "":
        return
    else:
        await ctx.send(random.choice(ballres))
        
@client.command()
async def con(ctx, member: discord.User):
    if member.id == 403918298116259858:
        await ctx.send("You can't con the creator!")
        return
    await ctx.send(f'{member.mention} is conned by {ctx.author.mention}.')


@client.command()
async def cal(ctx, *, expression=""):
    if expression == "":
        await ctx.send('You must enter an expression!')
        return
    await ctx.send(f'Calculating {expression}...')
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
        await ctx.send(f'The result is {result}.')

@client.command()
async def wtsinit(ctx):
    global driver
    driver.execute_script("window.open('https://web.whatsapp.com');")

@client.command(aliases=['w'])
async def wts(ctx, *,inp):
    driver.switch_to.window(driver.window_handles[1])
    temp = inp.split(',')
    exchange = {'self': 'Handsomes', 'class':'華仁智障集中營'}
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
    
@client.command()
async def wa(ctx, *, expr=""):
    if expr == "":
        await ctx.send('You must enter an expression!')
        return
    driver.switch_to.window(driver.window_handles[0])
    exp_arg = '//input'
    exp_inp = wait.until(EC.presence_of_element_located((By.XPATH, exp_arg)))
    exp_inp.send_keys(expr+Keys.ENTER)
    time.sleep(10)
    for arg in ['Input', 'Input interpretation']:
        try:
            ans_t = driver.find_element_by_xpath(f'//section[header/h2 = "{arg}:"]/div/div/img').get_attribute('alt')
            await ctx.send(f'{arg}:\n{ans_t}')
            break
        except:
            pass
    for arg in ['Solution', 'Solutions', 'Result' , 'Decimal approximation', 'Exact result', 'Definite integral', 'Indefinite integral', 'Derivative', 'Definitions', 'Definition']:
        try:
            ans_t = driver.find_element_by_xpath(f'//section[header/h2 = "{arg}:"]/div/div/img').get_attribute('alt')
            await ctx.send(f'{arg}:\n{ans_t}')
        except:
            pass
    exp_inp = wait.until(EC.presence_of_element_located((By.XPATH, exp_arg)))
    exp_inp.send_keys(Keys.BACKSPACE * len(expr))
    
@client.command()
async def wal(ctx, *, expr=""):
    if expr == "":
        await ctx.send('You must enter an expression!')
        return
    driver.switch_to.window(driver.window_handles[0])
    exp_arg = '//input'
    exp_inp = wait.until(EC.presence_of_element_located((By.XPATH, exp_arg)))
    exp_inp.send_keys(expr+Keys.ENTER)
    time.sleep(10)
    out_t = []
    for out_ele in driver.find_elements_by_xpath('//h2'):
        out_t.append(out_ele.text)
    for arg in out_t:
        ans_t = driver.find_element_by_xpath(f'//section[header/h2 = "{arg}"]/div/div/img').get_attribute('alt')
        await ctx.send(f'{arg}\n{ans_t}')
    #exp_inp = wait.until(EC.presence_of_element_located((By.XPATH, exp_arg)))
    exp_inp.send_keys(Keys.BACKSPACE * len(expr))
    
@client.command(aliases=['?'])
async def _help(ctx, cmd=""):
    if cmd == "":
        await ctx.send('Commands available: help, ping, cal\nType /? [command] for more info')
    if cmd == "?":
        await ctx.send('Displays info about a command.\nSyntax: /? [command]\nType /? to display all commands.')
    elif cmd == 'ping':
        await ctx.send('Shows the latency of me. 200-300ms is a normal range.\nSyntax: /ping')
    elif cmd == 'cal':
        await ctx.send('Calculator.\nSyntax: /cal [expression]')
    #print(type(ctx))


@client.command()
async def unload(ctx, extension):
    try:
        client.unload_extension(extension)
    except commands.ExtensionNotLoaded:
        await ctx.send(f'{extension} is already unloaded or is not found.')
        return
    await ctx.send(f'Unloaded {extension}.')


@client.command()
async def load(ctx, extension):
    try:
        client.load_extension(extension)
    except commands.ExtensionNotFound:
        await ctx.send(f'{extension} is not found.')
        return
    except commands.ExtensionAlreadyLoaded:
        await ctx.send(f'{extension} is already loaded.')
        return
    except:
        await ctx.send(f'The code in {extension} is written badly.')
        return
    await ctx.send(f'Loaded {extension}')


@client.command()
async def reload(ctx, extension):
    try:
        client.reload_extension(extension)
    except commands.ExtensionNotLoaded:
        await ctx.send(f'{extension} is not loaded.')
        return
    except commands.ExtensionNotFound:
        await ctx.send(f'{extension} is not found.')
        return
    except:
        await ctx.send(f'The code in {extension} is written badly.')
        return
    await ctx.send(f'Reloaded {extension}')


@client.command()
async def clear(ctx, amount=0):
    if type(amount) != int or amount < 0:
        await ctx.send('Please enter an amount:int that is >0.')
        return
    await ctx.channel.purge(limit=int(amount) + 1)
    await ctx.send(f'Cleared {amount} messages by {ctx.author.name}')

#
# for file in os.listdir('.'):
#     if file.endswith('.py'):
#         if not file == 'dcbot.py':
#             client.load_extension(file[:-3])

client.run('Njc4ODI4MDMzMzA1NjA4MjA0.XkofaA.SnuHPKYUUiEREC8-04ujQf2XGCs')
