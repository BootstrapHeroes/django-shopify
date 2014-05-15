#!/usr/bin/env python
import os
from setuptools import setup, find_packages

#from djangp_shopify import __version__
__version__ = "0.4.2"

__dir__ = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(__dir__, "shopify_app", "management", "commands", "templates")
templates_files = [os.path.join(templates_dir, file) for file in os.listdir(templates_dir)]

setup(
    name='django-shopify',
    version=__version__,
    description='Django-Shopify generic app',
    author='Bootstrap Heroes Developers',
    author_email='jmg.utn@gmail.com',
    url='https://github.com/SocalProofit/django-shopify',
    classifiers=[
        "Framework :: Django",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Programming Language :: Python :: 2.7",
    ],
    packages=find_packages(exclude=["django_shopify"]),
    data_files=[
        (templates_dir, templates_files)
    ],
    include_package_data=True,
    install_requires=[
        "simplejson",
        "django_conventions",
        "requests",
    ],
    scripts=['bin/start_shopify_app'],
)
