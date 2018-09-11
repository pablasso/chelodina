import ast

from chelodina.utils import validator


TURTLE_MODULE = "turtle"


def turtle_wrapper(current_ast):
    """
    Returns an AST wrapped with the needed imports and closing statements
    """
    body = [_import(TURTLE_MODULE)] + current_ast
    return ast.Module(body=body)


def _import(name):
    return ast.Import(names=[ast.alias(name=name, asname=None)])


def call(attribute, *args):
    validator.validate_command(attribute)

    def format_args():
        formatted_args = []
        for arg in args:
            if isinstance(arg, float):
                formatted_args.append(number(arg))
            else:
                raise Exception("Unsupported parameter type {0}".format(arg))
        return formatted_args

    args = format_args()
    module = ast.Name(id=TURTLE_MODULE, ctx=ast.Load())
    return ast.Expr(
        value=ast.Call(
            func=ast.Attribute(value=module, attr=attribute, ctx=ast.Load()),
            args=args,
            keywords=[],
        )
    )


def number(value):
    return ast.Num(n=value)
