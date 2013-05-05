# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
from os.path import abspath, dirname, join

path = abspath(dirname(__file__))

classifiers = (
    'Development Status :: 3 - Alpha',
    'Programming Language :: Python :: 2.7',
    'License :: OSI Approved :: MIT License',
)

required = (
    'pandas'
)

kw = {
    'name': 'bearcart',
    'version': '0.1.0',
    'description': 'Python Pandas + Rickshaw.js = BearCart',
    'long_description': open(join(path, 'README.md')).read(),
    'author': 'Rob Story',
    'author_email': 'wrobstory@gmail.com',
    'license': 'MIT License',
    'url': 'https://github.com/wrobstory/bearcart',
    'keywords': 'data visualization',
    'classifiers': classifiers,
    'packages': ['bearcart'],
    'package_data': {'bearcart': ['*.html']},
    'install_requires': required,
    'zip_safe': True,
}

setup(**kw)
