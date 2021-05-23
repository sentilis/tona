# -*- coding: utf-8 -*-
#    Copyright (C) 2021  The Project TONA Authors
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
from setuptools import setup, Command
from shutil import rmtree
import os
import sys
import re

class PublishCommand(Command):

    user_options = [
        ('testpypi', 't', "Publish on https://test.pypi.org/")
    ]

    def initialize_options(self):
        self.testpypi = 0

    def finalize_options(self):
        pass

    def run(self):

        try:
            print("Removing previous builds ...")
            rmtree("./dist")
        except OSError:
            pass

        print("Building Source and Wheel (universal) distribution…")
        os.system("{0} setup.py sdist bdist_wheel --universal"
                  .format(sys.executable))

        print("Uploading the package to PyPi via Twine…")

        if self.testpypi:
            os.system("twine upload --repository testpypi dist/*")
        else:
            os.system("twine upload dist/*")


long_description = ""
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

requirements = []
with open("requirements.txt", encoding="utf-8") as f:
    for line in f.readlines():
        requirements.append(line.replace('\n', ''))

package_data = []
package_dir = {}
packages =[]
for data in os.walk("."):
    dir = data[0]
    if not re.search(".git|.pm|__pycache__|storage", dir):
        if re.search("static|templates", dir):
            package_data.append(dir+"/*")
        else:
            # TODO: Check is work replace on Windows
            package = 'tona' if dir == '.' else 'tona' + dir[1:].replace('/','.')
            package_dir.update({package: dir})
            packages.append(package)

setup(
    name="tona",
    version="0.1.0",
    url="https://github.com/sentilis/tona",
    author="Jose Hbez",
    author_email="me@josehbez.com",
    description="Lightweight tools for personal productivity",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=packages,
    package_dir=package_dir,
    package_data={'tona': package_data},
    entry_points={
        "console_scripts": ["tona=tona.main:main"]
    },
    install_requires=requirements,
    license="GPLv3",
    classifiers=[
        "Development Status :: 4 - Beta",

        "Environment :: Console",

        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",

        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",

        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: POSIX :: Linux",

        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Utilities",
    ],
    cmdclass={
        "publish": PublishCommand
    }
)