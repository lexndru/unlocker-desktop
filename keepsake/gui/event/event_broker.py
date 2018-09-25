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
import webbrowser

from wx.lib.wordwrap import wordwrap

from keepsake import __homepage__, __version__, __license__

from keepsake.unlocker import Unlocker

from keepsake.util.settings import Settings

from keepsake.gui.misc.scripts import Scripts

from keepsake.gui.dialog.create_server import CreateServerDialog
from keepsake.gui.dialog.update_server import UpdateServerDialog
from keepsake.gui.dialog.preferences import PreferencesDialog


class EventBroker(object):

    FILES_EXT = (
        "Unlocker files (*.unl)|*.unl",
        "All files (*.*)|*.*"
    )

    def __init__(self, panel):
        self.panel = panel

    def refresh_callback(self, panel):
        panel.bootloader.check_system()
        mn = panel.get_menu()
        mn.menu_open_server.Enable(False)
        mn.menu_update_server.Enable(False)
        mn.menu_remove_server.Enable(False)
        mn.menu_copy_server.Enable(False)
        mn.menu_copy_passkey.Enable(False)
        tb = panel.get_toolbar()
        tb.toolbar.EnableTool(tb.connect_server.GetId(), False)
        tb.toolbar.EnableTool(tb.remove_record.GetId(), False)
        tb.toolbar.EnableTool(tb.update_record.GetId(), False)
        if panel.bootloader.secrets_encryption:
            tb.toolbar.EnableTool(tb.decrypt_records.GetId(), True)
            tb.toolbar.EnableTool(tb.encrypt_records.GetId(), False)
            tb.toolbar.EnableTool(tb.add_record.GetId(), False)
            tb.toolbar.EnableTool(tb.import_records.GetId(), False)
            tb.toolbar.EnableTool(tb.export_records.GetId(), False)
            mn.menu_new_server.Enable(False)
            mn.menu_encrypt_records.Enable(False)
            mn.menu_decrypt_records.Enable(True)
            mn.menu_import_servers.Enable(False)
            mn.menu_export_any.Enable(False)
            mn.menu_export_all.Enable(False)
        else:
            tb.toolbar.EnableTool(tb.decrypt_records.GetId(), False)
            tb.toolbar.EnableTool(tb.encrypt_records.GetId(), True)
            tb.toolbar.EnableTool(tb.add_record.GetId(), True)
            tb.toolbar.EnableTool(tb.import_records.GetId(), True)
            tb.toolbar.EnableTool(tb.export_records.GetId(), True)
            mn.menu_new_server.Enable(True)
            mn.menu_encrypt_records.Enable(True)
            mn.menu_decrypt_records.Enable(False)
            mn.menu_import_servers.Enable(True)
            mn.menu_export_any.Enable(True)
            mn.menu_export_all.Enable(True)
        panel.get_list_view().clear()
        panel.get_list_view().refresh()
        panel.get_toolbar().search.SetValue("")

    def bind_refresh_button(self, event):
        style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
        title = "Please wait"
        message = "Updating known servers..."
        dlg = wx.ProgressDialog(title, message, maximum=5,
                                parent=self.panel, style=style)
        self.refresh_callback(self.panel)
        count = 0
        while count < 5:
            count += 1
            wx.MilliSleep(250)
            wx.Yield()
            dlg.Update(count)
        dlg.Destroy()

    def bind_connect_button(self, event):
        record = self.panel.get_detail_view().get_record()
        title = "Please wait"
        message = "Connecting to %s server..." % record.scheme
        style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
        dlg = wx.ProgressDialog(title, message, maximum=5,
                                parent=self.panel, style=style)
        wx.MilliSleep(250)  # dummy
        wx.Yield()
        dlg.Destroy()
        unlocker = self.panel.get_records().get_unlocker()
        unlocker.connect(record.scheme, record.name)
        self.panel.history("Established connection to %s ..." % record.name)

    def bind_add_button(self, event):
        server_dlg = CreateServerDialog(self.panel)
        server_dlg.CenterOnScreen()
        dlg_btn_val = server_dlg.ShowModal()
        if dlg_btn_val == wx.ID_OK:
            new_server = server_dlg.get_results()
            if new_server.auth is None:
                new_server.auth = "password"
            data = new_server.as_dict()
            try:
                new_record = self.panel.get_records().append_record(**data)
                self.panel.get_list_view().add(new_record)
            except Exception as e:
                error = "Cannot continue due to an error: %s" % e
                self.panel.display_message(error)
        server_dlg.Destroy()

    def bind_remove_button(self, event):
        record = self.panel.get_detail_view().get_record()
        dialog = wx.MessageBox(
            "Are you sure you want to permanently " \
            "remove server %s?" % record.name,
            "Delete server", wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
        if dialog == wx.YES:
            self.panel.get_list_view().remove_record(record)
            self.panel.get_records().remove_record(record)

    def bind_update_button(self, event):
        record = self.panel.get_detail_view().get_record()
        update_dlg = UpdateServerDialog(self.panel, record.name)
        update_dlg.CenterOnScreen()
        dlg_btn_val = update_dlg.ShowModal()
        if dlg_btn_val == wx.ID_OK:
            new_server = update_dlg.get_results()
            if new_server.auth is None:
                new_server.auth = "password"
            auth = new_server.auth
            jump = update_dlg.get_jump_server()
            try:
                self.panel.get_records().update_record(record, auth, jump)
                self.panel.history("Record %s updated ..." % record.name)
            except Exception as e:
                error = "Cannot continue due to an error: %s" % e
                self.panel.display_message(error)
        update_dlg.Destroy()

    def bind_import_button(self, event):
        dlg = wx.FileDialog(
            self.panel, message="Choose a file", defaultDir=os.getcwd(),
            defaultFile="", wildcard="|".join(self.FILES_EXT),
            style=wx.OPEN | wx.CHANGE_DIR)
        message = ""
        if dlg.ShowModal() == wx.ID_OK:
            filepath = dlg.GetPath()
            try:
                unlocker = self.panel.get_records().get_unlocker()
                unlocker.migrate_import(filepath)
                message = "Successfully imported %s" % filepath
            except Exception as e:
                message = "Failed to import: %s" % str(e)
            self.panel.display_message(message)
        dlg.Destroy()
        if message:
            self.panel.history(message)

    def export_callback(self, export_servers):
        dialog = wx.MessageBox(
            "Preparing to export %d selected server(s).\nDo you " \
            "want to save the export to disk?" % len(export_servers),
            "Export servers", wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)
        if dialog != wx.YES or len(export_servers) == 0:
            return  # stop
        dlg = wx.FileDialog(
            self.panel, message="Save file as ...", defaultDir=os.getcwd(),
            defaultFile="", wildcard="|".join(self.FILES_EXT), style=wx.SAVE)
        dlg.SetFilterIndex(0)
        message = ""
        if dlg.ShowModal() == wx.ID_OK:
            filepath = dlg.GetPath()
            if not "." in filepath:
                filepath += ".unl"
            servers_names = [s.name for s in export_servers]
            try:
                unlocker = self.panel.get_records().get_unlocker()
                unlocker.migrate_export(filepath, servers_names)
                message = "Successfully exported %s" % filepath
            except Exception as e:
                message = "Failed to export: %s" % str(e)
            self.panel.display_message(message)
        dlg.Destroy()
        if message:
            self.panel.history(message)

    def bind_export_all_button(self, event):
        records_list = [r for r in self.panel.get_servers()]
        self.export_callback(records_list)

    def bind_export_any_button(self, event):
        records_list = [r for r in self.panel.get_servers()]
        servers = [s.name for s in records_list]
        dlg = wx.MultiChoiceDialog(
            self.panel, "Choose servers to export", "Export ...", servers)
        if dlg.ShowModal() != wx.ID_OK:
            return
        selections = dlg.GetSelections()
        dlg.Destroy()
        export_servers = [records_list[i] for i in selections]
        if len(export_servers) == 0:
            dialog = wx.MessageBox(
                "You haven't selected any servers to export.\nTry again.",
                "Export servers", wx.OK | wx.ICON_INFORMATION)
            return
        missing_jumps = []
        for each in export_servers:
            jump = each.jump_signature
            if jump == "~":
                continue
            if not any([s.auth_signature == jump for s in export_servers]):
                missing_jumps.append(each)
        if len(missing_jumps) > 0:
            dialog = wx.MessageBox(
                "You have selected servers that bounce from other " \
                "servers. Do you want to append jump servers as well " \
                "in the final export?",
                "Export servers", wx.YES_NO | wx.ICON_INFORMATION)
            if dialog == wx.YES:
                found_jumps = []
                for each in missing_jumps:
                    for server in records_list:
                        if each.jump_signature == server.auth_signature:
                            export_servers.append(server)
                            found_jumps.append(each)
                for each in found_jumps:
                    missing_jumps.remove(each)
                if len(missing_jumps) != 0:
                    dialog = wx.MessageBox(
                        "Unable to find jump servers. " \
                        "Export might be corrupted.",
                        "Export fix failed", wx.OK | wx.ICON_INFORMATION)
        self.export_callback(export_servers)

    def copy_callback(self, data):
        text_data = wx.TextDataObject()
        text_data.SetText(data)
        if wx.TheClipboard.Open():
            wx.TheClipboard.SetData(text_data)
            wx.TheClipboard.Close()
            return True
        return False

    def copy_to_clipboard(self, field):
        record = self.panel.get_detail_view().get_record()
        if hasattr(record, field):
            data = getattr(record, field)
            if self.copy_callback(data):
                return self.panel.history("Copied %s to clipboard" % field)
        self.panel.display_message("Cannot copy %s to clipboard" % field)

    def bind_copy_fields_menu(self, event):
        record = self.panel.get_detail_view().get_record()
        data = ""
        data += "Name: %s\n" % record.name
        data += "Host: %s\n" % record.host
        data += "IPv4: %s\n" % record.ipv4
        data += "Port: %s\n" % record.port
        data += "User: %s\n" % record.user
        data += "Protocol: %s" % record.scheme
        self.copy_callback(data)

    def bind_copy_passkey_menu(self, event):
        self.on_context_copy_passkey(event)

    def bind_cut_menu(self, event):
        element = self.panel.FindFocus()
        if hasattr(element, "GetStringSelection"):
            self.copy_callback(element.GetStringSelection())
        if hasattr(element, "SetValue"):
            element.SetValue("")

    def bind_copy_menu(self, event):
        element = self.panel.FindFocus()
        if hasattr(element, "GetStringSelection"):
            self.copy_callback(element.GetStringSelection())

    def bind_paste_menu(self, event):
        element = self.panel.FindFocus()
        if not wx.TheClipboard.Open():
            return self.panel.display_message("Can't access clipboard")
        clipboard = wx.TextDataObject()
        wx.TheClipboard.GetData(clipboard)
        wx.TheClipboard.Close()
        if hasattr(element, "SetValue"):
            element.SetValue(clipboard.GetText())

    def bind_context_menu(self, event):
        menu = wx.Menu()
        connect_server = menu.Append(wx.ID_ANY, "Connect ...")
        menu.AppendSeparator()
        copy_name = menu.Append(wx.ID_ANY, "Copy name")
        copy_host = menu.Append(wx.ID_ANY, "Copy host")
        copy_user = menu.Append(wx.ID_ANY, "Copy user")
        copy_passkey = menu.Append(wx.ID_ANY, "Copy passkey")
        self.panel.Bind(wx.EVT_MENU, self.bind_connect_button, connect_server)
        self.panel.Bind(wx.EVT_MENU, self.on_context_copy_name, copy_name)
        self.panel.Bind(wx.EVT_MENU, self.on_context_copy_host, copy_host)
        self.panel.Bind(wx.EVT_MENU, self.on_context_copy_user, copy_user)
        self.panel.Bind(wx.EVT_MENU, self.on_context_copy_passkey, copy_passkey)
        self.panel.PopupMenu(menu)

    def on_context_copy_name(self, event):
        self.copy_to_clipboard("name")

    def on_context_copy_host(self, event):
        self.copy_to_clipboard("host")

    def on_context_copy_user(self, event):
        self.copy_to_clipboard("user")

    def on_context_copy_passkey(self, event):
        record = self.panel.get_detail_view().get_record()
        passkey = self.panel.get_records().decode_passkey(record.name)
        if self.copy_callback(passkey):
            return self.panel.history("Copied passkey to clipboard")
        self.panel.display_message("Cannot copy passkey to clipboard")

    def bind_preferences_button(self, event):
        pref = PreferencesDialog(self.panel)
        pref.CenterOnScreen()
        val = pref.ShowModal()
        if val == wx.ID_OK:
            sett = Settings()
            sett.update(pref.get_shell(), pref.get_terminal())
            Unlocker.SHELL = pref.get_shell()
            Unlocker.TERMINAL = pref.get_terminal()
            style = wx.PD_APP_MODAL | wx.PD_AUTO_HIDE
            title = "Please wait"
            message = "Saving preferences..."
            dlg = wx.ProgressDialog(
                title, message, maximum=5, parent=pref, style=style)
            wx.MilliSleep(250)  # dummy
            wx.Yield()
            dlg.Destroy()
        pref.Destroy()

    def bind_item_selected(self, event):
        item_id = self.panel.get_list_view().get_current_row()
        if not item_id >= 0:
            return

        record = self.panel.get_list_view().match_record(item_id)
        self.panel.get_detail_view().update(record)

        # enable toolbar
        tb = self.panel.get_toolbar()
        tb.toolbar.EnableTool(tb.connect_server.GetId(), True)
        tb.toolbar.EnableTool(tb.remove_record.GetId(), True)
        tb.toolbar.EnableTool(tb.update_record.GetId(), True)

        # enable menu options
        mn = self.panel.get_menu()
        mn.menu_open_server.Enable(True)
        mn.menu_update_server.Enable(True)
        mn.menu_remove_server.Enable(True)
        mn.menu_copy_server.Enable(True)
        mn.menu_copy_passkey.Enable(True)

    def bind_clear_search_button(self, event):
        list_view = self.panel.get_list_view()
        list_view.clear()
        list_view.refresh()

    def bind_search_button(self, event):
        toolbar = self.panel.get_toolbar()
        search = toolbar.search.GetValue().strip()
        if not search:
            return self.bind_clear_search_button(event)
        self.panel.get_list_view().clear()
        for server in self.panel.get_servers():
            if self.panel.get_records().compare_record(search, server):
                self.panel.get_list_view().add(server)

    def bind_encrypt_button(self, event):
        self.panel.get_list_view().clear()
        self.panel.get_scripts().encrypt()
        self.panel.history("Please refresh list ...")

        # disable toolbar buttons
        tb = self.panel.get_toolbar()
        tb.toolbar.EnableTool(tb.connect_server.GetId(), False)
        tb.toolbar.EnableTool(tb.add_record.GetId(), False)
        tb.toolbar.EnableTool(tb.remove_record.GetId(), False)
        tb.toolbar.EnableTool(tb.update_record.GetId(), False)
        tb.toolbar.EnableTool(tb.import_records.GetId(), False)
        tb.toolbar.EnableTool(tb.export_records.GetId(), False)
        tb.toolbar.EnableTool(tb.encrypt_records.GetId(), False)
        tb.toolbar.EnableTool(tb.decrypt_records.GetId(), True)

        # disable menu options
        mn = self.panel.get_menu()
        mn.menu_open_server.Enable(False)
        mn.menu_new_server.Enable(False)
        mn.menu_update_server.Enable(False)
        mn.menu_remove_server.Enable(False)
        mn.menu_copy_server.Enable(False)
        mn.menu_copy_passkey.Enable(False)
        mn.menu_import_servers.Enable(False)
        mn.menu_export_any.Enable(False)
        mn.menu_export_all.Enable(False)
        mn.menu_encrypt_records.Enable(False)
        mn.menu_decrypt_records.Enable(True)

    def bind_decrypt_button(self, event):
        self.panel.get_list_view().clear()
        self.panel.get_scripts().decrypt()
        self.panel.history("Please refresh list ...")

        # disable toolbar buttons
        tb = self.panel.get_toolbar()
        tb.toolbar.EnableTool(tb.connect_server.GetId(), False)
        tb.toolbar.EnableTool(tb.add_record.GetId(), True)
        tb.toolbar.EnableTool(tb.remove_record.GetId(), False)
        tb.toolbar.EnableTool(tb.update_record.GetId(), False)
        tb.toolbar.EnableTool(tb.import_records.GetId(), True)
        tb.toolbar.EnableTool(tb.export_records.GetId(), True)
        tb.toolbar.EnableTool(tb.encrypt_records.GetId(), True)
        tb.toolbar.EnableTool(tb.decrypt_records.GetId(), False)

        # disable menu options
        mn = self.panel.get_menu()
        mn.menu_open_server.Enable(False)
        mn.menu_new_server.Enable(True)
        mn.menu_update_server.Enable(False)
        mn.menu_remove_server.Enable(False)
        mn.menu_copy_server.Enable(False)
        mn.menu_copy_passkey.Enable(False)
        mn.menu_import_servers.Enable(True)
        mn.menu_export_any.Enable(True)
        mn.menu_export_all.Enable(True)
        mn.menu_encrypt_records.Enable(True)
        mn.menu_decrypt_records.Enable(False)

    def bind_quit(self, event):
        self.panel.parent.Close()

    def bind_documentation_menu(self, event):
        webbrowser.open(__homepage__, new=2)

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
            350, wx.ClientDC(self.panel))
        about.WebSite = (__homepage__, "Keepsake GitHub")
        about.Developers = ["Alexandru Catrina <alex@codeissues.net>"]
        license = []
        sections = __license__.split("\n\n")
        for each in sections:
            license.append(" ".join(each.split("\n")))
        about.License = wordwrap("\n\n".join(license), 500,
                                 wx.ClientDC(self.panel))
        wx.AboutBox(about)
