from setuptools import setup

setup(
    name="ok",
    version='0.0.1',
    long_description=__doc__,
    packages=["ok"],
    install_requires=[
        "Flask >= 0.10",
        "kyotocabinet >= 1.9",
        "pyxdg >= 0.25"
        ],
    scripts=["ok-serve"]
)
