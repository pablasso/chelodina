import ast

from chelodina.utils import validator

TURTLE_MODULE = "turtle"
LOGO_PARAMETER_PREFIX = ":"
PARAMETER_PREFIX_REPLACEMENT = "p_"


def _sanitize_var(name):
    """
    Logo function parameters start with colon, this prefixes them instead
    """
    return name.replace(LOGO_PARAMETER_PREFIX, PARAMETER_PREFIX_REPLACEMENT)


# TODO: the parser should be improved to separate [params,numbers] into
# [params_function,params_body,numbers] to avoid doing this
def _sanitize_funcdef_parameters(parameters):
    return [
        arg(parameter.id) for parameter in parameters if isinstance(parameter, ast.Name)
    ]


def _import(name):
    return ast.Import(names=[ast.alias(name=name, asname=None)])


def turtle_wrapper(current_ast):
    """
    Returns an AST wrapped with the needed imports and closing statements
    """
    done = call_expr("done", TURTLE_MODULE)
    body = [_import(TURTLE_MODULE)] + current_ast + [done]
    return ast.Module(body=body)


def fill_locations(current_ast):
    return ast.fix_missing_locations(current_ast)


def funcdef(name, parameters, body):
    parameters = _sanitize_funcdef_parameters(parameters)
    return ast.FunctionDef(
        name=name,
        args=ast.arguments(
            args=parameters,
            vararg=None,
            kwonlyargs=[],
            kw_defaults=[],
            kwarg=None,
            defaults=[],
        ),
        body=body,
        decorator_list=[],
        returns=None,
    )


def call(attribute, module_name="", parameters=[]):
    def function_expression():
        if module_name:
            module = ast_name(module_name)
            function_attr = ast.Attribute(value=module, attr=attribute, ctx=ast.Load())
        else:
            function_attr = ast_name(attribute)
        return function_attr

    validator.validate_parameter_types(parameters)
    function_attr = function_expression()
    return ast.Call(func=function_attr, args=parameters, keywords=[])


def call_expr(attribute, module_name="", parameters=[]):
    return ast.Expr(value=call(attribute, module_name, parameters))


def repeat(times, body):
    times = number(int(times.n)) if isinstance(times, ast.Num) else times
    index = ast_name("_", ast.Store())
    range_call = call("range", "", [times])
    return ast.For(target=index, iter=range_call, body=body, orelse=[])


def ast_name(name, ctx=ast.Load()):
    name = _sanitize_var(name)
    return ast.Name(id=name, ctx=ctx)


def number(value):
    return ast.Num(n=value)


def operator(value):
    if value == "+":
        return ast.Add()
    elif value == "-":
        return ast.Sub()
    elif value == "*":
        return ast.Mult()
    elif value == "/":
        return ast.Div()

    raise Exception("operator not supported: {0}".format(value))


def binary_operation(operator, operand_a, operand_b):
    return ast.BinOp(op=operator, left=operand_a, right=operand_b)


def arg(name):
    name = _sanitize_var(name)
    return ast.arg(arg=name, annotation=None)
