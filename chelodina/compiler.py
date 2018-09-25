import turtle
import astor

from chelodina.parser import Parser


def get_parser():
    return Parser()


def get_ast(code):
    return get_parser().parse(code)


def get_source(code):
    parsed_ast = get_ast(code)
    return astor.to_source(parsed_ast)


def run(code):
    parsed_ast = get_ast(code)
    compiled = compile(parsed_ast, filename="<ast>", mode="exec")
    namespace = {}
    try:
        exec(compiled, namespace)
    except (KeyboardInterrupt, turtle.Terminator):
        print("\nChelodina finished. Goodbye.")
