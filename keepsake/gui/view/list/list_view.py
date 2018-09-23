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
import wx.dataview as dv


class ListView(object):

    event = None

    list_headers = (
        ("#", 40),
        ("Hash", 80),
        ("Bounce", 65),
        ("Service", 65),
        ("Host", 180),
        ("Port", 65),
        ("User", 140),
        ("Name", 160),
    )

    @classmethod
    def register_event_broker(cls, broker):
        cls.event = broker

    def __init__(self, panel):
        self.panel = panel
        self.list_view = None
        self.list_data = {}
        self.index = 0
        self.prepare()
        self.refresh()

    def prepare(self):
        self.list_view = dv.DataViewListCtrl(self.panel)
        for idx, header in enumerate(self.list_headers):
            name, width = header
            self.list_view.AppendTextColumn(name, width=width)
        self.list_view.Bind(dv.EVT_DATAVIEW_SELECTION_CHANGED,
                            self.event.bind_item_selected)
        self.list_view.Bind(dv.EVT_DATAVIEW_ITEM_ACTIVATED,
                            self.event.bind_connect_button)
        self.list_view.Bind(dv.EVT_DATAVIEW_ITEM_CONTEXT_MENU,
                            self.event.bind_context_menu)

    def clear(self):
        data = self.list_data.copy()
        for each in data.iterkeys():
            self.list_view.DeleteItem(0)
        self.list_data = {}
        self.panel.parent.history("Records list is now empty")

    def refresh(self):
        self.panel.get_records().flush()
        self.panel.get_records().refresh_records()
        for record in self.panel.get_servers():
            self.add(record)
        self.panel.parent.history("Records list is now updated")

    def add(self, record):
        item = [str(self.index)]
        item.append(record.auth_signature)
        records = self.panel.get_records().get_unlocker()
        item.append(str(record.jump_signature != records.SELF_BOUNCE))
        item.append(record.scheme)
        item.append(record.host)
        item.append(record.port)
        item.append(record.user)
        item.append(record.name)
        self.list_view.AppendItem(item)
        message = "Added new %s server (%s) ..." % (record.scheme, record.host)
        self.panel.parent.history(message)
        self.add_data(record)
        self.index += 1

    def add_data(self, record):
        index = self.index  # copy for thread safety
        self.list_data.update({index: record})
        return index

    def remove_data(self, index):
        if index not in self.list_data:
            self.panel.display_message("Cannot find record on row %d" % index)
            return
        record = self.list_data[index]
        del self.list_data[index]
        return record

    def remove(self, index):
        self.list_view.DeleteItem(index)
        record = self.remove_data(index)
        message = "Removed %s server (%s) ..." % (record.scheme, record.host)
        self.panel.parent.history(message)
        self.index -= 1

    def remove_record(self, record):
        for index, each in self.list_data.iteritems():
            if each.name == record.name:
                return self.remove(index)
        name = record.name
        self.panel.display_message("Cannot find record %s to remove" % name)

    def get_sizer(self):
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.list_view, 1, wx.EXPAND)
        return sizer

    def match_record(self, index):
        if index in self.list_data:
            return self.list_data.get(index)
        self.panel.display_message("Cannot find record for index %d" % index)
