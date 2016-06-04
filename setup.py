# from distutils.core import setup
from setuptools import setup, find_packages
import os
import glob

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

# use the in house version number so we stay in synch with ourselves.
from plambda.eval import PLambda
    
setup(
    name='PLambda',
    version=PLambda.plambda_version, 
    description='The PLambda language',
    long_description=long_description,
    url='https://github.com/SRI-CSL/PLambda',
    author='Ian A. Mason',
    author_email='iam@csl.sri.com',
    

    packages=find_packages(exclude=['tests']),
    
    entry_points = {
        'console_scripts': [
            'plambda = plambda.eval.PLambda:main',
            'pyactor = plambda.actors.pyactor:main',
            'plambdaparse = plambda.visitor.Parser:main',
        ],
    },


    
    license='MIT',
    
    install_requires=[
        "antlr4-python2-runtime >= 4.5.3"
    ],
    
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Topic :: System :: Distributed Computing',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)