import argparse
from os import path

from chelodina import compiler


def main(args=None):
    parser = argparse.ArgumentParser(description="Transpile Logo into Python")
    parser.add_argument("--input", help="Logo source file", required=True)
    parser.add_argument("--run", action="store_true", help="Run the transpiled code")
    args = parser.parse_args()

    code = _get_file_contents(parser, args.input)

    if args.run:
        compiler.run(code)
    else:
        return compiler.get_source(code)


def _get_file_contents(parser, file_path):
    if not path.exists(file_path):
        parser.error("Input file not found: {0}".format(file_path))

    content = None
    with open(file_path, "r") as logo_file:
        content = logo_file.read()
    return content


if __name__ == "__main__":
    main()
