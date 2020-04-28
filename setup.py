#coding=utf8
from setuptools import find_packages
from setuptools import setup
import os

version = '1.0.2'

setup(
    name='rbco.caseclasses',
    version=version,
    description='Compact syntax to define simple "struct-like" (or "record-like", "bean-like") classes.',
    long_description=(
        open('README.rst').read() + '\n\n' +
        open(os.path.join('docs', 'HISTORY.txt')).read()
    ),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='caseclasses',
    author='Rafael Oliveira',
    author_email='rafaelbco@gmail.com',
    url='https://github.com/rafaelbco/rbco.caseclasses',
    license='MIT',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['rbco'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
        'funcsigs',
    ],
    extras_require={
        'test': [
        ]
    },
    test_suite='',
)
