#!/usr/bin/env python
#
# Setup prog for vc3-client
#
#

import sys
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

release_version='0.9.1'

etc_files = ['./etc/vc3-client.conf']

scripts = ['scripts/vc3-client', ]


def choose_data_file_location():
    rpm_install = False

    if 'bdist_rpm' in sys.argv:
        rpm_install = True

    if rpm_install:
        return '/etc/vc3'
    else:
        return 'etc'
       
# ===========================================================

# setup for distutils
print(scripts)
setup(
    name="vc3-client",
    version=release_version,
    description='vc3-client package',
    long_description='''This package contains vc3 client''',
    license='GPL',
    author='VC3 Team',
    author_email='vc3-project@googlegroups.com',
    maintainer='VC3 team',
    maintainer_email='vc3-project@googlegroups.com',
    url='http://virtualclusters.org/',
    packages=['vc3client'],
    scripts=scripts,
    data_files=[(choose_data_file_location(), etc_files)],
    install_requires=['requests', 'pyopenssl', 'cherrypy', 'pyyaml', 'vc3-info-service']
)
