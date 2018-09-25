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

from keepsake.gui.dialog.preferences import PreferencesDialog

from keepsake.util.settings import Settings

from keepsake.unlocker import Unlocker


class WelcomeEvent(object):

    def __init__(self, panel):
        self.panel = panel

    def display_preferences(self):
        sett = Settings()
        pref = PreferencesDialog(self.panel)
        pref.CenterOnScreen()
        val = pref.ShowModal()
        if val == wx.ID_OK:
            sett.update(pref.get_shell(), pref.get_terminal())
            Unlocker.SHELL = pref.get_shell()
            Unlocker.TERMINAL = pref.get_terminal()
        else:
            sett.read_or_init()
        pref.Destroy()
        style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
        dlg = wx.ProgressDialog("Please wait", "Saving preferences...",
                                maximum=5, parent=self.panel, style=style)
        wx.MilliSleep(250)  # dummy
        wx.Yield()
        dlg.Destroy()
