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
                      | statement"""
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        """statement : expression
                     | funcdef"""
        p[0] = p[1]

    def p_expression(self, p):
        """expression : NAME numbers
                      | NAME"""
        name = p[1]
        module = self.module if validator.is_std_function(name) else ""
        self.calls.append(name)
        if len(p) == 3:
            parameters = p[2]
            p[0] = ast_builder.call(name, module, parameters)
        else:
            p[0] = ast_builder.call(name, module)

    def p_expression_params(self, p):
        """expression : NAME params"""
        name = p[1]
        module = self.module if validator.is_std_function(name) else ""
        parameters = p[2]
        self.calls.append(name)
        p[0] = ast_builder.call(name, module, parameters)

    def p_funcdef(self, p):
        """funcdef : TO NAME params statements END
                   | TO NAME statements END"""
        if len(p) == 5:  # without params
            parameters = []
            body = p[3]
        elif len(p) == 6:  # with params
            parameters = p[3]
            body = p[4]
        name = p[2]
        self.functions.add(name)
        p[0] = ast_builder.funcdef(name, parameters, body)

    def p_params(self, p):
        """params : params PARAM
                  | PARAM"""
        if len(p) == 2:
            arg = ast_builder.arg(p[1])
            p[0] = [arg]
        else:
            args = p[1]
            arg = ast_builder.arg(p[2])
            p[0] = args + [arg]

    def p_numbers(self, p):
        """numbers : numbers NUMBER
                   | NUMBER"""
        if len(p) == 2:
            number = ast_builder.number(p[1])
            p[0] = [number]
        else:
            numbers = p[1]
            number = ast_builder.number(p[2])
            p[0] = numbers + [number]

    def p_error(self, p):
        if p:
            print("Syntax error at: {0}".format(p))
        else:
            print("Syntax error at EOF")
