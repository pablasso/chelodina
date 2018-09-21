import ply.yacc as yacc

from chelodina import ast_builder
from chelodina.lexer import Lexer
from chelodina.utils import validator


class Parser:
    tokens = Lexer.tokens
    module = "turtle"

    def __init__(self):
        self.functions = set()
        self.calls = []

    def parse(self, code):
        Lexer().build()
        parser = yacc.yacc(module=self, write_tables=False)
        parsed = parser.parse(code)
        validator.validate_statements(self.calls, self.functions)
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
        name = p[1]
        module = self.module if validator.is_std_function(name) else ""
        self.calls.append(name)
        if len(p) == 3:
            p[0] = ast_builder.call(name, module, p[2])
        else:
            p[0] = ast_builder.call(name, module)

    def p_funcdef(self, p):
        """funcdef : TO NAME statements END"""
        name = p[2]
        body = p[3]
        self.functions.add(name)
        p[0] = ast_builder.funcdef(name, body)

    def p_error(self, p):
        if p:
            print("Syntax error at: {0}".format(p))
        else:
            print("Syntax error at EOF")
