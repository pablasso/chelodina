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
    exec(compile(ast, filename="<ast>", mode="exec"))
