import ast


TURTLE_MODULE = "turtle"


def turtle_wrapper(current_ast):
    """
    Returns an AST wrapped with the needed imports and closing statements
    """
    body = [_import(TURTLE_MODULE)] + current_ast
    return ast.Module(body=body)


def _import(name):
    return ast.Import(names=[ast.alias(name=name, asname=None)])


def call(attribute, parameters):
    module = ast.Name(id=TURTLE_MODULE, ctx=ast.Load())
    return ast.Expr(
        value=ast.Call(
            func=ast.Attribute(value=module, attr=attribute, ctx=ast.Load()),
            args=parameters,
            keywords=[],
        )
    )


def number(value):
    return ast.Num(n=value)