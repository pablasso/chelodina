import ply.lex as lex


class Lexer:

    tokens = (
        "TO",
        "END",
        "NAME",
        "NUMBER",
        "NAME",
        "PARAM",
        "REPEAT",
        "LBRACKET",
        "RBRACKET",
        "PLUS",
        "MINUS",
        "MULT",
        "DIV",
    )
    reserved = {"to": "TO", "end": "END", "repeat": "REPEAT"}

    t_ignore = " \t"
    t_PARAM = r":[a-zA-Z]+"
    t_LBRACKET = r"\["
    t_RBRACKET = r"\]"
    t_PLUS = r"\+"
    t_MINUS = r"-"
    t_MULT = r"\*"
    t_DIV = r"/"

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def t_NAME(self, t):
        r"[a-zA-Z]+"
        t.value = t.value.lower()
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
