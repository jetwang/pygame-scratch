# !/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='pygamescratch',
    version='0.2',
    description='provide scratch like API using pygame, while just using 2 threads',
    keywords='scratch children education learn python game easy',
    author='Jet Wang',
    author_email='jetwangw@163.com',
    license='MIT',
    url='https://github.com/jetwang/pygame-scratch',
    include_package_data=True,
    packages=find_packages(
        where='src',
        include=['pygamescratch'],
        exclude=['sample*'],
    ),
    package_dir={"": "src"},
    install_requires=['pygame']
)
