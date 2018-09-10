import ply.yacc as yacc

from chelodina import ast_builder
from chelodina.lexer import Lexer


class Parser:
    tokens = Lexer.tokens

    def parse(self, code):
        Lexer().build()
        parser = yacc.yacc(module=self, write_tables=False)
        parsed = parser.parse(code)
        return ast_builder.turtle_wrapper(parsed)

    def p_commands(self, p):
        """commands : commands command
                    | command"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_command(self, p):
        "command : COMMAND NUMBER"
        p[0] = ast_builder.call(p[1], p[2])

    def p_error(self, p):
        if p:
            print("Syntax error at: {0}".format(p))
        else:
            print("Syntax error at EOF")
