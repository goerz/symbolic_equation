#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""The setup script."""
from setuptools import find_packages, setup


def get_version(filename):
    """Extract the package version"""
    with open(filename, encoding='utf8') as in_fh:
        for line in in_fh:
            if line.startswith('__version__'):
                return line.split('=')[1].strip()[1:-1]
    raise ValueError("Cannot extract version from %s" % filename)


with open('README.rst', encoding='utf8') as readme_file:
    readme = readme_file.read()

try:
    with open('HISTORY.rst', encoding='utf8') as history_file:
        history = history_file.read()
except OSError:
    history = ''

# requirements for use
requirements = ['uniseg']

# requirements for development (testing, generating docs)
dev_requirements = [
    'black',
    'coverage',
    'coveralls',
    'flake8',
    'gitpython',
    'isort',
    'ipython',
    'jupyter',
    'nbsphinx',
    'nbval',
    'pre-commit',
    'pylint',
    'pytest',
    'pytest-cov',
    'pytest-xdist',
    'sympy',
    'twine',
    'watermark',
    'wheel',
]

version = get_version('./src/symbolic_equation/__init__.py')

setup(
    author="Michael Goerz",
    author_email='mail@michaelgoerz.net',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Natural Language :: English',
        'Topic :: Scientific/Engineering',
    ],
    description=(
        "A class for multiline symbolic equations in the Jupyter Notebook"
    ),
    python_requires='>=3.6',
    install_requires=requirements,
    extras_require={'dev': dev_requirements},
    license="BSD license",
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='sympy, equation, algebra',
    name='symbolic_equation',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url='https://github.com/goerz/symbolic_equation',
    version=version,
    zip_safe=False,
)
