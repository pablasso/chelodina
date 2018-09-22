import ply.lex as lex


class Lexer:

    tokens = ("TO", "END", "NAME", "NUMBER", "NAME", "PARAM")
    reserved = {"to": "TO", "end": "END"}

    t_ignore = " \t"
    t_PARAM = r":[a-zA-Z]+"

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def t_NAME(self, t):
        r"[a-zA-Z]+"
        t.type = self.reserved.get(t.value, "NAME")
        return t

    def t_NUMBER(self, t):
        r"-?\d+(\.+\d+)?"
        t.value = float(t.value)
        return t

    def t_newline(self, t):
        r"\n+"
        t.lexer.lineno += t.value.count("\n")

    def t_error(self, t):
        print("Error: token {0}".format(t))
        t.lexer.skip(1)
