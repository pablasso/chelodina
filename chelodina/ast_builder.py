import ast


TURTLE_MODULE = "turtle"
LOGO_PARAMETER_PREFIX = ":"
PARAMETER_PREFIX_REPLACEMENT = "p_"


def _sanitize_var(name):
    """
    Logo function parameters start with colon, this prefixes them instead
    """
    return name.replace(LOGO_PARAMETER_PREFIX, PARAMETER_PREFIX_REPLACEMENT)


def _import(name):
    return ast.Import(names=[ast.alias(name=name, asname=None)])


def turtle_wrapper(current_ast):
    """
    Returns an AST wrapped with the needed imports and closing statements
    """
    done = call("done", TURTLE_MODULE)
    body = [_import(TURTLE_MODULE)] + current_ast + [done]
    return ast.Module(body=body)


def funcdef(name, parameters, body):
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
    def format_args():
        formatted_args = []
        # TODO: replace this with a validation as the formatting is now done in the parser
        for parameter in parameters:
            if isinstance(parameter, ast.Num):
                formatted_args.append(parameter)
            elif isinstance(parameter, ast.arg):
                formatted_args.append(parameter)
            else:
                raise Exception("Unsupported parameter type {0}".format(parameter))
        return formatted_args

    def function_expression():
        if module_name:
            module = ast_name(module_name)
            function_attr = ast.Attribute(value=module, attr=attribute, ctx=ast.Load())
        else:
            function_attr = ast_name(attribute)
        return function_attr

    parameters = format_args()
    function_attr = function_expression()
    return ast.Expr(value=ast.Call(func=function_attr, args=parameters, keywords=[]))


def ast_name(name):
    name = _sanitize_var(name)
    return ast.Name(id=name, ctx=ast.Load())


def number(value):
    return ast.Num(n=value)


def arg(name):
    name = _sanitize_var(name)
    return ast.arg(arg=name, annotation=None)
