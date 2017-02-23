import functools
from string import ascii_lowercase as VALID_LETTERS

COMMON_MISTAKES = {'"': '^',
                   '“': '^',
                   ' ': '',
                   ':': '=',
                   'A': '^',
                   '-+': '+',
                   '¢': '*',
                   'O': '0',
                   '—': '-',
                   "х": "x"}


SYNTAX_MISTAKES = {'^': '**'}

def casefix(text):
    return text.casefold()

def replace_many(text, iterable):
    for first, second in iterable:
        text = text.replace(first, second)
    return text

def fix_mistakes_base(text, mistakes):
    return replace_many(text, mistakes.items())

fix_common_mistakes = functools.partial(fix_mistakes_base,
                                        mistakes=COMMON_MISTAKES)

fix_syntax_mistakes = functools.partial(fix_mistakes_base,
                                        mistakes=SYNTAX_MISTAKES)


def find_variables(text):
    variables = []
    for letter in text:
        if letter in VALID_LETTERS and letter not in variables:
            variables.append(letter)
    return variables
