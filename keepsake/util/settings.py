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


from os import path, makedirs
from os.path import expanduser

from keepsake import __version__

from keepsake.unlocker import Unlocker


class Settings(object):

    HOME_DIR = expanduser("~")

    DIR_NAME = ".keepsake"
    FILENAME = "settings"

    SETTINGS_FIELDS = 3  # version, shell and terminal
    SETTINGS_SEPARATOR = "\n"

    def __init__(self):
        self.dir_path = path.join(self.HOME_DIR, self.DIR_NAME)
        self.filepath = path.join(self.dir_path, self.FILENAME)
        self.has_settings = False
        self.unlocker_shell = None
        self.unlocker_terminal = None

    def parse(self, content):
        if isinstance(content, (str, unicode)):
            return content.split(self.SETTINGS_SEPARATOR, self.SETTINGS_FIELDS)
        raise SystemExit("Cannot parse non-string settings")

    def build(self, *params):
        content = [__version__] + [p for p in params]
        if len(content) != self.SETTINGS_FIELDS:
            raise SystemExit("Cannot build settings with wrong size")
        return self.SETTINGS_SEPARATOR.join(content)

    def read_settings(self):
        if not path.exists(self.filepath):
            return False, "file does not exist"
        data = None
        try:
            with open(self.filepath, "r") as fd:
                data = fd.read()
        except Exception as e:
            return False, str(e)
        try:
            _, self.unlocker_shell, self.unlocker_terminal = self.parse(data)
        except Exception as e:
            return False, str(e)
        return True, None

    def read(self):
        self.has_settings, error = self.read_settings()
        return error

    def update(self, shell, terminal):
        if not path.exists(self.dir_path):
            try:
                makedirs(self.dir_path)
            except Exception as e:
                return False, str(e)
        try:
            self.unlocker_shell = shell
            self.unlocker_terminal = terminal
            with open(self.filepath, "w") as fd:
                fd.write(self.build(shell, terminal))
        except Exception as e:
            return False, str(e)
        return True, None

    def read_or_init(self):
        if self.read() is not None:
            self.update(Unlocker.SHELL, Unlocker.TERMINAL)
            return False
        return True
