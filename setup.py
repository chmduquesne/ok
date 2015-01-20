# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="ok",
    version='0.0.1',
    long_description=__doc__,
    packages=["ok"],
    install_requires=[
        "Flask >= 0.10",
        "kyotocabinet >= 1.9",
        "pyxdg >= 0.25",
        "persistentdicts >= 0.0.2"
        ],
    scripts=["ok-serve"],
    zip_safe=False,
    include_package_data=True
)
