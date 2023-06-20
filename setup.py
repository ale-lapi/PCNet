#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages

__author__ = "Alessandro Lapi"
__email__ = "alessandro.lapi@studio.unibo.it"


def get_requires(requirements_filename):
    '''
    What packages are required for this module to be executed?

    Parameters
    ----------
    requirements_filename : str
        filename of requirements (e.g requirements.txt)

    Returns
    -------
    requirements : list
        list of required packages
    '''
    with open(requirements_filename, 'r') as fp:
        requirements = fp.read()

    return list(filter(lambda x: x != '', requirements.split()))

def read_description(readme_filename):
    '''
    Description package from filename

    Parameters
    ----------
    readme_filename : str
        filename with readme information (e.g README.md)

    Returns
    -------
    description : str
        str with description
    '''

    try:

        with open(readme_filename, 'r') as fp:
            description = '\n'
            description += fp.read()

        return description

    except IOError:
        return ''

# Path of the current file
here = os.path.abspath(os.path.dirname(__file__))

# Package-Metadata
NAME = "PCNet"
DESCRIPTION = 'PCNet is a tool for building a citation network from PubMed database'
URL = 'https://github.com/ale-lapi/PCNet'
EMAIL = 'alessandro.lapi@studio.unibo.it'
AUTHOR = 'Alessandro Lapi'
VERSION = '1.0.0'
KEYWORDS = 'citation-network pubmed xml-parser'
REQUIREMENTS_FILENAME = os.path.join(here, 'requirements.txt')
README_FILENAME = os.path.join(here, 'README.md')

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    LONG_DESCRIPTION = read_description(README_FILENAME)

except IOError:
    LONG_DESCRIPTION = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    keywords=KEYWORDS,
    packages=find_packages(include=['PCNet'], 
                           exclude=('test', 'testing')),
    install_requires=get_requires(REQUIREMENTS_FILENAME),
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.5',
    license = 'MIT'
)
