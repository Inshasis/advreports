from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in advreports/__init__.py
from advreports import __version__ as version

setup(
	name="advreports",
	version=version,
	description="Advance Reports with Customizations",
	author="Manish Arora",
	author_email="manish.arora@aurigait.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
