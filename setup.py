from __future__ import unicode_literals

import re


from setuptools import find_packages, setup


def read_file(filename):
    with open(filename) as fh:
        return fh.read()


def get_version(filename):
    init_py = read_file(filename)
    metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", init_py))
    return metadata['version']


setup(
    name='pyspotify-connect',
    version=get_version('spotifyconnect/__init__.py'),
    url='https://github.com/chukysoria/pyspotify-connect',
    license='Apache License, Version 2.0',
    author='chukysoria',
    author_email='nomail@nomail.com',
    description='Python wrapper for libspotify-connect',
    long_description=read_file('README.rst'),
    keywords='spotify connect library',
    packages=find_packages(exclude=['tests', 'tests.*']),
    test_suite="tests",
    zip_safe=False,
    include_package_data=True,
    setup_requires=[
        'cffi >= 1.0.0'],
    tests_require=['pytest'],
    cffi_modules=['spotifyconnect/_spotifyconnect_build.py:ffi'],
    install_requires=[
        'cffi >= 1.0.0',
        'Flask >= 0.10.1'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries',
    ],
)
