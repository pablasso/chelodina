import ast


TURTLE_MODULE = "turtle"


def turtle_wrapper(current_ast):
    """
    Returns an AST wrapped with the needed imports and closing statements
    """
    done = call("done", TURTLE_MODULE)
    body = [_import(TURTLE_MODULE)] + current_ast + [done]
    return ast.Module(body=body)


def _import(name):
    return ast.Import(names=[ast.alias(name=name, asname=None)])


def funcdef(name, body):
    return ast.FunctionDef(
        name=name,
        args=ast.arguments(
            args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]
        ),
        body=body,
        decorator_list=[],
        returns=None,
    )


def call(attribute, module_name="", *args):
    def format_args():
        formatted_args = []
        for arg in args:
            if isinstance(arg, float):
                formatted_args.append(number(arg))
            else:
                raise Exception("Unsupported parameter type {0}".format(arg))
        return formatted_args

    def function_expression():
        if module_name:
            module = ast.Name(id=module_name, ctx=ast.Load())
            function_attr = ast.Attribute(value=module, attr=attribute, ctx=ast.Load())
        else:
            function_attr = ast.Name(id=attribute, ctx=ast.Load())
        return function_attr

    args = format_args()
    function_attr = function_expression()
    return ast.Expr(value=ast.Call(func=function_attr, args=args, keywords=[]))


def number(value):
    return ast.Num(n=value)
