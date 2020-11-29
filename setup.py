import os
from setuptools import setup, find_packages

setup(
    name="ar",
    version="0.3.1",
    description="Access ar archive files (.a)",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="apache-2.0",
    packages=find_packages(),
)
