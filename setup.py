#!/usr/bin/env python

from setuptools import setup

from keepsake import __version__


setup(name="keepsake",
    packages=[
        "keepsake",
        "keepsake.gui",
        "keepsake.util",
    ],
    include_package_data=True,
    entry_points = {
        "console_scripts": [
            "keepsake = keepsake.bootstrap:main"
        ]
    },
    install_requires=[
        # TODO: complete requirements
    ],
    test_suite="tests",
    version=__version__,
    description="GUI and CLI credentials manager",
    long_description="n/a",
    author="Alexandru Catrina",
    author_email="alex@codeissues.net",
    license="MIT",
    url="https://github.com/lexndru/unlocker-gui",
    download_url="https://github.com/lexndru/unlocker-gui/archive/v{}.tar.gz".format(__version__),
    keywords=["credentials manager", "keychain", "remote connection"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Education",
        "Topic :: System :: Networking",
        "Topic :: System :: Shells",
        "Topic :: System :: Systems Administration",
        "Topic :: Terminals",
        "Topic :: Utilities",
        "Topic :: Internet",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Unix Shell",
        "Operating System :: POSIX",
    ],
)
