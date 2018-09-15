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

from keepsake.unlocker import Unlocker


class Records(object):

    _unlocker = Unlocker
    _records = None
    _recents = None

    class Row(object):

        @classmethod
        def fields(cls):
            return {k:v for k, v in cls.__dict__.iteritems() if k[0] != "_"}

    def get_unlocker(self):
        return self._unlocker

    def flush(self):
        self._records = {}
        self._recents = []

    def has_record(self, record=None, name=None):
        if record is not None and issubclass(record, self.Row):
            return record.name in self._records
        elif name is not None:
            return name in self._records
        raise ValueError("Invalid arguments to lookup records")

    def add_record(self, record, name=None):
        if not issubclass(record, self.Row):
            raise TypeError("Cannot add a non-row record")
        if name is None:
            name = record.name
        if self.has_record(name=name):
            raise ValueError("Cannot add records with duplicated names")
        self._records.update({name: record})
        self._recents.append(name)

    def del_record(self, record=None, name=None):
        if record is not None and issubclass(record, self.Row):
            del self._records[record.name]
            self._recents.remove(record.name)
        elif name is not None:
            del self._records[name]
            self._recents.remove(name)
        else:
            raise ValueError("Invalid arguments to remove records")

    def get_record_by_name(self, name=None):
        if name is None:
            raise ValueError("Cannot get record for a null name")
        return self._records.get(name)

    def get_last_record(self):
        if len(self._recents) == 0:
            raise ValueError("Cannot get recent records")
        last_name = self._recents[-1]
        if not self.has_record(name=last_name):
            raise ValueError("Cannot get record with name %s" % last_name)
        return self.get_record_by_name(last_name)

    def get_records(self):
        return self._records

    def parse_line(self, line):
        records = {}
        total_cols = len(self._unlocker.COLS_FIELDS)
        i = 0
        for c in line.split(self._unlocker.COLS_SEPARATOR, total_cols):
            records.update({self._unlocker.COLS_FIELDS[i]: c.strip()})
            i += 1
        return records

    def refresh_records(self):
        rows = self._unlocker.list().split(self._unlocker.ROWS_SEPARATOR)
        for index, line in enumerate(rows[self._unlocker.ROWS_PADDING:]):
            if not line:
                continue  # skip empty lines if any
            row = type(self.Row.__name__, (self.Row,), self.parse_line(line))
            if self.has_record(name=row.name):  # skip if record exists
                continue
            self.add_record(row)

    def append_record(self, name, host, port, user, auth, scheme, jump=None):
        self._unlocker.append(name, host, port, user, auth, scheme, jump)
        return type(self.Row.__name__, (self.Row,), {
            "name": name,
            "host": host,
            "port": port,
            "user": user,
            "ipv4": "?",
            "scheme": scheme,
            "auth_signature": "?",
            "jump_signature": "Yes" if jump is not None else "No"
        })

    def remove_record(self, record):
        self._unlocker.remove(record.name)
        if self.has_record(name=record.name):
            self.del_record(name=record.name)

    def update_record(self, record, auth, jump=None):
        self._unlocker.update(record.name, auth, jump)

    def __repr__(self):
        return self.get_records()
