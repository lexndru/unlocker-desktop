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

from shlex import split as command
from subprocess import Popen, PIPE

from keepsake.util.safe_output import safe_output


class Unlocker(object):

    ROWS_SEPARATOR, COLS_SEPARATOR = "\n", "|"
    ROWS_PADDING = 2  # header and separator
    COLS_FIELDS = (
        "auth_signature",
        "jump_signature",
        "scheme",
        "ipv4",
        "port",
        "host",
        "user",
        "name",
    )

    PROGRAM_NAME = "unlocker"
    SCRIPT_DECRYPT = "unlock"
    SCRIPT_ENCRYPT = "lock"

    OPT_INSTALL = "install"
    OPT_MIGRATE = "migrate"

    OPT_INIT = "init"
    OPT_LIST = "list"

    OPT_APPEND = "append"
    OPT_UPDATE = "update"
    OPT_REMOVE = "remove"
    OPT_FORGET = "forget"
    OPT_LOOKUP = "lookup"
    OPT_RECALL = "recall"

    SELF_BOUNCE = "~"

    class Error(Exception):
        pass

    _term = "gnome-terminal -e '%s'"
    _bash = "bash -c '%s'"

    @classmethod
    @safe_output
    def list(cls):
        cls._proc = Popen([cls.PROGRAM_NAME, cls.OPT_LIST], stdout=PIPE)
        output, error = cls._proc.communicate()
        if error is not None:
            raise cls.Error(error)
        return output

    @classmethod
    def append(cls, name, host, port, user, auth, scheme, jump=None):
        if not auth:
            auth = "password"
        arguments = [cls.PROGRAM_NAME, cls.OPT_APPEND,
                     "--name", unicode(name),
                     "--host", unicode(host),
                     "--port", unicode(port),
                     "--user", unicode(user),
                     "--auth", unicode(auth),
                     "--scheme", unicode(scheme)]
        if jump is not None and len(jump) > 0:
            arguments.append("--jump-server")
            arguments.append(jump)
        cls._proc = Popen(command(cls._term % " ".join(arguments)))
        output, error = cls._proc.communicate()
        if error is not None:
            raise cls.Error(error)
        return output

    @classmethod
    def remove(cls, name):
        arguments = [cls.PROGRAM_NAME, cls.OPT_REMOVE, "--name", unicode(name)]
        cls._proc = Popen(command(cls._term % " ".join(arguments)))
        output, error = cls._proc.communicate()
        if error is not None:
            raise cls.Error(error)
        return output

    @classmethod
    def update(cls, name, auth, jump=None):
        arguments = [cls.PROGRAM_NAME, cls.OPT_UPDATE,
                     "--name", unicode(name), "--auth", unicode(auth)]
        if jump is not None and len(jump) > 0:
            arguments.append("--jump-server")
            arguments.append(jump)
        cls._proc = Popen(command(cls._term % " ".join(arguments)))
        output, error = cls._proc.communicate()
        if error is not None:
            raise cls.Error(error)
        return output

    @classmethod
    def migrate_export(cls, filename, servers):
        arguments = [cls.PROGRAM_NAME, cls.OPT_MIGRATE,
                     "--export", " ".join(servers), ">", unicode(filename)]
        cls._proc = Popen(cls._bash % " ".join(arguments), shell=True)
        output, error = cls._proc.communicate()
        if error is not None:
            raise cls.Error(error)
        return output

    @classmethod
    def migrate_import(cls, filename):
        arguments = [cls.PROGRAM_NAME, cls.OPT_MIGRATE,
                     "--import", "<", unicode(filename)]
        cls._proc = Popen(cls._bash % " ".join(arguments), shell=True)
        output, error = cls._proc.communicate()
        if error is not None:
            raise cls.Error(error)
        return output

    @classmethod
    def connect(cls, service, name):
        cmd = "keepsake-unlock %s %s" % (service, name)
        cls._proc = Popen(cls._term % cmd, shell=True)
        output, error = cls._proc.communicate()
        if error is not None:
            raise cls.Error(error)
        return output

    @classmethod
    def decrypt(cls):
        cls._proc = Popen(cls._term % cls.SCRIPT_DECRYPT, shell=True)
        output, error = cls._proc.communicate()
        if error is not None:
            raise cls.Error(error)
        return output

    @classmethod
    def encrypt(cls):
        cls._proc = Popen(cls._term % cls.SCRIPT_ENCRYPT, shell=True)
        output, error = cls._proc.communicate()
        if error is not None:
            raise cls.Error(error)
        return output

    @classmethod
    def passkey(cls, name):
        cls._proc = Popen([cls.PROGRAM_NAME], stdin=PIPE, stdout=PIPE)
        output, error = cls._proc.communicate(input=name)
        if error is not None:
            raise cls.Error(error)
        return output
