import functools
from string import ascii_lowercase as VALID_LETTERS, digits

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


def fix_exponentation(text):
    text = list(text)
    while True:
        found_var = False
        for i, char in enumerate(text):
            if char in VALID_LETTERS:
                found_var = True
            else:
                if found_var and char in digits:
                    text.insert(i, "**")
                    break
                else:
                    found_var = False
        else:
            break
    text = "".join(text)
    return text
        


def find_variables(text):
    variables = []
    for letter in text:
        if letter in VALID_LETTERS and letter not in variables:
            variables.append(letter)
    return variables
