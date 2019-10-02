import os
import random
import string

allchar = string.ascii_letters + string.digits


def moyo_generator(length):
    return "moyo_" + "".join(random.choice(allchar) for i in range(length))


sylabs = [
    "ko",
    "shi",
    "ri",
    "sho",
    "yo",
    "hi",
    "ha",
    "ra",
    "ri",
    "ori",
    "ya",
    "yi",
    "yo",
    "na",
    "ta",
    "ti",
    "ka",
    "ki",
    "ma",
    "mo",
    "to",
    "li",
]


def moyo_generator_nice(length, sylabs):
    return (
        "moyogatomi-"
        + "".join(random.choice(sylabs).lower() for i in range(length))
        + "-"
        + "".join(random.choice(allchar).lower() for i in range(3))
    )


def manage_nickname(default = None):
    if default:
        return default

    if not os.path.exists("data"):
        os.mkdir("data")
    files = os.listdir("data")
    
    if "nickname.save" in files:
        with open("data/nickname.save", "r") as f:
            nickname = f.read().strip()
        return nickname
    else:
        nickname = moyo_generator_nice(3, sylabs)
        with open("data/nickname.save", "w") as f:
            f.write(nickname)
        return nickname
