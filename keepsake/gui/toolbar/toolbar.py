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


class Toolbar(object):

    bootloader = None
    event = None

    @classmethod
    def register_boot(cls, loader):
        cls.bootloader = loader

    @classmethod
    def register_event_broker(cls, broker):
        cls.event = broker

    def __init__(self, panel):
        self.panel = panel

    def get_icon(self, name):
        return os.path.join(__project__, "icons", "{}.png".format(name))

    def create_toolbar(self):
        self.toolbar = wx.ToolBar(self.panel)
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
            wx.ID_ANY, "Refresh", wx.Bitmap(self.get_icon("refresh")),
            shortHelp="Update list of known servers")
        self.toolbar.AddSeparator()
        self.import_records = self.toolbar.AddLabelTool(
            wx.ID_ANY, "Import...", wx.Bitmap(self.get_icon("upload")),
            shortHelp="Import servers from disk")
        self.export_records = self.toolbar.AddLabelTool(
            wx.ID_ANY, "Export...", wx.Bitmap(self.get_icon("download")),
            shortHelp="Export servers on disk")
        self.toolbar.AddSeparator()
        self.encrypt_records = self.toolbar.AddLabelTool(
            wx.ID_ANY, "Encrypt", wx.Bitmap(self.get_icon("encrypt")),
            shortHelp="Encrypt secrets")
        self.decrypt_records = self.toolbar.AddLabelTool(
            wx.ID_ANY, "Decrypt", wx.Bitmap(self.get_icon("decrypt")),
            shortHelp="Decrypt secrets")
        self.panel.Bind(
            wx.EVT_TOOL, self.event.bind_connect_button, self.connect_server)
        self.panel.Bind(
            wx.EVT_TOOL, self.event.bind_add_button, self.add_record)
        self.panel.Bind(
            wx.EVT_TOOL, self.event.bind_remove_button, self.remove_record)
        self.panel.Bind(
            wx.EVT_TOOL, self.event.bind_update_button, self.update_record)
        self.panel.Bind(
            wx.EVT_TOOL, self.event.bind_refresh_button, self.refresh_view)
        self.panel.Bind(
            wx.EVT_TOOL, self.event.bind_import_button, self.import_records)
        self.panel.Bind(
            wx.EVT_TOOL, self.event.bind_export_any_button,
            self.export_records)
        self.panel.Bind(
            wx.EVT_TOOL, self.event.bind_encrypt_button, self.encrypt_records)
        self.panel.Bind(
            wx.EVT_TOOL, self.event.bind_decrypt_button, self.decrypt_records)
        self.toolbar.EnableTool(self.connect_server.GetId(), False)
        self.toolbar.EnableTool(self.remove_record.GetId(), False)
        self.toolbar.EnableTool(self.update_record.GetId(), False)
        if self.bootloader.secrets_encryption:
            self.toolbar.EnableTool(self.encrypt_records.GetId(), False)
            self.toolbar.EnableTool(self.add_record.GetId(), False)
            self.toolbar.EnableTool(self.import_records.GetId(), False)
            self.toolbar.EnableTool(self.export_records.GetId(), False)
        else:
            self.toolbar.EnableTool(self.decrypt_records.GetId(), False)
            self.toolbar.EnableTool(self.add_record.GetId(), True)
            self.toolbar.EnableTool(self.import_records.GetId(), True)
            self.toolbar.EnableTool(self.export_records.GetId(), True)
        self.toolbar.Realize()
        return hsizer

    def create_search(self):
        self.search = wx.SearchCtrl(
            self.panel, size=(300, 30), style=wx.TE_PROCESS_ENTER)
        self.search.ShowSearchButton(True)
        self.search.ShowCancelButton(True)
        self.panel.Bind(
            wx.EVT_TEXT_ENTER, self.event.bind_search_button, self.search)
        self.panel.Bind(
            wx.EVT_KEY_UP, self.event.bind_search_button, self.search)
        self.panel.Bind(
            wx.EVT_SEARCHCTRL_CANCEL_BTN, self.event.bind_clear_search_button,
            self.search)
        return self.search

    def get_sizer(self):
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.create_toolbar(), 1, wx.EXPAND)
        sizer.Add(self.create_search(), 0, wx.TOP, 5)
        return sizer
