from setuptools import setup, find_packages

setup(
    name='gendiff',
    version='1.0.0',
    author='Emil Murzin',
    author_email='emil.morua@gmail.com',
    description=('CLI utility that allows you to find '
                 'and display differences between two '
                 'configuration files in json or yml format.'),
    packages=find_packages(),
)
