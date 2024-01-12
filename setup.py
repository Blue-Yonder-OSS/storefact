# -*- encoding: utf-8 -*-
import io
from os.path import dirname
from os.path import join

from setuptools import setup


def read(*names, **kwargs):
    return io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8")
    ).read()


long_description = read("README.rst")


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
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Utilities",
    ],
    install_requires=instreq,
    extras_require={
        's3': ['boto'],
        'azure': ['azure-storage-blob'],
    },
    setup_requires=['setuptools_scm'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
