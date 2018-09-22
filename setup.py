from setuptools import setup


setup(
    name="chelodina",
    version="0.1",
    description="A Logo to Python transpiler",
    url="http://github.com/pablasso/chelodina",
    author="Juan Pablo Ortiz",
    author_email="me@pablasso.com",
    license="MIT",
    packages=["chelodina"],
    install_requires=["ply", "astor"],
    zip_safe=False,
)
