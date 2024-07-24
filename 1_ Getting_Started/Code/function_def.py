print("Hello")


def greet():  # -param, -return
    print('Good afternoon')
    print('How are you?')


greet()
print("I hope you're fine")

print("max('HELLO WORLD'):", max('HELLO WORLD'))
print("max('Hello World'):", max('Hello World'))
print("min('Hello World'):", min('Hello World'))

# same name diff func sign


def greet(lang):  # +param, -return #same name
    if lang == "es":  # single quote, double quote no diff
        print('Hola')
    elif lang == 'fr':
        print('Bonjour')
    else:
        print('Hello')


greet('es')  # no enter after func def

# def greet(lang):
# IndentationError
# print(greet('es'))

# same name same func sign


def greet(lang):  # +param, -return #same name
    lang = lang


print(greet('es'))  # output: None, null of python
greet('es')  # does nothing
print(greet('es'))

# same name diff func sign


def greet(lang):  # +param, +return #same name
    name = input("What's your name?\nInput: ")
    if lang == "es":
        return 'Hola '+name
    elif lang == 'fr':
        return 'Bonjour '+name
    else:
        return 'Hello '+name
    print("won't run")  # after return statement


print(greet('es'))
greet('en')  # no print = no output

# same name same func sign


def greet(lang):  # +param, +return #same name
    greet = ""  # var name = func name
    if lang == "es":
        greet = 'Hola'
    elif lang == 'fr':
        greet = 'Bonjour'
    else:
        greet = 'Hello'
    name = input("What's your name?\nInput: ")
    return greet+" "+name


print(greet('fr'))
# print(greet())  # TypeError: requires param lang


def addTwo(a, b):
    return a + b


res = addTwo(3, 5)
print(res)
