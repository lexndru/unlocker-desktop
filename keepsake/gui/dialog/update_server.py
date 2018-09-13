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

from keepsake.util.server import ServerTemplate


class UpdateServerDialog(wx.Dialog):

    last_server = None

    def __init__(self, parent, name):
        self.dlg = wx.PreDialog()
        self.dlg.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.dlg.Create(parent, wx.ID_ANY, "Update authentication on server",
                        pos=wx.DefaultPosition, size=(300, 200),
                        style=wx.DEFAULT_DIALOG_STYLE)
        self.PostCreate(self.dlg)
        self.last_server = ServerTemplate()
        sizer = wx.BoxSizer(wx.VERTICAL)

        # sizer for the server name
        pre_row = wx.BoxSizer(wx.HORIZONTAL)

        # name label
        name_label = wx.StaticText(self, -1, "Name:", size=(50, -1))
        pre_row.Add(name_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # set name input field
        name_field = wx.TextCtrl(self, -1, name, size=(250, -1),
                                 style=wx.TE_READONLY)
        name_field.Disable()
        pre_row.Add(name_field, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer.Add(pre_row, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # add separator
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.TOP, 5)

        # ask for authentication method
        auth_row = wx.BoxSizer(wx.VERTICAL)

        options = ["Store a password", "Store a private key"]
        auth_option = wx.RadioBox(
            self, -1, "Authentication method", wx.DefaultPosition,
            (300, -1), options, 1, wx.RA_SPECIFY_COLS)
        self.Bind(wx.EVT_RADIOBOX, self.bind_auth_option, auth_option)
        auth_row.Add(auth_option, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        # add auth row
        sizer.Add(auth_row, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # add separator
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.TOP, 5)

        # sizer for the server bounce
        post_row = wx.BoxSizer(wx.HORIZONTAL)

        # create name label
        jump_label = wx.StaticText(self, -1, "Jump:", size=(50, -1))
        post_row.Add(jump_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # create name input field
        self.last_server.jump = wx.TextCtrl(self, -1, "", size=(250, -1))
        post_row.Add(self.last_server.jump, 0,
                     wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # add post row
        sizer.Add(post_row, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # add separator
        line = wx.StaticLine(self, -1, size=(20, -1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW | wx.ALIGN_CENTER_VERTICAL | wx.TOP, 5)

        # buttons sizer
        btn_sizer = wx.StdDialogButtonSizer()

        # add ok button
        btn_ok = wx.Button(self, wx.ID_OK)
        btn_ok.SetDefault()
        btn_sizer.AddButton(btn_ok)

        btn_cancel = wx.Button(self, wx.ID_CANCEL)
        btn_sizer.AddButton(btn_cancel)

        # display buttons
        btn_sizer.Realize()
        sizer.Add(btn_sizer, 0,
                  wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.ALL, 5)

        # render dialog
        self.SetSizer(sizer)
        sizer.Fit(self)

    def bind_auth_option(self, event):
        if event.GetInt() == 0:
            self.last_server.auth = "password"
        elif event.GetInt() == 1:
            self.last_server.auth = "privatekey"
        else:
            raise Exception("Unsupported auth option: %r" % event.GetInt())
