# Chelodina

[![LICENSE](license.svg)](https://github.com/pablasso/chelodina/blob/master/LICENSE) [![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Chelodina is a transpiler that converts LOGO:

```logo
TO triangle :length
  REPEAT 3 [ FORWARD :length RIGHT 120 ]
END

TO flower :length :count
  REPEAT 150 [
    triangle :length
    RIGHT 360 / :count
  ]
END

TO web
  REPEAT 6 [ flower 150 18 ]
END

web

```

Into Python:

```python
import turtle


def triangle(p_length):
    for _ in range(3):
        turtle.forward(p_length)
        turtle.right(120.0)


def flower(p_length, p_count):
    for _ in range(150):
        triangle(p_length)
        turtle.right(360.0 / p_count)


def web():
    for _ in range(6):
        flower(150.0, 18.0)


web()
turtle.done()
```

## Installation

```
pip install chelodina
```

## Usage

```
usage: chelodina [-h] --input INPUT [--run]

arguments:
  -h, --help     show this help message and exit
  --input INPUT  Logo source file
  --run          Run the transpiled code
```

There's some ready [examples](/examples) to try if you clone the repository:

```
chelodina --input examples/example1.logo
```

You can also trigger the program to run in a GUI:

```
chelodina --input examples/example1.logo --run
```

## Status

- Implemented:
	- Motion functions: `FORWARD`, `BACK`, `LEFT`, `RIGHT`, `SETPOS`, `SETX`, `SETY`, `SETHEADING`, `SETH`, `HOME`
	- Screen functions: `DONE`, `CLEARSCREEN`
	- Control structures: `REPEAT`
	- Function calls and definitions with optional parameters
	- Binary operations

This is still on an early stage, I focused on making some [examples](/examples) work. Functions with similar structure are trivial to implement, but I want to focus on improving the tests first.

For grammar reference look at [grammar.bnf](grammar.bnf).

### Known quirks

- Validations for a valid AST (e.g. to make sure a function parameter exists before trying to use it on a statement) are not user friendly yet. I suggest double-checking your programs [elsewhere](https://calormen.com/jslogo/) first.
- Only tested on Python 3.6+ so far.

## Development

Use [pipenv](https://pipenv.readthedocs.io/en/latest/) to install dependencies:

```
pipenv install --dev
```

### Running tests

Run tests with:

```
pipenv run tests
```

Automatically run tests after detecting changes with:

```
pipenv run tests-watch
```

### Debug

- The easy way is to write tests to debug your code. Feel free to use `assert False` where necessary.
- If you need to run tests along anything that sends to or needs the standard output (a debugger like pdb or pudb), you'll need to run `pytest` directly: `pytest --capture=no`.
- There's a library to pretty-print your AST in the `utils` package. Usage example:

```python
from chelodina import compiler
from chelodina.utils.debug import parseprint

logo_code = """
to myfunction
  forward 51.0
  left 91
end
"""

parsed_ast = compiler.get_ast(logo_code)
parseprint(parsed)
```

And you'll see the resulting AST:

```python
Module(body=[
    Import(names=[
        alias(name='turtle', asname=None),
      ]),
    FunctionDef(name='myfunction', args=arguments(args=[], vararg=None, kwonlyargs=[], kw_defaults=[], kwarg=None, defaults=[]), body=[
        Expr(value=Call(func=Attribute(value=Name(id='turtle', ctx=Load()), attr='forward', ctx=Load()), args=[
            Num(n=51.0),
          ], keywords=[])),
        Expr(value=Call(func=Attribute(value=Name(id='turtle', ctx=Load()), attr='left', ctx=Load()), args=[
            Num(n=91.0),
          ], keywords=[])),
      ], decorator_list=[], returns=None),
    Expr(value=Call(func=Attribute(value=Name(id='turtle', ctx=Load()), attr='done', ctx=Load()), args=[], keywords=[])),
  ])
```


### Code style

I use [black](https://github.com/ambv/black) for code formatting, please install the [pre-commit hook](https://github.com/ambv/black#version-control-integration) before doing a PR. This will be enforced with a linter check in the future.

You can run the command manually too:

```
black .
```

Not required, but if you install [EditorConfig](https://editorconfig.org) in your editor of choice it will make your life easier.
