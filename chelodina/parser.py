import ast
import ply.yacc as yacc

from chelodina.lexer import Lexer


class Parser:
    TURTLE_MODULE = "turtle"
    tokens = Lexer.tokens

    def parse(self, code):
        Lexer().build()
        parser = yacc.yacc(module=self, write_tables=False)

        parsed = parser.parse(code)
        imports = ast.Import(names=[ast.alias(name=self.TURTLE_MODULE, asname=None)])
        parsed = ast.Module(body=[imports] + parsed)
        return parsed

    def p_commands(self, p):
        """commands : commands command
                    | command"""
        if len(p) == 2:
            p[0] = [ast.Expr(value=p[1])]
        else:
            p[0] = [ast.Expr(value=p[1]), ast.Expr(value=p[2])]

    def p_command(self, p):
        "command : COMMAND NUMBER"
        parameters = [ast.Num(n=p[2])]
        function_name = ast.Name(id=self.TURTLE_MODULE, ctx=ast.Load())
        p[0] = ast.Call(
            func=ast.Attribute(value=function_name, attr=p[1], ctx=ast.Load()),
            args=parameters,
            keywords=[],
        )

    def p_error(self, p):
        if p:
            print("Syntax error at: {0}".format(p))
        else:
            print("Syntax error at EOF")
