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

import wx


class DetailView(object):

    def __init__(self, panel):
        self.panel = panel
        self.current_record = None

    def get_record(self):
        return self.current_record

    def get_sizer(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # record details (name, bounce, connection hash)
        st_record = wx.StaticBox(self.panel, wx.ID_ANY, "Record details")
        sb_record = wx.StaticBoxSizer(st_record, wx.VERTICAL)
        sizer.Add(sb_record, 0, wx.EXPAND | wx.ALL, 5)

        # connection details (protocol, host, ip, port, user)
        st_connection = wx.StaticBox(self.panel, wx.ID_ANY,
                                     "Connection details")
        sb_connection = wx.StaticBoxSizer(st_connection, wx.VERTICAL)
        sizer.Add(sb_connection, 0, wx.EXPAND | wx.ALL, 5)

        # display record name
        static = wx.StaticText(self.panel, wx.ID_ANY, "Name:",
                               size=(100, -1), style=wx.ALIGN_RIGHT)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(static)
        row.Add((0, 0), proportion=1)
        self.detail_record_name = wx.StaticText(
            self.panel, wx.ID_ANY, "n/a", size=(200, -1))
        row.Add(self.detail_record_name)
        sb_record.Add(row, 0, wx.EXPAND | wx.ALL, 2)

        # display record hash
        static = wx.StaticText(self.panel, wx.ID_ANY, "Hash:",
                               size=(100, -1), style=wx.ALIGN_RIGHT)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(static)
        row.Add((0, 0), proportion=1)
        self.detail_record_hash = wx.StaticText(
            self.panel, wx.ID_ANY, "n/a", size=(200, -1))
        row.Add(self.detail_record_hash)
        sb_record.Add(row, 0, wx.EXPAND | wx.ALL, 2)

        # display record jump
        static = wx.StaticText(self.panel, wx.ID_ANY, "Bounce:",
                               size=(100, -1), style=wx.ALIGN_RIGHT)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(static)
        row.Add((0, 0), proportion=1)
        self.detail_record_jump = wx.StaticText(
            self.panel, wx.ID_ANY, "n/a", size=(200, -1))
        row.Add(self.detail_record_jump)
        sb_record.Add(row, 0, wx.EXPAND | wx.ALL, 2)

        # display connection protocol and port
        static = wx.StaticText(self.panel, wx.ID_ANY, "Protocol:",
                               size=(100, -1), style=wx.ALIGN_RIGHT)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(static)
        row.Add((0, 0), proportion=1)
        self.detail_connection_protocol = wx.StaticText(
            self.panel, wx.ID_ANY, "n/a", size=(400, -1))
        row.Add(self.detail_connection_protocol)
        sb_connection.Add(row, 0, wx.EXPAND | wx.ALL, 2)

        # display connection host and ip
        static = wx.StaticText(self.panel, wx.ID_ANY, "Hostname:",
                               size=(100, -1), style=wx.ALIGN_RIGHT)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(static)
        row.Add((0, 0), proportion=1)
        self.detail_connection_hostname = wx.StaticText(
            self.panel, wx.ID_ANY, "n/a", size=(400, -1))
        row.Add(self.detail_connection_hostname)
        sb_connection.Add(row, 0, wx.EXPAND | wx.ALL, 2)

        # display connection username
        static = wx.StaticText(self.panel, wx.ID_ANY, "Username:",
                               size=(100, -1), style=wx.ALIGN_RIGHT)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(static)
        row.Add((0, 0), proportion=1)
        self.detail_connection_username = wx.StaticText(
            self.panel, wx.ID_ANY, "n/a", size=(400, -1))
        row.Add(self.detail_connection_username)
        sb_connection.Add(row, 0, wx.EXPAND | wx.ALL, 2)

        return sizer

    def update(self, record):
        self.detail_record_name.SetLabel(record.name)
        self.detail_record_hash.SetLabel(record.auth_signature)
        self.detail_record_jump.SetLabel(record.jump_signature)
        self.detail_connection_username.SetLabel(record.user)
        hostname = "%s (%s)" % (record.host, record.ipv4)
        self.detail_connection_hostname.SetLabel(hostname)
        protocol = "%s (%s)" % (record.scheme, record.port)
        self.detail_connection_protocol.SetLabel(protocol)
        self.current_record = record
