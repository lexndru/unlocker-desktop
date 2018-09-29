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

import time
import random

from unittest import TestCase
from threading import Thread
from xvfbwrapper import Xvfb

from keepsake.bootloader import Boot

from keepsake.gui.app import DesktopApp
from keepsake.gui.window import SingleMainWindow
from keepsake.gui.panel import CredentialsPanel


class DesktopThread(Thread):

    app = None

    def run(self):
        boot = Boot()
        boot.check_system()
        CredentialsPanel.register_boot(boot)
        print "around here"
        self.app = SingleMainWindow(CredentialsPanel)
        print "finally here %r" % self.app
        DesktopApp.run()


class TestGUIApp(TestCase):

    gui = None
    display = Xvfb()

    def setUp(self):
        print "Opening ..."
        self.display.start()
        self.gui = DesktopThread(name="keepsake test gui")
        self.gui.start()
        print "Running ..."

    def tearDown(self):
        print "Closing ..."
        self.assertIsNotNone(self.gui.app)
        self.gui.app.Close()
        self.display.stop()
        print "Closed"

    def test_gui_app(self):
        print "Waiting 5 seconds ..."
        time.sleep(5)  # wait a few seconds before closing
        print "Done waiting"
