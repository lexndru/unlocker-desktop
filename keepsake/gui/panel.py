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

from keepsake.gui.event.welcome import WelcomeEvent
from keepsake.gui.event.event_broker import EventBroker

from keepsake.gui.menu.main_menu import MainMenu

from keepsake.gui.toolbar.toolbar import Toolbar

from keepsake.gui.view.list.list_view import ListView
from keepsake.gui.view.detail.detail_view import DetailView

from keepsake.gui.misc.records import Records
from keepsake.gui.misc.scripts import Scripts


class CredentialsPanel(wx.Panel):

    bootloader = None

    notice_messages = []

    @classmethod
    def register_boot(cls, boot):
        cls.bootloader = boot

    def __init__(self, parent):
        super(self.__class__, self).__init__(parent=parent)
        self.parent = parent
        self.check_boot_alerts() and self.trigger_boot_alerts()
        if self.bootloader.first_run:
            we = WelcomeEvent(self)
            we.display_preferences()
        self.event_broker = self.init_live_events()
        self.toolbar = self.init_toolbar()
        self.scripts = self.init_scripts()
        self.records = self.init_records()
        self.records.flush()
        self.main_menu = self.init_main_menu()
        self.list_view = self.init_list_view()
        self.detail_view = self.init_detail_view()
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.toolbar.get_sizer(), 0, wx.EXPAND | wx.ALL, 1)
        self.main_sizer.Add(
            self.list_view.get_sizer(), 1, wx.EXPAND | wx.ALL, 1)
        self.main_sizer.Add(self.detail_view.get_sizer(), 0, wx.ALL, 5)
        self.main_sizer.Add(wx.StaticLine(self, wx.ID_ANY), 0, wx.EXPAND, 1)
        self.SetSizerAndFit(self.main_sizer)
        self.Show(True)

    def init_toolbar(self):
        Toolbar.register_boot(self.bootloader)
        Toolbar.register_event_broker(self.event_broker)
        return Toolbar(self)

    def init_live_events(self):
        return EventBroker(self)

    def init_main_menu(self):
        MainMenu.register_boot(self.bootloader)
        MainMenu.register_event_broker(self.event_broker)
        return MainMenu(self.parent)

    def init_detail_view(self):
        return DetailView(self)

    def init_list_view(self):
        ListView.register_event_broker(self.event_broker)
        return ListView(self)

    def init_scripts(self):
        return Scripts()

    def init_records(self):
        return Records()

    def get_menu(self):
        return self.main_menu

    def get_toolbar(self):
        return self.toolbar

    def get_detail_view(self):
        return self.detail_view

    def get_list_view(self):
        return self.list_view

    def get_records(self):
        return self.records

    def get_scripts(self):
        return self.scripts

    def get_servers(self):
        return self.records.get_records().itervalues()

    def display_message(self, message=None, title="Notice"):
        dlg = wx.MessageDialog(
            self, message, title, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def history(self, *messages):
        self.parent.history(" ".join(messages))

    def check_boot_alerts(self):
        if self.bootloader.secrets_encryption:
            notice = "Keepsake cannot access encrypted data! " \
                     "Please decrypt first and then refresh records list."
            self.notice_messages.append(notice)
        elif not self.bootloader.secrets_status:
            notice = "Keepsake cannot find data! Maybe initialize first?"
            self.notice_messages.append(notice)
        if not self.bootloader.keepsake_status:
            notice = "Keepsake helper scripts are not deployed! " \
                     "Reinstalling may fix this, otherwise open " \
                     "a terminal and \"keepsake fix\"."
            self.notice_messages.append(notice)
        if not self.bootloader.unlocker_status:
            notice = "Keepsake requires Unlocker to be installed! " \
                     "Open a terminal and \"pip install unlocker\""
            self.notice_messages.append(notice)
        if not self.bootloader.unlocker_scripts:
            notice = "Keepsake requires Unlocker scripts to be deployed! " \
                     "Open a terminal and \"unlocker install\""
            self.notice_messages.append(notice)
        return len(self.notice_messages) > 0

    def trigger_boot_alerts(self):
        problems = len(self.notice_messages)
        notice = "Found %d problem(s) during bootload:" % problems
        for msg in self.notice_messages:
            notice += "\n- %s" % msg
        self.display_message(notice)
        self.parent.history("%s ..." % notice[:-1])
