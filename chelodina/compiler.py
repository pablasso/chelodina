import astor

from chelodina.parser import Parser


class Compiler:
    def __init__(self):
        self.parser = Parser()

    def get_ast(self, code):
        return self.parser.parse(code)

    def get_source(self, code):
        parsed_ast = self.get_ast(code)
        return astor.to_source(parsed_ast)

    def run(self, code):
        parsed_ast = self.get_ast(code)
        exec(compile(ast, filename="<ast>", mode="exec"))
