motion_functions = {
    # TODO: missing motion commands [setxy, arc]
    "forward",
    "fd",
    "back",
    "bk",
    "left",
    "right",
    "setpos",
    "setx",
    "sety",
    "setheading",
    "seth",
    "home",
}

screen_functions = {"done", "clear", "clearscreen"}

std_functions = motion_functions.union(screen_functions)


def validate_statements(statements, extras=set()):
    supported_statements = std_functions.union(extras)
    for statement in statements:
        if statement not in supported_statements:
            raise Exception("Statement not supported: {0}".format(statement))


def is_std_function(name):
    return name in std_functions
