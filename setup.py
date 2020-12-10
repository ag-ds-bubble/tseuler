import setuptools
import json
import sys
from urllib import request    
from pkg_resources import parse_version

""""
versioning : x[Major Fixes].x[Minor Fixes].x[Patch Number].x[Development Version]
"""

# Command to upload to testpypi :
#   cls & rmdir /s /q build dist tseuler.egg-info & python setup_dev.py sdist & python setup_dev.py bdist_wheel & twine upload -r testpypi dist/*
# Command to upload to pypi :
#   cls & rmdir /s /q build dist tseuler.egg-info & python setup.py sdist & python setup.py bdist_wheel & twine upload dist/*

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    try:
        lineiter = (line.strip() for line in open(filename))
        temp = [line.replace('==','>=') for line in lineiter if line and not line.startswith("#")]
        return [k for k in temp if 'scikit-learn' not in k]
    except:
        return []

# Constants
REQS = parse_requirements('requirements.txt')
from tseuler import __version__
_next_version = __version__


with open("README.md", "r") as fh:
    long_description = fh.read()

# Package Setup
setuptools.setup(name="tseuler",
                 version=_next_version,
                 author="Achintya Gupta",
                 author_email="ag.ds.bubble@gmail.com",
                 description="A library for Time-Series exploration, analysis & modelling.",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url="https://github.com/ag-ds-bubble/tseuler",
                 packages=setuptools.find_packages(),
                 include_package_data = True,
                 package_data={'tseuler': ['tsmad/_helpers/_logo.png']},
                 install_requires=REQS,
                 classifiers=["Programming Language :: Python :: 3",
                              "Development Status :: 4 - Beta",
                              "Intended Audience :: Developers",
                              "License :: OSI Approved :: BSD License",
                              "Operating System :: OS Independent",],
                 python_requires='>=3.7')

