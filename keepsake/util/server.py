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

SERVER_FMT = u"[scheme={scheme} " \
             u"name={name} " \
             u"host={host} " \
             u"port={port} " \
             u"user={user} " \
             u"auth={auth} " \
             u"jump={jump}]"


class ServerTemplate(dict):

    def __init__(self):
        self.name, self.auth = None, None
        self.scheme, self.user, self.host, self.port = None, None, None, None
        self.jump = None

    def as_dict(self):
        return dict(auth=self.get_auth().strip(),
                    name=self.get_name().strip(),
                    host=self.get_host().strip(),
                    port=self.get_port().strip(),
                    user=self.get_user().strip(),
                    jump=self.get_jump().strip(),
                    scheme=self.get_scheme().strip())

    def __repr__(self):
        return SERVER_FMT.format(
                auth=self.get_auth(),
                name=self.get_name(),
                host=self.get_host(),
                port=self.get_port(),
                user=self.get_user(),
                jump=self.get_jump(),
                scheme=self.get_scheme())

    def get_auth(self):
        return self.auth

    def get_name(self):
        return self.name.GetValue()

    def get_host(self):
        return self.host.GetValue()

    def get_port(self):
        return self.port.GetValue()

    def get_user(self):
        return self.user.GetValue()

    def get_jump(self):
        return self.jump.GetValue()

    def get_scheme(self):
        return self.scheme.GetValue()
