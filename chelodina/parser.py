import ply.yacc as yacc

from chelodina import ast_builder
from chelodina.lexer import Lexer
from chelodina.utils import validator


class Parser:
    tokens = Lexer.tokens
    module = "turtle"
    precedence = (("left", "PLUS", "MINUS"), ("left", "MULT", "DIV"))

    def __init__(self):
        self.functions = set()
        self.calls = []

    def parse(self, code):
        Lexer().build()
        parser = yacc.yacc(module=self, write_tables=False)
        parsed_ast = parser.parse(code)
        validator.validate_statements(self.calls, self.functions)
        parsed_ast = ast_builder.turtle_wrapper(parsed_ast)
        parsed_ast = ast_builder.fill_locations(parsed_ast)
        return parsed_ast

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
                     | funcdef
                     | repeat"""
        p[0] = p[1]

    def p_expression(self, p):
        """expression : NAME terms
                      | NAME """
        name = p[1]
        module = self.module if validator.is_std_function(name) else ""
        self.calls.append(name)
        if len(p) == 3:
            parameters = p[2]
            p[0] = ast_builder.call_expr(name, module, parameters)
        else:
            p[0] = ast_builder.call_expr(name, module)

    def p_terms_number(self, p):
        """terms : terms NUMBER
                 | NUMBER"""
        if len(p) == 2:
            number = ast_builder.number(p[1])
            p[0] = [number]
        else:
            numbers = p[1]
            number = ast_builder.number(p[2])
            p[0] = numbers + [number]

    def p_terms_params(self, p):
        """terms : terms PARAM
                 | PARAM"""
        if len(p) == 2:
            arg = ast_builder.ast_name(p[1])
            p[0] = [arg]
        else:
            args = p[1]
            arg = ast_builder.ast_name(p[2])
            p[0] = args + [arg]

    def p_terms_binary_operations(self, p):
        """terms : terms PLUS terms
                 | terms MINUS terms
                 | terms MULT terms
                 | terms DIV terms"""
        operator = ast_builder.operator(p[2])
        # TODO: how can we do this with plain objects outside the array?
        operand_a = p[1][0]
        operand_b = p[3][0]
        p[0] = [ast_builder.binary_operation(operator, operand_a, operand_b)]

    def p_funcdef(self, p):
        """funcdef : TO NAME terms statements END
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

    def p_repeat(self, p):
        """repeat : REPEAT terms LBRACKET statements RBRACKET"""
        # TODO: how can we do this with plain objects outside the array?
        times = p[2][0]
        body = p[4]
        p[0] = ast_builder.repeat(times, body)

    def p_error(self, p):
        if p:
            print("Syntax error at: {0}".format(p))
        else:
            print("Syntax error at EOF")
