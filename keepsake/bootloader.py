#!/usr/bin/env python
#
# Copyright 2018 Alexandru Catrina
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from distutils import spawn
from os import path
from os.path import expanduser


class Boot(object):

    def __init__(self):
        self.keepsake_status = False
        self.unlocker_status = False
        self.unlocker_scripts = False
        self.secrets_status = False
        self.secrets_encryption = False

    def __repr__(self):
        return str({k: v for k, v in self.__dict__.iteritems() if k[0] != "_"})

    def check_system(self):
        self.keepsake_status = self.is_installed("keepsake-unlock")
        self.unlocker_status = self.is_installed("unlocker")
        self.unlocker_scripts = self.is_installed("unlock", "lock")
        self.secrets_status = self.has_file(".secrets")
        self.secrets_encryption = self.has_file(".secrets.lock")

    def has_file(self, filename, dirname=".unlocker"):
        return path.exists(path.join(expanduser("~"), dirname, filename))

    def is_installed(self, *programs):
        return all([spawn.find_executable(p) is not None for p in programs])
