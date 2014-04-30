#coding=utf8
from setuptools import find_packages
from setuptools import setup
import os

version = '0.0.1.dev0'

setup(
    name='rbco.caseclasses',
    version=version,
    description='Case classes.',
    long_description=(
        open('README.txt').read() + '\n\n' +
        open(os.path.join('docs', 'HISTORY.txt')).read()
    ),
    # Get more strings from
    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Framework :: Plone',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='caseclasses',
    author='Rafael Oliveira',
    author_email='rafaelbco@gmail.com',
    url='',
    license='',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['rbco'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'setuptools',
    ],
    extras_require={
        'test': [
        ]
    },
)