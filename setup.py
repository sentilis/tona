# -*- coding: utf-8 -*-
# Part of Sentilis. See LICENSE file for full copyright and licensing details.
from setuptools import setup, Command, find_packages
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


package_data = {}
package_dir = {}
packages = []
for data in os.walk("tona"):
    dir = data[0]
    if not re.search(".git|.pm|__pycache__|storage", dir):
        if re.search("static|templates", dir):
            package_data.update({dir.replace("/", "."): [dir + "/*.*"]})
        else:
            # TODO: Check is work replace on Windows
            package =  dir.replace('/', '.')
            package_dir.update({package: dir})
            packages.append(package)

setup(
    name="tona",
    version="0.1.2",
    url="https://github.com/sentilis/tona",
    author="Jose Hbez",
    author_email="dev@josehbez.com",
    description="The All-In-One workspace for personal productivity",
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=packages,
    package_dir=package_dir,
    include_package_data=True,
    #package_data=package_data,
    entry_points={
        "console_scripts": ["tona=tona.__main__:main"]
    },
    install_requires=requirements,
    license="LGPLv3",
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
    # cmdclass={
    #    "publish": PublishCommand
    # }
)
