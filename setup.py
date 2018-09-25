from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="chelodina",
    version="0.5.5",
    description="A Logo to Python transpiler",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/pablasso/chelodina",
    author="Juan Pablo Ortiz",
    author_email="me@pablasso.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["ply", "astor"],
    zip_safe=False,
    entry_points={"console_scripts": ["chelodina = chelodina.__main__:main"]},
)
