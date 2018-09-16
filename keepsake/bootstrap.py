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

import sys

from keepsake.bootloader import Boot

from keepsake.gui.app import DesktopApp
from keepsake.gui.window import SingleMainWindow
from keepsake.gui.panel import CredentialsPanel

from keepsake.util.misc import deploy_helper_script


def main():

    # fix missing keepsake script
    if len(sys.argv) > 1 and sys.argv[1] == "fix":
        try:
            print "Script deployed:", deploy_helper_script()
        except Exception as e:
            print "Failed to deploy:", str(e)
        return  # force exit

    # scan current system
    boot = Boot()
    boot.check_system()

    # register boot scan results
    CredentialsPanel.register_boot(boot)

    # initialize window frame with panel to display
    SingleMainWindow(CredentialsPanel)

    # run application
    DesktopApp.run()
