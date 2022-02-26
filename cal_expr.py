import math
from collections import OrderedDict
from inspect import signature

lastresult = 0

def cale(expr):
    def precedence(op):
        if op == '*' or op == '/' or op == '%':
            return 12
        elif op == '+' or op == '-':
            return 11
        elif op == '(':
            return 0
        return 15

    def mytan(x):
        if x%180 == 90:
            raise ModuleNotFoundError
        return math.tan(math.radians(x))

    def myfact(x):
        if x > 100000:
            raise ModuleNotFoundError
        return math.factorial(x)
        
    def heron(a, b, c):
        s = (a+b+c)/2
        return math.sqrt(s*(s-a)*(s-b)*(s-c))

    ops = OrderedDict([
        ("+", lambda x, y: x + y),
        ("-", lambda x, y: x - y),
        ("/", lambda x, y: x / y),
        ("*", lambda x, y: x * y),
        ("%", lambda x, y: x % y),
        ("^", lambda x, y: x ** y),
        ("sind", lambda x: math.sin(math.radians(x))),
        ("cosd", lambda x: math.cos(math.radians(x))),
        ("tand", mytan),
        ("sin", lambda x: math.sin(x)),
        ("cos", lambda x: math.cos(x)),
        ("tan", lambda x: math.tan(x)),
        ("ln", lambda x: math.log(x)),
        ("logten", lambda x: math.log10(x)),
        ("logtwo", lambda x: math.log2(x)),
        ("log", lambda x, y: math.log(x, y)),
        ("sqrt", lambda x: math.sqrt(x)),
        ("!", myfact),
        ("asind", lambda x: math.degrees(math.asin(x))),
        ("acosd", lambda x: math.degrees(math.acos(x))),
        ("atand", lambda x: math.degrees(math.atan(x))),
        ("asin", lambda x: math.asin(x)),
        ("acos", lambda x: math.acos(x)),
        ("atan", lambda x: math.atan(x)),
        ("exp", lambda x: math.exp(x)), 
        ("inv", lambda x: 1/x), 
        ("C", lambda x, y: math.factorial(x) / math.factorial(y) / math.factorial(x - y)),
        ("P", lambda x, y: math.factorial(x) / math.factorial(x - y)),
        ("coslaw", lambda a, b, C: math.sqrt(a*a + b*b - 2*a*b*ops["cosd"](C))),
        ("heron", heron)
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
        'tau': (math.pi * 2),
        'phi': ((1+math.sqrt(5))/2),
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
            if temp % 1 == 0:
                temp = int(temp)
            if neg:
                temp *= -1
                neg = False
            lastop = False
            lastnum = True
            a.append(temp)
            i += j - 1
        elif expr[i] in ops or expr[i].isalpha():
            isconst = False
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
                    isconst = True
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
            if not isconst:
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
                except ModuleNotFoundError:
                    return f"'{a[0]}' is not defined for {b[-1]}."
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
            if params == 3:
                try:
                    temp = func(b[-3], b[-2], b[-1])
                    print(f'applying {a[0]} at {b[-3]}, {b[-2]}, {b[-1]}')
                except IndexError:
                    return "Missing numbers/ Too many operators"
                b.pop(-1)
                b.pop(-1)
                b[-1] = temp
            a.pop(0)
        else:
            return f"Error type: {type(a[0])}"
    if len(b) == 1:
        ans = b[0]
        try:
            if ans % 1 == 0:
                ans = int(ans)
        except:
            pass
        return ans
    else:
        return "Too many numbers/ Missing operators"


if __name__ == '__main__':
    while True:
        expr = input('Enter an expression: ')
        res = cale(expr)
        if type(res) != str:
            lastresult = res
            print(f'The result is: {res}')
        else:
            print(res)