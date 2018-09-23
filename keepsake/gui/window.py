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
import os

from keepsake import __project__

FRAME_CONFIG = {
    "title": "Keepsake Desktop",
    "size": (860, 440),
    # "style": wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.CAPTION
}


class SingleMainWindow(wx.Frame):

    def __init__(self, panel):
        super(self.__class__, self).__init__(parent=None, **FRAME_CONFIG)
        self.set_icon(os.path.join(__project__, "icons", "app-icon.png"))
        self.menubar = wx.MenuBar()
        self.SetMinSize(self.GetSize())
        self.SetMenuBar(self.menubar)
        self.statusbar = self.CreateStatusBar()
        self.panel = panel(self)
        self.Centre()
        self.Show()

    def history(self, event_message):
        self.statusbar.SetStatusText(event_message)

    def set_icon(self, icon_name):
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap(icon_name, wx.BITMAP_TYPE_ANY))
        self.SetIcon(icon)
