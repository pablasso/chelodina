motion_commands = {
    # TODO: missing motion commands [setxy, arc]
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
    "home": True,
}

screen_commands = {"done": True, "clear": True, "clearscreen": True}

commands = {**motion_commands, **screen_commands}


def validate_command(command):
    if command not in commands:
        raise Exception("command <{0}> not supported".format(command))
