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
import webbrowser

from wx.lib.wordwrap import wordwrap

from keepsake import __project__, __homepage__, __version__, __license__

from keepsake.gui.dialog.create_server import CreateServerDialog
from keepsake.gui.dialog.update_server import UpdateServerDialog

from keepsake.gui.misc.records import Records
from keepsake.gui.misc.scripts import Scripts


class CredentialsPanel(wx.Panel):

    bootloader = None

    notice_messages = []

    unlocker_files = (
        "Unlocker files (*.unl)|*.unl",
        "All files (*.*)|*.*"
    )

    headers = (
        ("Hash", 80),
        ("Bounce", 80),
        ("Service", 160),
        ("Host", 180),
        ("User", 140),
        ("Name", 160),
    )

    lookup_fields = ("name", "host", "user", "scheme")

    search = None
    toolbar = None
    list_view = None

    records = None
    records_list = []

    encrypted = False

    def __init__(self, parent):
        super(self.__class__, self).__init__(parent=parent)
        self.parent = parent
        self.create_main_menu()
        self.scripts = Scripts()
        self.records = Records()
        self.records.flush()  # reset Records memory
        self.reinitialize()
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        top_sizer.Add(self.create_toolbar(), 1, wx.EXPAND)
        top_sizer.Add(self.create_search(), 0, wx.TOP, 5)
        self.main_sizer.Add(top_sizer, 0, wx.EXPAND | wx.ALL, 1)
        self.main_sizer.Add(self.create_listview(), 1, wx.EXPAND | wx.ALL, 1)
        self.SetSizerAndFit(self.main_sizer)
        self.Show(True)

    def get_icon(self, name):
        return os.path.join(__project__, "icons/{}.png".format(name))

    def set_boottime_alerts(self):
        problems = len(self.notice_messages)
        notice = "Found %d problem(s) during bootload:" % problems
        for msg in self.notice_messages:
            notice += "\n- %s" % msg
        self.display_message(notice)
        self.parent.history(notice[:-1] + "...")

    def reinitialize(self):
        if self.bootloader is not None:
            self.read_notice_messages() and self.set_boottime_alerts()
            self.notice_messages = []  # flush messages
        self.records.refresh_records()
        for name, server in self.records.get_records().iteritems():
            self.records_list.append(server)

    def create_file_menu(self):
        file_menu = wx.Menu()

        # open server
        self.menu_open_server = file_menu.Append(
            wx.ID_ANY, "&Open connection\tCtrl-O")
        self.menu_open_server.Enable(False)
        self.parent.Bind(
            wx.EVT_MENU, self.bind_connect_button, self.menu_open_server)

        # add server
        self.menu_new_server = file_menu.Append(
            wx.ID_ANY, "&New connection\tCtrl-N")
        if self.bootloader.secrets_encryption:
            self.menu_new_server.Enable(False)
        self.parent.Bind(
            wx.EVT_MENU, self.bind_add_button, self.menu_new_server)
        file_menu.AppendSeparator()

        # import servers
        import_servers = file_menu.Append(wx.ID_ANY, "&Import ...")
        self.parent.Bind(wx.EVT_MENU, self.bind_import_button, import_servers)

        # export servers
        export_servers = file_menu.Append(wx.ID_ANY, "&Export ...")
        self.parent.Bind(wx.EVT_MENU, self.bind_export_button, export_servers)
        file_menu.AppendSeparator()

        # quit
        quit_app = file_menu.Append(wx.ID_ANY, "&Quit\tCtrl-Q")
        self.parent.Bind(wx.EVT_MENU, self.bind_quit, quit_app)

        return file_menu

    def create_edit_menu(self):
        edit_menu = wx.Menu()

        # cut selected
        self.menu_cut_selected = edit_menu.Append(wx.ID_ANY, "Cut\tCtrl-X")
        self.parent.Bind(
            wx.EVT_MENU, self.bind_cut_menu, self.menu_cut_selected)

        # copy selected
        self.menu_copy_selected = edit_menu.Append(wx.ID_ANY, "Copy\tCtrl-C")
        self.parent.Bind(
            wx.EVT_MENU, self.bind_copy_menu, self.menu_copy_selected)

        # paste selected
        self.menu_paste_selected = edit_menu.Append(wx.ID_ANY, "Paste\tCtrl-V")
        self.parent.Bind(
            wx.EVT_MENU, self.bind_paste_menu, self.menu_paste_selected)
        edit_menu.AppendSeparator()

        # copy fields
        self.menu_copy_server = edit_menu.Append(wx.ID_ANY, "Copy server")
        self.menu_copy_server.Enable(False)
        self.parent.Bind(
            wx.EVT_MENU, self.bind_copy_fields_menu, self.menu_copy_server)

        # copy passkey
        self.menu_copy_passkey = edit_menu.Append(wx.ID_ANY, "Copy secret")
        self.menu_copy_passkey.Enable(False)
        self.parent.Bind(
            wx.EVT_MENU, self.bind_copy_passkey_menu, self.menu_copy_passkey)
        edit_menu.AppendSeparator()

        # update selected
        self.menu_update_server = edit_menu.Append(wx.ID_ANY, "Update server")
        self.menu_update_server.Enable(False)
        self.parent.Bind(
            wx.EVT_MENU, self.bind_update_button, self.menu_update_server)

        # remove selected
        self.menu_remove_server = edit_menu.Append(wx.ID_ANY, "Delete server")
        self.menu_remove_server.Enable(False)
        self.parent.Bind(
            wx.EVT_MENU, self.bind_remove_button, self.menu_remove_server)
        edit_menu.AppendSeparator()

        # refresh
        refresh_list = edit_menu.Append(wx.ID_ANY, "Refresh ...\tCtrl-R")
        self.parent.Bind(wx.EVT_MENU, self.bind_refresh_button, refresh_list)

        return edit_menu

    def create_tool_menu(self):
        tool_menu = wx.Menu()

        # encrypt records
        self.menu_encrypt_records = tool_menu.Append(
            wx.ID_ANY, "Encrypt ...\tCtrl-L")
        if self.bootloader.secrets_encryption:
            self.menu_encrypt_records.Enable(False)
        self.parent.Bind(
            wx.EVT_MENU, self.bind_encrypt_button, self.menu_encrypt_records)

        # decrypt records
        self.menu_decrypt_records = tool_menu.Append(
            wx.ID_ANY, "Decrypt ...\tCtrl-U")
        if not self.bootloader.secrets_encryption:
            self.menu_decrypt_records.Enable(False)
        self.parent.Bind(
            wx.EVT_MENU, self.bind_decrypt_button, self.menu_decrypt_records)

        return tool_menu

    def create_help_menu(self):
        help_menu = wx.Menu()

        # about program
        about = help_menu.Append(wx.ID_ANY, "About")
        self.parent.Bind(wx.EVT_MENU, self.bind_about_menu, about)
        help_menu.AppendSeparator()

        # online documentation
        documentation = help_menu.Append(wx.ID_ANY, "Online documentation")
        self.parent.Bind(
            wx.EVT_MENU, self.bind_documentation_menu, documentation)

        return help_menu

    def create_main_menu(self):
        self.parent.menubar.Append(self.create_file_menu(), "&File")
        self.parent.menubar.Append(self.create_edit_menu(), "&Edit")
        self.parent.menubar.Append(self.create_tool_menu(), "&Tool")
        self.parent.menubar.Append(self.create_help_menu(), "&Help")
        self.parent.Refresh()
        self.Refresh()

    def create_search(self):
        self.search = wx.SearchCtrl(
            self, size=(300, 30), style=wx.TE_PROCESS_ENTER)
        self.search.ShowSearchButton(True)
        self.search.ShowCancelButton(True)
        self.Bind(wx.EVT_TEXT_ENTER, self.bind_search_button, self.search)
        self.Bind(wx.EVT_KEY_UP, self.bind_search_button, self.search)
        self.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN,
                  self.bind_clear_search_button, self.search)
        return self.search

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
        self.list_view.Bind(
            wx.EVT_LIST_ITEM_ACTIVATED, self.bind_connect_button)
        self.list_view.Bind(wx.EVT_CONTEXT_MENU, self.bind_context_menu)
        self.populate_listview()
        return vsizer

    def clear_listview(self):
        while len(self.records_list) > 0:
            idx = len(self.records_list) - 1
            self.list_view.DeleteItem(idx)
            self.records_list.pop(idx)
        self.parent.history("Records list is now empty")

    def populate_listview(self):
        for index, record in enumerate(self.records_list):
            self.add_listview_item(index, record)
        self.parent.history("Records list is now updated")

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
        message = "Added new %s server (%s) ..." % (record.scheme, record.host)
        self.parent.history(message)

    def del_listview_item(self, index):
        self.list_view.DeleteItem(index)
        record = self.current_record
        message = "Removed %s server (%s) ..." % (record.scheme, record.host)
        self.parent.history(message)

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
        self.Bind(wx.EVT_TOOL, self.bind_connect_button, self.connect_server)
        self.Bind(wx.EVT_TOOL, self.bind_add_button, self.add_record)
        self.Bind(wx.EVT_TOOL, self.bind_remove_button, self.remove_record)
        self.Bind(wx.EVT_TOOL, self.bind_update_button, self.update_record)
        self.Bind(wx.EVT_TOOL, self.bind_refresh_button, self.refresh_view)
        self.Bind(wx.EVT_TOOL, self.bind_import_button, self.import_records)
        self.Bind(wx.EVT_TOOL, self.bind_export_button, self.export_records)
        self.Bind(wx.EVT_TOOL, self.bind_encrypt_button, self.encrypt_records)
        self.Bind(wx.EVT_TOOL, self.bind_decrypt_button, self.decrypt_records)
        self.toolbar.EnableTool(self.connect_server.GetId(), False)
        self.toolbar.EnableTool(self.remove_record.GetId(), False)
        self.toolbar.EnableTool(self.update_record.GetId(), False)
        if self.encrypted:
            self.toolbar.EnableTool(self.encrypt_records.GetId(), False)
            self.toolbar.EnableTool(self.add_record.GetId(), False)
        else:
            self.toolbar.EnableTool(self.decrypt_records.GetId(), False)
        self.toolbar.Realize()
        return hsizer

    def display_message(self, message=None, title="Notice"):
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
        self.menu_open_server.Enable(True)
        self.menu_update_server.Enable(True)
        self.menu_remove_server.Enable(True)
        self.menu_copy_server.Enable(True)
        self.menu_copy_passkey.Enable(True)

    def copy_data(self, data):
        text_data = wx.TextDataObject()
        text_data.SetText(data)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(text_data)
            wx.TheClipboard.Close()
            return True
        return False

    def copy_to_clipboard(self, field):
        if hasattr(self.current_record, field):
            data = getattr(self.current_record, field)
            if self.copy_data(data):
                return self.parent.history("Copied %s to clipboard" % field)
        self.display_message("Cannot copy %s to clipboard" % field)

    def on_context_copy_name(self, event):
        self.copy_to_clipboard("name")

    def on_context_copy_host(self, event):
        self.copy_to_clipboard("host")

    def on_context_copy_user(self, event):
        self.copy_to_clipboard("user")

    def on_context_copy_passkey(self, event):
        passkey = self.records.decode_passkey(self.current_record.name)
        if self.copy_data(passkey):
            return self.parent.history("Copied passkey to clipboard")
        self.display_message("Cannot copy passkey to clipboard")

    def bind_context_menu(self, event):
        copy_name = wx.NewId()
        copy_host = wx.NewId()
        copy_user = wx.NewId()
        copy_passkey = wx.NewId()
        self.Bind(wx.EVT_MENU, self.on_context_copy_name, id=copy_name)
        self.Bind(wx.EVT_MENU, self.on_context_copy_host, id=copy_host)
        self.Bind(wx.EVT_MENU, self.on_context_copy_user, id=copy_user)
        self.Bind(wx.EVT_MENU, self.on_context_copy_passkey, id=copy_passkey)
        menu = wx.Menu()
        menu.Append(copy_name, "Copy name")
        menu.Append(copy_host, "Copy host")
        menu.Append(copy_user, "Copy user")
        menu.Append(copy_passkey, "Copy passkey")
        self.PopupMenu(menu)

    def bind_clear_search_button(self, event):
        self.clear_listview()
        self.reinitialize()
        self.populate_listview()

    def bind_search_button(self, event):
        search = self.search.GetValue().strip()
        if not search:
            return self.bind_clear_search_button(event)
        records_list = self.records_list[:]
        self.clear_listview()
        index = 0
        for record in records_list:
            if self.found_record(search, record):
                self.add_listview_item(index, record)
                self.records_list.append(record)
                index += 1

    def found_record(self, search, record):
        for field in self.lookup_fields:
            value = getattr(record, field)
            if isinstance(value, str):
                value = value.decode("utf-8")
            if search in value:
                return True
        return False

    def bind_refresh_button(self, event):
        self.bootloader.check_system()
        dlg = wx.ProgressDialog(
            "Please wait", "Updating known servers...",
            maximum=5, parent=self, style=wx.PD_APP_MODAL | wx.PD_AUTO_HIDE)
        count = 0
        self.menu_open_server.Enable(False)
        self.menu_update_server.Enable(False)
        self.menu_remove_server.Enable(False)
        self.menu_copy_server.Enable(False)
        self.menu_copy_passkey.Enable(False)
        self.toolbar.EnableTool(self.connect_server.GetId(), False)
        self.toolbar.EnableTool(self.remove_record.GetId(), False)
        self.toolbar.EnableTool(self.update_record.GetId(), False)
        if self.bootloader.secrets_encryption:
            self.toolbar.EnableTool(self.decrypt_records.GetId(), True)
            self.toolbar.EnableTool(self.encrypt_records.GetId(), False)
            self.toolbar.EnableTool(self.add_record.GetId(), False)
            self.menu_new_server.Enable(False)
            self.menu_encrypt_records.Enable(False)
            self.menu_decrypt_records.Enable(True)
        else:
            self.toolbar.EnableTool(self.decrypt_records.GetId(), False)
            self.toolbar.EnableTool(self.encrypt_records.GetId(), True)
            self.toolbar.EnableTool(self.add_record.GetId(), True)
            self.menu_new_server.Enable(True)
            self.menu_encrypt_records.Enable(True)
            self.menu_decrypt_records.Enable(False)
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
        self.search.SetValue("")

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
        record = self.current_record
        dlg = UpdateServerDialog(self, record)
        dlg.CenterOnScreen()
        val = dlg.ShowModal()
        if val == wx.ID_OK:
            if dlg.last_server.auth is None:
                dlg.last_server.auth = "password"
            try:
                self.records.update_record(record, dlg.last_server.auth)
                self.parent.history("Record %s updated ..." % record.name)
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
        wx.MilliSleep(250)
        wx.Yield()
        self.records.get_unlocker().connect(service, name)
        self.parent.history("Established connection to %s ..." % name)
        dlg.Destroy()

    def bind_import_button(self, event):
        dlg = wx.FileDialog(
            self, message="Choose a file", defaultDir=os.getcwd(),
            defaultFile="", wildcard="|".join(self.unlocker_files),
            style=wx.OPEN | wx.CHANGE_DIR)
        message = ""
        if dlg.ShowModal() == wx.ID_OK:
            filepath = dlg.GetPath()
            try:
                self.records.get_unlocker().migrate_import(filepath)
                message = "Successfully imported %s" % filepath
            except Exception as e:
                message = "Failed to import: %s" % str(e)
            self.display_message(message)
        dlg.Destroy()
        if message:
            self.parent.history(message)

    def bind_export_button(self, event):
        files = "|".join(self.unlocker_files)
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile="", wildcard=files, style=wx.SAVE)
        dlg.SetFilterIndex(0)
        message = ""
        if dlg.ShowModal() == wx.ID_OK:
            filepath = dlg.GetPath()
            try:
                self.records.get_unlocker().migrate_export(filepath)
                message = "Successfully exported %s" % filepath
            except Exception as e:
                message = "Failed to export: %s" % str(e)
            self.display_message(message)
        dlg.Destroy()
        if message:
            self.parent.history(message)

    def bind_encrypt_button(self, event):
        self.scripts.encrypt()
        self.clear_listview()
        self.parent.history("Please refresh list ...")

    def bind_decrypt_button(self, event):
        self.scripts.decrypt()
        self.clear_listview()
        self.parent.history("Please refresh list ...")

    def read_notice_messages(self):
        if self.bootloader.secrets_encryption:
            self.encrypted = True
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

    def bind_quit(self, event):
        self.parent.Close()

    def bind_copy_fields_menu(self, event):
        data = ""
        data += "Name: %s\n" % self.current_record.name
        data += "Host: %s\n" % self.current_record.host
        data += "IPv4: %s\n" % self.current_record.ipv4
        data += "Port: %s\n" % self.current_record.port
        data += "User: %s\n" % self.current_record.user
        data += "Protocol: %s" % self.current_record.scheme
        self.copy_data(data)

    def bind_copy_passkey_menu(self, event):
        self.on_context_copy_passkey(event)

    def bind_cut_menu(self, event):
        element = self.FindFocus()
        if hasattr(element, "GetStringSelection"):
            self.copy_data(element.GetStringSelection())
        if hasattr(element, "SetValue"):
            element.SetValue("")

    def bind_copy_menu(self, event):
        element = self.FindFocus()
        if hasattr(element, "GetStringSelection"):
            self.copy_data(element.GetStringSelection())

    def bind_paste_menu(self, event):
        element = self.FindFocus()
        if not wx.TheClipboard.Open():
            return self.display_message("Can't access clipboard")
        clipboard = wx.TextDataObject()
        wx.TheClipboard.GetData(clipboard)
        wx.TheClipboard.Close()
        if hasattr(element, "SetValue"):
            element.SetValue(clipboard.GetText())

    def bind_about_menu(self, event):
        about = wx.AboutDialogInfo()
        about.Name = "Keepsake Desktop"
        about.Version = __version__
        about.Copyright = "(c) 2018 Alexandru Catrina"
        about.Description = wordwrap(
            "Keepsake Desktop is a credentials manager with support for "
            "various protocols such as SSH, MySQL, Redis, Mongo, PostgreSQL"
            "\n\nIt's a GUI frontend for Unlocker, therefore it requires "
            "Unlocker to be installed and all helper scripts to be "
            "deployed on the current machine. Keepsake has implemented "
            "core functionalities of unlocker, such as passwordless "
            "connections, encryption, appending, updating, removing, "
            "listing and migrating secrets.",
            350, wx.ClientDC(self))
        about.WebSite = (__homepage__, "Keepsake GitHub")
        about.Developers = ["Alexandru Catrina <alex@codeissues.net>"]
        license = []
        sections = __license__.split("\n\n")
        for each in sections:
            license.append(" ".join(each.split("\n")))
        about.License = wordwrap("\n\n".join(license), 500, wx.ClientDC(self))
        wx.AboutBox(about)

    def bind_documentation_menu(self, event):
        webbrowser.open(__homepage__, new=2)

    @classmethod
    def register_boot(cls, boot):
        cls.bootloader = boot
