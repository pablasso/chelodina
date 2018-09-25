import ast


STD_FUNCTIONS = {
    # motion
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
    # screen
    "done",
    "clear",
    "clearscreen",
}

PARAMETER_TYPES_ALLOWED = {ast.Num, ast.Name, ast.arg, ast.BinOp}


def validate_statements(statements, extras=set()):
    supported_statements = STD_FUNCTIONS.union(extras)
    for statement in statements:
        if statement not in supported_statements:
            raise Exception("Statement not supported: {0}".format(statement))


def validate_parameter_types(parameters):
    for parameter in parameters:
        if type(parameter) not in PARAMETER_TYPES_ALLOWED:
            raise Exception("Parameter type not supported: {0}".format(parameter))


def is_std_function(name):
    return name in STD_FUNCTIONS
