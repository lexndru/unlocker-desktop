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


class PreferencesDialog(wx.Dialog):

    unlocker_versions = [
        "v2.2.0"
    ]

    terminals = [
        "XTerm",
        "GNOME Terminal",
        "Konsole",
        "Terminator",
        "Guake",
        "Tilda",
    ]

    shells = [
        "sh",
        "bash",
        "tcsh",
        "ksh",
        "csh",
        "zsh",
    ]

    def __init__(self, parent):
        self.parent = parent
        self.dlg = wx.PreDialog()
        self.dlg.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.dlg.Create(parent, wx.ID_ANY, "Preferences",
                        pos=wx.DefaultPosition, size=(300, 300),
                        style=wx.DEFAULT_DIALOG_STYLE)
        self.PostCreate(self.dlg)
        sizer = wx.BoxSizer(wx.VERTICAL)

        # unlocker version
        unlocker_label = wx.StaticText(self, -1, "Unlocker:", size=(100, -1))
        unlocker = wx.Choice(
            self, wx.ID_ANY, choices=self.unlocker_versions, size=(200, -1))
        unlocker.SetSelection(0)
        unlocker.Enable(False)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(unlocker_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        row.Add(unlocker, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer.Add(row, 0,  wx.ALL, 5)

        # terminal
        terminal_label = wx.StaticText(self, -1, "Terminal:", size=(100, -1))
        terminal = wx.Choice(
            self, wx.ID_ANY, choices=self.terminals, size=(200, -1))
        terminal.SetSelection(1)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(terminal_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        row.Add(terminal, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer.Add(row, 0,  wx.ALL, 5)

        # shell
        shell_label = wx.StaticText(self, -1, "Shell:", size=(100, -1))
        shell = wx.Choice(
            self, wx.ID_ANY, choices=self.shells, size=(200, -1))
        shell.SetSelection(1)
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(shell_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        row.Add(shell, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer.Add(row, 0, wx.ALL, 5)

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
