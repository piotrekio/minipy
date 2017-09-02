import string


__all__ = ['has', 'get']


ALPHABET = string.ascii_letters


substitutes = dict()
reserved = set()


def next_name():
    for letter in ALPHABET:
        if letter not in reserved:
            reserved.add(letter)
            return letter
    raise Exception('I ran out of names! :(')

def get(name):
    sub = substitutes.get(name)
    if sub is None:
        sub = next_name()
        substitutes[name] = sub
    return sub

def has(name):
    return name in substitutes

