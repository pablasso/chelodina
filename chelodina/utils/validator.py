commands = {
    # TODO: missing motion commands [setxy, home, arc]
    "forward": True,
    "fd": True,
    "back": True,
    "bk": True,
    "left": True,
    "right": True,
    "setpos": True,
    "setx": True,
    "sety": True,
    "setheading": True,
    "seth": True,
}


def validate_command(command):
    if command not in commands:
        raise Exception("command <{0}> not supported".format(command))
