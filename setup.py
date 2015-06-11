import os

from setuptools import setup
from setuptools_cmds import Publish, Package


__version__ = '1.0.0'


setup(
    name='setuptools-cmds',
    version=__version__,
    license='WTFPL',
    description='Helper commands for setuptools',
    author='Hugo Castilho',
    author_email='hcastilho@gmail.com',
    url='',
    keywords='setuptools commands',
    #classifiers=[
    #],
    py_modules = ['setuptools_cmds'],
    install_requires=[
        'setuptools',
    ],
    extras_require = {
        'PYTEST': ['pytest', 'pytest-cov'],
    },
    cmdclass = {
        'publish': Publish,
        'package': Package,
    },
)
