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

from subprocess import PIPE

from keepsake.util.misc import spawn_process, spawn_piped_process

from keepsake.util.safe_output import safe_output


class Unlocker(object):

    ROWS_PADDING = 2  # header and separator
    ROWS_SEPARATOR, COLS_SEPARATOR = "\n", "|"

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

    TERMINAL = "gnome-terminal -e '%s'"
    SHELL = "bash -c '%s'"
    KEEPSAKE_SCRIPT = "keepsake-unlock %s %s"

    @classmethod
    @safe_output
    def list(cls):
        out, err = spawn_process(cls.PROGRAM_NAME, cls.OPT_LIST, stdout=PIPE)
        if err:
            raise cls.Error(err)
        return out

    @classmethod
    def append(cls, name, host, port, user, auth, scheme, jump=None):
        if not auth:
            auth = "password"
        arguments = [cls.PROGRAM_NAME, cls.OPT_APPEND,
                     "--name", unicode(name), "--host", unicode(host),
                     "--port", unicode(port), "--user", unicode(user),
                     "--auth", unicode(auth), "--scheme", unicode(scheme)]
        if jump is not None and len(jump) > 0:
            arguments.append("--jump-server")
            arguments.append(jump)
        return spawn_process(cls.TERMINAL % " ".join(arguments))

    @classmethod
    def remove(cls, name):
        arguments = [cls.PROGRAM_NAME, cls.OPT_REMOVE,
                     "--name", unicode(name)]
        return spawn_process(cls.TERMINAL % " ".join(arguments))

    @classmethod
    def update(cls, name, auth, jump=None):
        arguments = [cls.PROGRAM_NAME, cls.OPT_UPDATE,
                     "--name", unicode(name), "--auth", unicode(auth)]
        if jump is not None and len(jump) > 0:
            arguments.append("--jump-server")
            arguments.append(jump)
        return spawn_process(cls.TERMINAL % " ".join(arguments))

    @classmethod
    def migrate_export(cls, filename, servers):
        arguments = [cls.PROGRAM_NAME, cls.OPT_MIGRATE,
                     "--export %s" % " ".join(servers), ">", unicode(filename)]
        return spawn_process(cls.SHELL % " ".join(arguments))

    @classmethod
    def migrate_import(cls, filename):
        arguments = [cls.PROGRAM_NAME, cls.OPT_MIGRATE,
                     "--import", "<", unicode(filename)]
        return spawn_process(cls.SHELL % " ".join(arguments))

    @classmethod
    def connect(cls, service, name):
        cmd = cls.KEEPSAKE_SCRIPT % (service, name)
        return spawn_process(cls.TERMINAL % cmd)

    @classmethod
    def decrypt(cls):
        return spawn_process(cls.TERMINAL % cls.SCRIPT_DECRYPT)

    @classmethod
    def encrypt(cls):
        return spawn_process(cls.TERMINAL % cls.SCRIPT_ENCRYPT)

    @classmethod
    def passkey(cls, name):
        out, err = spawn_piped_process(cls.PROGRAM_NAME, stdin=name)
        if err:
            raise cls.Error(err)
        return out
