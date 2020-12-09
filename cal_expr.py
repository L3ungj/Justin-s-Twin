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
        ("sqrt", lambda x:math.sqrt(x)),
        ("!", lambda x: math.factorial(x))
    ])
    a = []
    b = []
    lastop = True
    neg = False
    lastnum = False
    n = len(expr)
    i = 0
    while i < n:
        if expr[i] == ' ':
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
                func = ""
                while i + j < n and expr[i + j].isalpha():
                    func += expr[i + j]
                    j += 1
                if func not in ops:
                    return f"The function '{func}' doesn't exist."
                while len(b) and 15 <= precedence(b[-1]):
                    a.append(b[-1])
                    b.pop(-1)
                b.append(func)
                i += j - 1
            elif lastop and expr[i] == '-':
                neg = True
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
    # return a
    # eval
    while len(a):
        if type(a[0]) is float:
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
                except IndexError:
                    return "Missing numbers/ Too many operators"
                except ValueError:
                    return f"'{a[0]}' is not defined for {b[-1]}."
                b[-1] = temp
            if params == 2:
                try:
                    temp = func(b[-2], b[-1])
                except ZeroDivisionError:
                    return "You can't divide by 0!"
                except IndexError:
                    return "Missing numbers/ Too many operators"
                b.pop(-1)
                b[-1] = temp
            a.pop(0)
    if len(b) == 1:
        return b[0]
    else:
        return "Too many numbers/ Missing operators"
