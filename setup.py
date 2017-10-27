from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="ConfigDir",
    version="0.2",
    packages=find_packages(),
    install_requires=requirements,

    author="Dmitry Teselkin",
    author_email="teselkin.d@gmail.com",
    description="Hierarchical config directory based on YAML",
)
