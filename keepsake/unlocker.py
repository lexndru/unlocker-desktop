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

from subprocess import Popen, PIPE

from keepsake.util.safe_output import safe_output


class Unlocker(object):

    PROGRAM_NAME = "unlocker"

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

    class Error(Exception):
        pass

    @classmethod
    @safe_output
    def list(cls):
        proc = Popen([cls.PROGRAM_NAME, cls.OPT_LIST], stdout=PIPE)
        output, error = proc.communicate()
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
        command = "gnome-terminal -e '%s'" % " ".join(arguments)
        proc = Popen(command, shell=True)
        output, error = proc.communicate()
        if error is not None:
            raise cls.Error(error)
        return output

    @classmethod
    def remove(cls, name):
        arguments = [cls.PROGRAM_NAME, cls.OPT_REMOVE, "--name", unicode(name)]
        command = "gnome-terminal -e '%s'" % " ".join(arguments)
        proc = Popen(command, shell=True)
        output, error = proc.communicate()
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
        command = "gnome-terminal -e '%s'" % " ".join(arguments)
        print command
        proc = Popen(command, shell=True)
        output, error = proc.communicate()
        print output, error
        if error is not None:
            raise cls.Error(error)
        return output
