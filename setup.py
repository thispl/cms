# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in cms/__init__.py
from cms import __version__ as version

setup(
	name='cms',
	version=version,
	description='Canteen Management System',
	author='Teampro',
	author_email='subash.p@groupteampro.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
