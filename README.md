# Chelodina

A transpiler that converts Logo code into Python.

## Status

Proof of concept, feature list to be defined.

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

And you'll see this:

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
