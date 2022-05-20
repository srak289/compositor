import pyfiglet as ff
from re import compile

__all__ = []

emptyline = compile(r'^\s+$')

styles = dict(
    none = '',
    bold = '\x1b[1m',
    faded = '\x1b[2m', # buggy first char?
    italics = '\x1b[3m',
    underlined = '\x1b[4m',
    blinking = '\x1b[5m',
    reverse_video = '\x1b[7m',
)

fgcolors = dict(
    none = '',
    black = '\x1b[30m',
    red = '\x1b[31m',
    green = '\x1b[32m',
    brown = '\x1b[33m',
    blue = '\x1b[34m',
    purple = '\x1b[35m',
    cyan = '\x1b[36m',
    white = '\x1b[37m'
)

bgcolors = dict(
    none = '',
    black = '\x1b[40m',
    red = '\x1b[41m',
    green = '\x1b[42m',
    brown = '\x1b[43m',
    blue = '\x1b[44m',
    purple = '\x1b[45m',
    cyan = '\x1b[46m',
    white = '\x1b[47m'
)

cancel = '\x1b[0m'

def stripper(s):
    s = '\n'.join([ x for x in s.split('\n') if not emptyline.match(x) ])
    return s

def splitter(s):
    lines = []
    index = 0
    for i,line in enumerate(s.split('\n')):
        if i % 11 == 0 and i > 0:
            index += 1
        try:
            lines[index] += (line+'\n')
        except IndexError:
            lines.append(line+'\n')
    return lines

def colorizer(line, **kwargs):
    s = ''
    if 'fgcolor' in kwargs:
        s += fgcolors[kwargs['fgcolor']]
    if 'bgcolor' in kwargs:
        s += bgcolors[kwargs['bgcolor']]
    if 'style' in kwargs:
        s += styles[kwargs['style']]

    # what's with all the trailing whitespace...

    s += line
    s += cancel

    return s

def compositor(*args):
    def append(i, lines, line, c):
        lines[i].append(colorizer(line, **c))

    lineout = []
    for a,c in args:
        for i,line in enumerate(a.split('\n')):
            try:
                append(i, lineout, line, c)
            except IndexError:
                lineout.append([])
                append(i, lineout, line, c)

    compost = ''
    for x in lineout:
        for y in x:
            compost += y
        compost += '\n'

    return compost

if __name__ == '__main__':

    figroman = lambda x: ff.figlet_format(x, font='roman')

    screen = compositor(
        *[ (figroman(x), dict(fgcolor='purple')) for x in 'FOO' ],
        (figroman('BAR'), dict(fgcolor='red',style='blinking')),
        *[ (figroman(x), dict(fgcolor='purple')) for x in 'BAZ' ]
    )

    print(screen)
