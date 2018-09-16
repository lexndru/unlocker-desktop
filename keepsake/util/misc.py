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

from os import path, chmod
from os.path import expanduser
from uuid import uuid4


KEEPSAKE_SCRIPT = """#!/bin/bash

# connect to server
unlock $1 $2

# close window
read -p "(press enter to close this window)" _
"""


def deploy_helper_script(script_name="keepsake-unlock"):
    filepath = path.join(expanduser("~"), "bin", script_name)
    if path.exists(filepath):
        raise ValueError("Cannot continue: helper script is already deployed?")
    with open(filepath, "w") as fd:
        fd.write(KEEPSAKE_SCRIPT)
    chmod(filepath, 0500)
    return filepath


def generate_random_name(limit=16):
    name = str(uuid4().hex)
    return name[:limit]
