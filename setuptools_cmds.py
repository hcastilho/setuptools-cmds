import os
import sys

from setuptools import Command
from setuptools.command.test import test as TestCommand

class Publish(Command):
    description = 'Replacement for the cryptic sdist upload'
    user_options = [
        ('repository=', 'r', "Repository [default: devpi"),
    ]
    default_repository = 'devpi'

    def initialize_options(self):
        self.repository = None

    def finalize_options(self):
        if self.repository is None:
            self.repository = self.default_repository

    def run(self):
        os.system('python setup.py sdist upload -r {}'.format(self.repository))


class Package(Publish):
    description = 'Build system package with empackage'
    user_options = [
        ('repository=', 'r', "Repository [default: devpi"),
        ('push', 'p', "Push to package repository"),
        ('get', 'g', "Download"),
    ]
    packager_dir = 'package'

    def initialize_options(self):
        Publish.initialize_options(self)
        self.get = False
        self.push = False

    def finalize_options(self):
        Publish.finalize_options(self)
        if self.push is None:
            pass

    def run(self):
        Publish.run(self)
        oldpwd = os.getcwd()
        os.chdir(self.packager_dir)
        os.system('empackage {} {}'.format(
            '--get' if self.get else '',
            '--push' if self.push else '',
            ))
        os.chdir(oldpwd)


class Tag(Command):
    user_options = []
    version = None

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if self.version is None:
            print('Invalid version')
            sys.exit(1)
        os.system("git tag -a {0} -m 'version {0}'" % (self.version))
        os.system("git push --tags")


class PyTest(TestCommand):
    description = 'Run tests'
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]
    test_package_name = 'fraudsible'

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--verbose',
            '--cov={0}'.format(self.test_package_name),
            '--cov-report=term-missing',
        ]
        self.test_args.extend(self.pytest_args)
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


