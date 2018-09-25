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

from keepsake.unlocker import Unlocker


class PreferencesDialog(wx.Dialog):

    unlocker_versions = [
        "v2.2.0"
    ]

    terminals = [
        ("XTerm", "xterm -e '%s'"),
        ("GNOME Terminal", "gnome-terminal -e '%s'"),
        ("Konsole", "konsole -e '%s'"),
        ("Terminator", "terminator -e '%s'"),
        ("Guake", "guake -e '%s'"),
        ("Tilda", "tilda -e '%s'"),
    ]

    shells = [
        ("sh", "sh -c '%s'"),
        ("bash", "bash -c '%s'"),
        ("dash", "dash -c '%s'"),
        ("tcsh", "tcsh -c '%s'"),
        ("ksh", "ksh -c '%s'"),
        ("csh", "csh -c '%s'"),
        ("zsh", "zsh -c '%s'"),
    ]

    def __init__(self, panel):
        self.panel = panel
        self.dlg = wx.PreDialog()
        self.dlg.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        self.dlg.Create(panel, wx.ID_ANY, "Preferences",
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
        terminals_list = [i[0] for i in self.terminals]
        terminal_label = wx.StaticText(self, -1, "Terminal:", size=(100, -1))
        self.terminal = wx.Choice(
            self, wx.ID_ANY, choices=terminals_list, size=(200, -1))
        self.terminal.SetSelection(self.find_active_terminal_option())
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(terminal_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        row.Add(self.terminal, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        sizer.Add(row, 0,  wx.ALL, 5)

        # shell
        shells_list = [i[0] for i in self.shells]
        shell_label = wx.StaticText(self, -1, "Shell:", size=(100, -1))
        self.shell = wx.Choice(
            self, wx.ID_ANY, choices=shells_list, size=(200, -1))
        self.shell.SetSelection(self.find_active_shell_option())
        row = wx.BoxSizer(wx.HORIZONTAL)
        row.Add(shell_label, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
        row.Add(self.shell, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)
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

    def find_active_shell_option(self):
        return self.find_preselected_option(self.shells, Unlocker.SHELL)

    def find_active_terminal_option(self):
        return self.find_preselected_option(self.terminals, Unlocker.TERMINAL)

    def find_preselected_option(self, options, active):
        for index, row in enumerate(options):
            _, cmd = row
            if active == cmd:
                return index
        if len(options) > 0:
            return 1
        return 0

    def get_shell(self):
        return self.read_shell_by_index(self.shell.GetSelection())

    def read_shell_by_index(self, index):
        if not isinstance(index, int) or index >= len(self.shells):
            error_msg = "Unable to find shell. Either it's missing from " \
                        "the configuration file or a selection error occurred."
            dlg = wx.MessageDialog(
                self, error_msg, "Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return
        _, cmd = self.shells[index]
        return cmd

    def get_terminal(self):
        return self.read_terminal_by_index(self.terminal.GetSelection())

    def read_terminal_by_index(self, index):
        if not isinstance(index, int) or index >= len(self.terminals):
            error_msg = "Unable to find terminal. Either it's missing from " \
                        "the configuration file or a selection error occurred."
            dlg = wx.MessageDialog(
                self, error_msg, "Error", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
            return
        _, cmd = self.terminals[index]
        return cmd
