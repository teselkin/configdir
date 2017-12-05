from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="ConfigDir",
    version="0.3",
    packages=find_packages(),
    install_requires=requirements,
    download_url='http://github.com/teselkin/configdir/archive/master.tar.gz#egg=configdir',

    author="Dmitry Teselkin",
    author_email="teselkin.d@gmail.com",
    description="Hierarchical config directory based on YAML",
)
