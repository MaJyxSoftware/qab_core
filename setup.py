#!/usr/bin/env python3
import os
import sys
from setuptools import setup, find_packages

VERSION = os.environ.get('GITHUB_REF', '0.0.4').replace('refs/tags/v', '')

is_wheel = 'bdist_wheel' in sys.argv


_license = ""
if os.path.exists('LICENSE'):
    with open('LICENSE') as lf:
        _license = lf.readline().rstrip()

description = ""
if os.path.exists('README.md'):
    with open('README.md') as df:
        description = df.read()

requirements = []
if os.path.exists('requirements.txt'):
    with open('requirements.txt') as rf:
        requirements = rf.readlines()

setup_info = dict(
    name='qab_core',
    version=VERSION,
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    py_modules=['qab_core'],
    license=_license,
    description="QAB framework, high performance, secure, easy to learn, fast to code, ready for production",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/MaJyxSoftware/qab_core",
    author="Benjamin Schwald",
    author_email="b.schwald@majyx.net",
    python_requires='>=3.7',
    classifiers=[
        'English',
        'License :: OSI Approved :: MIT',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'Operating System :: Linux',
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities'
    ],
)

if is_wheel:
    setup_info['install_requires'] = requirements

setup(**setup_info)
