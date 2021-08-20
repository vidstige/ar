from setuptools import setup, find_packages

setup(
    name="ar",
    version="0.3.2",
    description="Access ar archive files (.a)",
    url="http://github.com/vidstige/ar/",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license="apache-2.0",
    packages=find_packages(),
    author="Samuel Carlsson",
    author_email="samuel.carlsson@gmail.com",
)
