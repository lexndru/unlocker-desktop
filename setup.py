#!/usr/bin/env python

from setuptools import setup

from keepsake import __version__

_desc = "Keepsake Desktop is a credentials manager with support for various " \
        "protocols such as SSH, MySQL, Redis, Mongo, PostgreSQL. It's a GUI " \
        "frontend for Unlocker, therefore it requires Unlocker to be " \
        "installed and all helper scripts to be deployed on the current " \
        "machine. Keepsake has implemented core functionalities of " \
        "Unlocker, such as passwordless connections, encryption, appending, " \
        "updating, removing, listing and migrating secrets."


setup(name="keepsake",
    packages=[
        "keepsake",
        "keepsake.gui",
        "keepsake.gui.dialog",
        "keepsake.gui.event",
        "keepsake.gui.menu",
        "keepsake.gui.misc",
        "keepsake.gui.toolbar",
        "keepsake.gui.validator",
        "keepsake.gui.view",
        "keepsake.gui.view.detail",
        "keepsake.gui.view.list",
        "keepsake.icons",
        "keepsake.util",
    ],
    include_package_data=True,
    entry_points = {
        "console_scripts": [
            "keepsake = keepsake.bootstrap:main"
        ]
    },
    install_requires=[
        "unlocker==2.2.0",
        "wxPython==4.0.3"
    ],
    test_suite="tests",
    version=__version__,
    description="GUI and CLI credentials manager",
    long_description=_desc,
    author="Alexandru Catrina",
    author_email="alex@codeissues.net",
    license="MIT",
    url="https://github.com/lexndru/unlocker-desktop",
    download_url="https://github.com/lexndru/unlocker-desktop/archive/v{}.tar.gz".format(__version__),
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
