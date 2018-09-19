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
import re

CHARS = "0123456789"


class PortValidator(wx.PyValidator):

    valid_format = re.compile(r"\d{1,5}", re.I | re.U)

    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def TransferToWindow(self):
        return True  # Prevent wxDialog from complaining.

    def TransferFromWindow(self):
        return True  # Prevent wxDialog from complaining.

    def Clone(self):
        return PortValidator()

    def Validate(self, win):
        tc = self.GetWindow()
        if self.valid_format.match(tc.GetValue()) is None:
            error = "You have typed an invalid port. Accepted values are " \
                    "from 1 to 65535"
            wx.MessageBox(error, "Invalid port")
            tc.SetBackgroundColour("pink")
            tc.SetFocus()
            tc.Refresh()
            return False
        bg_color = wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW)
        tc.SetBackgroundColour(bg_color)
        tc.Refresh()
        return True

    def OnChar(self, event):
        key = event.GetKeyCode()
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        if chr(key) in CHARS:
            event.Skip()
            return
        if not wx.Validator_IsSilent():
            wx.Bell()
        return
