from setuptools import setup

from browser import NAME, VERSION

setup(
    name=NAME,
    author="kamangir",
    version=VERSION,
    description="a browser plugin for abcli.",
    packages=[NAME],
)
