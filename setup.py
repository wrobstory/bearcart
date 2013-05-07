# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


classifiers = (
    'Development Status :: 4 - Beta',
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
    'long_description': open('README.md', 'rt').read(),
    'author': 'Rob Story',
    'author_email': 'wrobstory@gmail.com',
    'license': 'MIT License',
    'url': 'https://github.com/wrobstory/bearcart',
    'keywords': 'data visualization',
    'classifiers': classifiers,
    'packages': ['bearcart'],
    'package_data': {'bearcart': ['bearcart/*.js',
                                  'bearcart/*.css',
                                  'bearcart/templates/*.html',
                                  'bearcart/templates/*.js']},
    'install_requires': required,
    'zip_safe': True,
}

setup(**kw)
