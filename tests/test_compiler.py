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

    # TODO: make integration tests import automatically generated fixtures
    simple_commands_expected = "import turtle\nturtle.forward(50.0)\nturtle.left(90.0)\nturtle.forward(100.0)\nturtle.left(-90.5)\nturtle.home()\nturtle.done()\n"
    parsed = Compiler().get_ast(simple_commands_code)
    assert astor.to_source(parsed) == simple_commands_expected


def test_functions():
    function_code = """
    to myfunction
    forward 51.0
    left 91
    end

    forward 45
    myfunction
    right 20
    """

    # TODO: make integration tests import automatically generated fixtures
    function_code_expected = "import turtle\n\n\ndef myfunction():\n    turtle.forward(51.0)\n    turtle.left(91.0)\n\n\nturtle.forward(45.0)\nmyfunction()\nturtle.right(20.0)\nturtle.done()\n"
    parsed = Compiler().get_ast(function_code)
    assert astor.to_source(parsed) == function_code_expected
