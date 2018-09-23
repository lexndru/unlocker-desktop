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
import sys


class JumpServerDialog(wx.Dialog):

    selected_jump_server = None

    headers = (
        ("Name", 180),
        ("User", 140),
        ("Host", 180),
        ("Port", 60),
    )

    def __init__(self, parent, record_name=None):
        self.parent = parent
        self.dlg = wx.PreDialog()
        self.dlg.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.dlg.Create(parent, wx.ID_ANY, "Choose jump server",
                        pos=wx.DefaultPosition, size=(300, 500),
                        style=wx.DEFAULT_DIALOG_STYLE)
        self.PostCreate(self.dlg)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # create label
        if record_name is None:
            record_name = self.parent.last_server.get_name()
        text_title = "Select a jump server for %s" % record_name
        title = wx.StaticText(self, -1, text_title, size=(300, -1))
        sizer.Add(title, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

        # add list of servers
        self.servers = []
        jump_list = wx.ListCtrl(self, style=wx.LC_REPORT | wx.BORDER_SUNKEN)
        sizer.Add(jump_list, 1, wx.EXPAND | wx.ALL, 5)
        for idx, header in enumerate(self.headers):
            name, width = header
            jump_list.InsertColumn(idx, name, wx.LIST_FORMAT_CENTER)
            jump_list.SetColumnWidth(idx, width)
        jump_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        for record in self.parent.panel.get_servers():
            if record.scheme != "ssh":
                continue
            idx = jump_list.InsertStringItem(sys.maxint, record.name)
            jump_list.SetStringItem(idx, 0, record.name)
            jump_list.SetStringItem(idx, 1, record.user)
            jump_list.SetStringItem(idx, 2, record.host)
            jump_list.SetStringItem(idx, 3, record.port)
            self.servers.append(record)

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

    def on_item_selected(self, event):
        self.selected_jump_server = self.servers[event.GetIndex()]
