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

from keepsake.gui.dialog.create_server import CreateServerDialog
from keepsake.gui.dialog.update_server import UpdateServerDialog

from keepsake.gui.misc.records import Records


class CredentialsPanel(wx.Panel):

    headers = (
        ("Hash", 80),
        ("Bounce", 80),
        ("Service", 160),
        ("Host", 180),
        ("User", 140),
        ("Name", 160),
    )

    toolbar = None
    list_view = None

    records = None
    records_list = []

    def __init__(self, parent):
        super(self.__class__, self).__init__(parent=parent)
        self.parent = parent
        self.records = Records()
        self.records.flush()  # reset Records memory
        self.reinitialize()
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.create_toolbar(), 0, wx.EXPAND | wx.ALL, 1)
        self.main_sizer.Add(self.create_listview(), 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizerAndFit(self.main_sizer)
        self.Show(True)

    def get_icon(self, name):
        return os.path.join(__project__, "icons/{}.png".format(name))

    def reinitialize(self):
        self.records.refresh_records()
        for name, server in self.records.get_records().iteritems():
            self.records_list.append(server)

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
        self.populate_listview()
        return vsizer

    def clear_listview(self):
        while len(self.records_list) > 0:
            idx = len(self.records_list) - 1
            self.list_view.DeleteItem(idx)
            self.records_list.pop(idx)

    def populate_listview(self):
        for index, record in enumerate(self.records_list):
            self.add_listview_item(index, record)

    def add_listview_item(self, index, record):
        idx = self.list_view.InsertStringItem(index, record.name)
        self.list_view.SetStringItem(idx, 0, record.auth_signature)
        bounce = "No"
        if record.jump_signature != self.records.get_unlocker().SELF_BOUNCE:
            bounce = "Yes"
        self.list_view.SetStringItem(idx, 1, bounce)
        service = "{} ({})".format(record.port, record.scheme)
        self.list_view.SetStringItem(idx, 2, service)
        self.list_view.SetStringItem(idx, 3, record.host)
        self.list_view.SetStringItem(idx, 4, record.user)
        self.list_view.SetStringItem(idx, 5, record.name)

    def del_listview_item(self, index):
        self.list_view.DeleteItem(index)

    def create_toolbar(self):
        self.toolbar = wx.ToolBar(self)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.toolbar, 1, wx.EXPAND)
        self.connect_server = self.toolbar.AddLabelTool(
            wx.ID_ANY, "Connect...", wx.Bitmap(self.get_icon("utilities")),
            shortHelp="Connect to server")
        self.toolbar.AddSeparator()
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
        self.import_records = self.toolbar.AddLabelTool(
            wx.ID_ANY, "Import...", wx.Bitmap(self.get_icon("upload")),
            shortHelp="Import servers from disk")
        self.export_records = self.toolbar.AddLabelTool(
            wx.ID_ANY, "Export...", wx.Bitmap(self.get_icon("download")),
            shortHelp="Export servers on disk")
        self.toolbar.AddSeparator()
        self.install_scripts = self.toolbar.AddLabelTool(
            wx.ID_ANY, "Install", wx.Bitmap(self.get_icon("hwinfo")),
            shortHelp="Install additional tools")
        self.toolbar.AddSeparator()
        self.encrypt_records = self.toolbar.AddLabelTool(
            wx.ID_ANY, "Encrypt", wx.Bitmap(self.get_icon("encrypt")),
            shortHelp="Encrypt secrets")
        self.decrypt_records = self.toolbar.AddLabelTool(
            wx.ID_ANY, "Decrypt", wx.Bitmap(self.get_icon("decrypt")),
            shortHelp="Decrypt secrets")
        self.Bind(wx.EVT_TOOL, self.bind_connect_button, self.connect_server)
        self.Bind(wx.EVT_TOOL, self.bind_add_button, self.add_record)
        self.Bind(wx.EVT_TOOL, self.bind_remove_button, self.remove_record)
        self.Bind(wx.EVT_TOOL, self.bind_update_button, self.update_record)
        self.Bind(wx.EVT_TOOL, self.bind_refresh_button, self.refresh_view)
        self.toolbar.EnableTool(self.connect_server.GetId(), False)
        self.toolbar.EnableTool(self.remove_record.GetId(), False)
        self.toolbar.EnableTool(self.update_record.GetId(), False)
        self.toolbar.EnableTool(self.install_scripts.GetId(), False)
        self.toolbar.EnableTool(self.import_records.GetId(), False)
        self.toolbar.EnableTool(self.export_records.GetId(), False)
        self.toolbar.EnableTool(self.encrypt_records.GetId(), False)
        self.toolbar.EnableTool(self.decrypt_records.GetId(), False)
        self.toolbar.Realize()
        return hsizer

    def display_message(self, message=None, title=None):
        dlg = wx.MessageDialog(
            self, message, title, wx.OK | wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()

    def on_item_selected(self, event):
        self.current_index = event.GetIndex()
        self.current_record = self.records_list[self.current_index]
        self.toolbar.EnableTool(self.connect_server.GetId(), True)
        self.toolbar.EnableTool(self.remove_record.GetId(), True)
        self.toolbar.EnableTool(self.update_record.GetId(), True)

    def bind_refresh_button(self, event):
        dlg = wx.ProgressDialog(
            "Please wait", "Updating known servers...",
            maximum=5, parent=self, style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)
        count = 0
        self.toolbar.EnableTool(self.connect_server.GetId(), False)
        self.toolbar.EnableTool(self.remove_record.GetId(), False)
        self.toolbar.EnableTool(self.update_record.GetId(), False)
        self.records.flush()
        self.clear_listview()
        wx.MilliSleep(250)  # list ctrl refresh delay
        self.reinitialize()
        self.populate_listview()
        self.list_view.Refresh()
        while count < 5:  # little over 1s
            count += 1
            wx.MilliSleep(250)
            wx.Yield()
            dlg.Update(count)
        dlg.Destroy()

    def bind_add_button(self, event):
        dlg = CreateServerDialog(self)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.last_server.auth is None:
                dlg.last_server.auth = "password"
            try:
                server = dlg.last_server.as_dict()
                record = self.records.append_record(**server)
                next_index = len(self.records_list)
                self.add_listview_item(next_index, record)
                self.records_list.append(record)
            except Exception as e:
                self.display_message("Cannot continue due to an error: %s" % e)
            finally:
                dlg.last_server = None  # nullify instance
        dlg.Destroy()

    def bind_remove_button(self, event):
        dialog = wx.MessageBox(
            "Are you sure you want to permanently remove server?",
            "Delete server", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dialog == wx.YES:
            self.records.remove_record(self.current_record)
            self.del_listview_item(self.current_index)
            self.records_list.pop(self.current_index)

    def bind_update_button(self, event):
        dlg = UpdateServerDialog(self, self.current_record)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.last_server.auth is None:
                dlg.last_server.auth = "password"
            try:
                self.records.update_record(self.current_record, dlg.last_server.auth)
            except Exception as e:
                self.display_message("Cannot continue due to an error: %s" % e)
            finally:
                dlg.last_server = None  # nullify instance
        dlg.Destroy()

    def bind_connect_button(self, event):
        service = self.current_record.scheme
        name = self.current_record.name
        dlg = wx.ProgressDialog(
            "Please wait", "Connecting to %s server..." % service,
            maximum=5, parent=self, style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)
        count = 0
        self.records.get_unlocker().connect(service, name)
        while count < 5:  # little over 1s
            count += 1
            wx.MilliSleep(250)
            wx.Yield()
            dlg.Update(count)
        dlg.Destroy()

    def bind_import_button(self, event):
        pass

    def bind_export_button(self, event):
        pass

    def bind_encrypt_button(self, event):
        pass

    def bind_decrypt_button(self, event):
        pass
