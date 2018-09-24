import astor

from chelodina import compiler

# TODO: these are integration tests, automate the fixture creation with astor instead of embedding it here


def test_simple_commands():
    simple_commands_code = """
    forward 50
    left 90
    forward 100
    left -90.5
    home
    """
    simple_commands_expected = "import turtle\nturtle.forward(50.0)\nturtle.left(90.0)\nturtle.forward(100.0)\nturtle.left(-90.5)\nturtle.home()\nturtle.done()\n"
    parsed = compiler.get_ast(simple_commands_code)
    assert astor.to_source(parsed) == simple_commands_expected


def test_function():
    function_code = """
    to myfunction
        forward 51.0
        left 91
    end

    forward 45
    myfunction
    right 20
    """
    function_code_expected = "import turtle\n\n\ndef myfunction():\n    turtle.forward(51.0)\n    turtle.left(91.0)\n\n\nturtle.forward(45.0)\nmyfunction()\nturtle.right(20.0)\nturtle.done()\n"
    parsed = compiler.get_ast(function_code)
    assert astor.to_source(parsed) == function_code_expected


def test_function_with_params():
    function_code = """
    to myfunction :left :forward
        forward :left
        left :forward
    end

    myfunction 48.0 98.0
    """
    function_code_expected = "import turtle\n\n\ndef myfunction(p_left, p_forward):\n    turtle.forward(p_left)\n    turtle.left(p_forward)\n\n\nmyfunction(48.0, 98.0)\nturtle.done()\n"
    parsed = compiler.get_ast(function_code)
    assert astor.to_source(parsed) == function_code_expected


def test_repeat():
    code = """
    repeat 5.0 [ forward 50 right 30 ]
    left 100

    to myfunction :param
        repeat :param [ left 10 ]
    end

    myfunction 5.0
    """
    code_expected = "import turtle\nfor _ in range(5):\n    turtle.forward(50.0)\n    turtle.right(30.0)\nturtle.left(100.0)\n\n\ndef myfunction(p_param):\n    for _ in range(p_param):\n        turtle.left(10.0)\n\n\nmyfunction(5.0)\nturtle.done()\n"
    parsed = compiler.get_ast(code)
    assert astor.to_source(parsed) == code_expected


def test_binary_operations():
    code = """
    to myfunction :parama :paramb
        forward :parama + 50.0
        left :parama - :paramb
        forward :paramb * 50.0
        left 50.0 / 25.0 * 2 - 1
    end

    myfunction 50.0 + 10.0 30.0
    """
    code_expected = "import turtle\n\n\ndef myfunction(p_parama, p_paramb):\n    turtle.forward(p_parama + 50.0)\n    turtle.left(p_parama - p_paramb)\n    turtle.forward(p_paramb * 50.0)\n    turtle.left(50.0 / 25.0 * 2.0 - 1.0)\n\n\nmyfunction(50.0 + 10.0, 30.0)\nturtle.done()\n"
    parsed = compiler.get_ast(code)
    assert astor.to_source(parsed) == code_expected
