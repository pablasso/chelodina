import astor

from chelodina.compiler import Compiler


def test_simple_commands():
    simple_commands_code = """
    forward 50
    left 90
    forward 100
    left -90.5
    home
    """

    # TODO: make integration tests cleaner
    simple_commands_expected = "import turtle\nturtle.forward(50.0)\nturtle.left(90.0)\nturtle.forward(100.0)\nturtle.left(-90.5)\nturtle.home()\nturtle.done()\n"
    parsed = Compiler().get_ast(simple_commands_code)
    assert astor.to_source(parsed) == simple_commands_expected
