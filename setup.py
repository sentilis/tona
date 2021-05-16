
from setuptools import setup, find_packages



long_description = ""
with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

requirements = []
with open("requirements.txt", encoding="utf-8") as f:
    for line in f.readlines():
        requirements.append(line.replace('\n', ''))

setup(
    name="tona",
    version="0.1.0",
    url="https://github.com/sentilis/tona",
    author="Sentilis",
    description="Lightweight tools for personal productivity",
    long_description="",
    packages=[
        'tona',
        'tona.cmd',
        'tona.models',
        'tona.utils',
        'tona.web',
        'tona.web.controllers'
    ],
    package_dir={
        'tona': '.',
        'tona.cmd': 'cmd',
        'tona.models': 'models',
        'tona.utils': 'utils',
        'tona.web': 'web',
        'tona.web.controllers': 'web/controllers'
    },
    package_data={'tona': ['web/static/*/*', 'web/templates/*']},
    entry_points={
        "console_scripts": ["tona=tona.cmd.main:cli"]
    },
    install_requires=requirements,
    license="GPLv3",
    classifiers=[
        "Development Status :: 1 - Beta",

        "Environment :: Console",

        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",

        "License :: OSI Approved :: GPLv3 License",

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
    ]
)