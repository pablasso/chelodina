# Chelodina

A transpiler that converts Logo code into Python.

## Status

Proof of concept, pretty much nothing implemented yet.

## Development

The main dependencies are required on [setup.py](setup.py). Using [pipenv](https://pipenv.readthedocs.io/en/latest/) will install those libraries plus the development dependencies specified in the [Pipfile](Pipfile).

```
pipenv install --dev
```

### Running tests

Run tests with:

```
pipenv run tests
```

Automagically run tests after detecting changes with:

```
pipenv run tests-watch
```

### Code style

I use [black](https://github.com/ambv/black) for code formatting, please install the [pre-commit hook](https://github.com/ambv/black#version-control-integration) before doing a PR. This will be enforced with a linter check in the future.

You can run the command manually too:

```
black .
```
