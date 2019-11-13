from setuptools import setup


def read_requirements():
    with open('requirements.txt', 'rt') as fh:
        return fh.read().splitlines()


setup(
    install_requires=read_requirements()
)
