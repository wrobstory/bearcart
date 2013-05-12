# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='bearcart',
    version='0.1.3',
    description='Python Pandas + Rickshaw.js = BearCart',
    author='Rob Story',
    author_email='wrobstory@gmail.com',
    license='MIT License',
    url='https://github.com/wrobstory/bearcart',
    keywords='data visualization',
    classifiers=['Development Status :: 4 - Beta',
                 'Programming Language :: Python :: 2.7',
                 'License :: OSI Approved :: MIT License'],
    packages=['bearcart'],
    package_data={'': ['*.js',
                       '*.css',
                       'templates/*.html',
                       'templates/*.js']}
)
