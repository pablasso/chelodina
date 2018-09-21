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

    def p_program(self, p):
        """program : statements"""
        p[0] = p[1]

    def p_statements(self, p):
        """statements : statements statement
                      | statement """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        """statement : expression
                     | funcdef"""
        p[0] = p[1]

    def p_expression(self, p):
        """expression : NAME NUMBER
                      | NAME"""
        if len(p) == 3:
            p[0] = ast_builder.call(p[1], p[2])
        else:
            p[0] = ast_builder.call(p[1])

    def p_funcdef(self, p):
        """funcdef : TO NAME statements END"""
        name = p[2]
        body = p[3]
        p[0] = ast_builder.funcdef(name, body)

    def p_error(self, p):
        if p:
            print("Syntax error at: {0}".format(p))
        else:
            print("Syntax error at EOF")
