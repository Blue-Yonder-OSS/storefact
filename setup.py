# -*- encoding: utf-8 -*-
import io
import re
import os
from os.path import dirname
from os.path import join
import inspect

from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()

instreq = [l.rstrip() for l in read('requirements.txt').splitlines()
           if not l.startswith('#')]


setup(
    name="storefact",
    use_scm_version=dict(write_to='storefact/_version.py'),
    description="A factory for simplekv-Store-based storage classes. Takes configuration values and returns a simplekv-Store",
    author="Felix Marczinowski",
    author_email="felix.marczinowski@blue-yonder.com",
    url="https://github.com/blue-yonder/storefact",
    packages=['storefact'],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Utilities",
    ],
    install_requires=instreq,
    extras_require={
        's3': ['boto'],
        'azure': ['azure-storage-blob'],
    },
    setup_requires=['setuptools_scm']
)
