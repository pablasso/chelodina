from chelodina.parser import Parser


class Compiler:
    def __init__(self):
        self.parser = Parser()

    def get_ast(self, code):
        return self.parser.parse(code)

    def run(self, code):
        ast = self.get_ast(code)
        exec(
            compile(ast, filename="<ast>", mode="exex")
        )  # TODO: research what else do we need here
