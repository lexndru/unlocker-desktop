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


class MainMenu(object):

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
        self.panel.menubar.Append(self.create_file_menu(), "&File")
        self.panel.menubar.Append(self.create_edit_menu(), "&Edit")
        self.panel.menubar.Append(self.create_tool_menu(), "&Tool")
        self.panel.menubar.Append(self.create_help_menu(), "&Help")
        self.panel.Refresh()

    def create_file_menu(self):
        file_menu = wx.Menu()

        # open server
        self.menu_open_server = file_menu.Append(
            wx.ID_ANY, "&Open connection\tCtrl-O")
        self.menu_open_server.Enable(False)
        self.panel.Bind(wx.EVT_MENU, self.event.bind_connect_button,
                         self.menu_open_server)

        # add server
        self.menu_new_server = file_menu.Append(
            wx.ID_ANY, "&New connection\tCtrl-N")
        if self.bootloader.secrets_encryption:
            self.menu_new_server.Enable(False)
        self.panel.Bind(
            wx.EVT_MENU, self.event.bind_add_button, self.menu_new_server)
        file_menu.AppendSeparator()

        # import servers
        self.menu_import_servers = file_menu.Append(wx.ID_ANY, "&Import ...")
        self.panel.Bind(wx.EVT_MENU, self.event.bind_import_button,
                        self.menu_import_servers)

        # export servers
        self.menu_export_any = file_menu.Append(wx.ID_ANY, "&Export ...")
        self.panel.Bind(wx.EVT_MENU, self.event.bind_export_any_button,
                        self.menu_export_any)
        self.menu_export_all = file_menu.Append(wx.ID_ANY, "E&xport all")
        self.panel.Bind(wx.EVT_MENU, self.event.bind_export_all_button,
                        self.menu_export_all)
        file_menu.AppendSeparator()

        # quit
        quit_app = file_menu.Append(wx.ID_ANY, "&Quit\tCtrl-Q")
        self.panel.Bind(wx.EVT_MENU, self.event.bind_quit, quit_app)

        return file_menu

    def create_edit_menu(self):
        edit_menu = wx.Menu()

        # cut selected
        self.menu_cut_selected = edit_menu.Append(wx.ID_ANY, "Cut\tCtrl-X")
        self.panel.Bind(
            wx.EVT_MENU, self.event.bind_cut_menu, self.menu_cut_selected)

        # copy selected
        self.menu_copy_selected = edit_menu.Append(wx.ID_ANY, "Copy\tCtrl-C")
        self.panel.Bind(
            wx.EVT_MENU, self.event.bind_copy_menu, self.menu_copy_selected)

        # paste selected
        self.menu_paste_selected = edit_menu.Append(wx.ID_ANY, "Paste\tCtrl-V")
        self.panel.Bind(
            wx.EVT_MENU, self.event.bind_paste_menu, self.menu_paste_selected)
        edit_menu.AppendSeparator()

        # copy fields
        self.menu_copy_server = edit_menu.Append(wx.ID_ANY, "Copy server")
        self.menu_copy_server.Enable(False)
        self.panel.Bind(wx.EVT_MENU, self.event.bind_copy_fields_menu,
                         self.menu_copy_server)

        # copy passkey
        self.menu_copy_passkey = edit_menu.Append(wx.ID_ANY, "Copy secret")
        self.menu_copy_passkey.Enable(False)
        self.panel.Bind(wx.EVT_MENU, self.event.bind_copy_passkey_menu,
                         self.menu_copy_passkey)
        edit_menu.AppendSeparator()

        # update selected
        self.menu_update_server = edit_menu.Append(wx.ID_ANY, "Update server")
        self.menu_update_server.Enable(False)
        self.panel.Bind(wx.EVT_MENU, self.event.bind_update_button,
                         self.menu_update_server)

        # remove selected
        self.menu_remove_server = edit_menu.Append(wx.ID_ANY, "Delete server")
        self.menu_remove_server.Enable(False)
        self.panel.Bind(wx.EVT_MENU, self.event.bind_remove_button,
                         self.menu_remove_server)
        edit_menu.AppendSeparator()

        # refresh
        refresh_list = edit_menu.Append(wx.ID_ANY, "Refresh ...\tCtrl-R")
        self.panel.Bind(wx.EVT_MENU, self.event.bind_refresh_button,
                         refresh_list)
        edit_menu.AppendSeparator()

        # preferences
        preferences = edit_menu.Append(wx.ID_ANY, "Preferences\tCtrl-P")
        self.panel.Bind(wx.EVT_MENU, self.event.bind_preferences_button,
                         preferences)

        return edit_menu

    def create_tool_menu(self):
        tool_menu = wx.Menu()

        # encrypt records
        self.menu_encrypt_records = tool_menu.Append(
            wx.ID_ANY, "Encrypt ...\tCtrl-L")
        if self.bootloader.secrets_encryption:
            self.menu_encrypt_records.Enable(False)
        self.panel.Bind(wx.EVT_MENU, self.event.bind_encrypt_button,
                         self.menu_encrypt_records)

        # decrypt records
        self.menu_decrypt_records = tool_menu.Append(
            wx.ID_ANY, "Decrypt ...\tCtrl-U")
        if not self.bootloader.secrets_encryption:
            self.menu_decrypt_records.Enable(False)
        self.panel.Bind(wx.EVT_MENU, self.event.bind_decrypt_button,
                         self.menu_decrypt_records)

        return tool_menu

    def create_help_menu(self):
        help_menu = wx.Menu()

        # about program
        about = help_menu.Append(wx.ID_ANY, "About")
        self.panel.Bind(wx.EVT_MENU, self.event.bind_about_menu, about)
        help_menu.AppendSeparator()

        # online documentation
        documentation = help_menu.Append(wx.ID_ANY, "Online documentation")
        self.panel.Bind(wx.EVT_MENU, self.event.bind_documentation_menu,
                         documentation)

        return help_menu
