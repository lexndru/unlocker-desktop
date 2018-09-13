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

import os
import wx

from keepsake import __project__

from keepsake.unlocker import Unlocker

from keepsake.gui.dialog.create_server import CreateServerDialog
from keepsake.gui.dialog.update_server import UpdateServerDialog


class CredentialsPanel(wx.Panel):

    headers = (
        ("Protocol", 160),
        ("Host", 180),
        ("User", 160),
        ("IPv4", 120),
        ("Name", 160),
        ("Hash", 80),
        ("Jump", 80),
    )

    toolbar = None
    list_view = None
    list_index = 0

    current_index, current_item = -1, None
    temp_storage, known_servers = {}, {}

    def __init__(self, parent):
        super(self.__class__, self).__init__(parent=parent)
        self.parent = parent
        self.reinitialize()
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.create_toolbar(), 0, wx.EXPAND | wx.ALL, 1)
        self.main_sizer.Add(self.create_listview(), 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizerAndFit(self.main_sizer)
        self.Show(True)

    def get_icon(self, name):
        return os.path.join(__project__, "icons/{}.png".format(name))

    def reinitialize(self):
        results = Unlocker.list().split("\n")
        for line in results[2:]:
            if not line:
                continue
            sig, jsig, scheme, ip4, port, host, user, name = line.split("|", 8)
            if name in self.known_servers:
                continue
            server = (
                host.strip(),
                user.strip(),
                ip4.strip(),
                port.strip(),
                scheme.strip(),
                sig.strip(),
                jsig.strip())
            self.temp_storage.update({name: server})

    def create_listview(self):
        options = {"style": wx.LC_REPORT | wx.BORDER_SUNKEN}
        self.list_view = wx.ListCtrl(self, **options)
        vsizer = wx.BoxSizer(wx.VERTICAL)
        vsizer.Add(self.list_view, 1, wx.EXPAND)
        for idx, header in enumerate(self.headers):
            name, width = header
            self.list_view.InsertColumn(idx, name, wx.LIST_FORMAT_CENTER)
            self.list_view.SetColumnWidth(idx, width)
        self.list_view.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_item_selected)
        self.refresh_listview()
        return vsizer

    def append_item_list(self, protocol, host, user, ipv4, name, sig, jsig):
        self.list_index += 1
        idx = self.list_view.InsertStringItem(self.list_index, protocol)
        self.list_view.SetStringItem(idx, 0, protocol)
        self.list_view.SetStringItem(idx, 1, host)
        self.list_view.SetStringItem(idx, 2, user)
        self.list_view.SetStringItem(idx, 3, ipv4)
        self.list_view.SetStringItem(idx, 4, name)
        self.list_view.SetStringItem(idx, 5, sig)
        self.list_view.SetStringItem(idx, 6, jsig)

    def refresh_listview(self):
        for name, server in self.temp_storage.iteritems():
            host, user, ipv4, port, scheme, sig, jsig = server
            protocol = u"{}/{}".format(scheme, port)
            self.append_item_list(protocol, host, user, ipv4, name, sig, jsig)
            self.known_servers.update({name: self.list_index})
        self.temp_storage = {}  # reset storage

    def create_toolbar(self):
        self.toolbar = wx.ToolBar(self)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.toolbar, 1, wx.EXPAND)
        self.add_record = self.toolbar.AddLabelTool(
            wx.ID_ANY, "Add new server", wx.Bitmap(self.get_icon("add")),
            shortHelp="Append new passkey credentials")
        self.remove_record = self.toolbar.AddLabelTool(
            wx.ID_ANY, "Remove server", wx.Bitmap(self.get_icon("delete")),
            shortHelp="Remove passkey credentials")
        self.update_record = self.toolbar.AddLabelTool(
            wx.ID_ANY, "Update server", wx.Bitmap(self.get_icon("edit")),
            shortHelp="Update passkey or bounce server")
        self.toolbar.AddSeparator()
        self.refresh_view = self.toolbar.AddLabelTool(
            wx.ID_ANY, "Refresh", wx.Bitmap(self.get_icon("reboot")),
            shortHelp="Update list of known servers")
        self.toolbar.AddSeparator()
        self.Bind(wx.EVT_TOOL, self.bind_add_button, self.add_record)
        self.Bind(wx.EVT_TOOL, self.bind_remove_button, self.remove_record)
        self.Bind(wx.EVT_TOOL, self.bind_update_button, self.update_record)
        self.Bind(wx.EVT_TOOL, self.bind_refresh_button, self.refresh_view)
        self.toolbar.EnableTool(self.remove_record.GetId(), False)
        self.toolbar.EnableTool(self.update_record.GetId(), False)
        self.toolbar.Realize()
        return hsizer

    def display_message(self, message=None, title=None):
        dlg = wx.MessageDialog(
            self, message, title, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def on_item_selected(self, event):
        self.current_index = event.GetIndex()
        self.current_item = event.GetItem()
        self.toolbar.EnableTool(self.remove_record.GetId(), True)
        self.toolbar.EnableTool(self.update_record.GetId(), True)

    def bind_add_button(self, event):
        dlg = CreateServerDialog(self)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.last_server.auth is None:
                dlg.last_server.auth = "password"
            try:
                server = dlg.last_server.as_dict()
                Unlocker.append(**server)
            except Unlocker.Error as e:
                self.display_message("Cannot continue due to an error: %s" % e)
            finally:
                dlg.last_server = None  # nullify instance
        dlg.Destroy()

    def bind_remove_button(self, event):
        dialog = wx.MessageBox(
            "Are you sure you want to permanently remove server?",
            "Delete server", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dialog == wx.YES:
            for name, idx in self.known_servers.iteritems():
                if idx == self.current_index + 1:
                    Unlocker.remove(name.strip())
                    break
            self.list_view.DeleteItem(self.current_index)

    def bind_update_button(self, event):
        current_server = None
        for name, idx in self.known_servers.iteritems():
            if idx == self.current_index + 1:
                current_server = name
                break
        else:
            error = "Cannot find the server to update. Try restarting the " \
                    "application"
            wx.MessageBox(error, "No server to update")
            return
        dlg = UpdateServerDialog(self, name)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.last_server.auth is None:
                dlg.last_server.auth = "password"
            try:
                Unlocker.update(current_server, dlg.last_server.auth)
            except Unlocker.Error as e:
                self.display_message("Cannot continue due to an error: %s" % e)
            finally:
                dlg.last_server = None  # nullify instance
        dlg.Destroy()

    def bind_refresh_button(self, event):
        dlg = wx.ProgressDialog(
            "Please wait", "Updating known servers...",
            maximum=5, parent=self, style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)
        count = 0
        self.reinitialize()
        self.refresh_listview()
        self.list_view.Refresh()
        while count < 5:  # little over 1s
            count += 1
            wx.MilliSleep(250)
            wx.Yield()
            dlg.Update(count)
        dlg.Destroy()
