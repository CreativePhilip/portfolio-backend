import random
import string

from string import printable


def random_text(size=10) -> string:
    return "".join([random.choice(printable) for x in range(size)])
