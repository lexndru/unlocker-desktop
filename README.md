# Keepsake
[![Build Status](https://travis-ci.org/lexndru/unlocker-desktop.svg?branch=master)](https://travis-ci.org/lexndru/unlocker-desktop)

Keepsake Desktop is a credentials manager with support for various protocols such as SSH, MySQL, Redis, Mongo, PostgreSQL. It's a GUI frontend for Unlocker, therefore it requires Unlocker to be installed and all helper scripts to be deployed on the current machine. Keepsake has implemented core functionalities of unlocker, such as passwordless connections, encryption, appending, updating, removing, listing and migrating secrets.

![Desktop](https://raw.githubusercontent.com/lexndru/unlocker-desktop/master/resources/screenshot.png)

## OS compatibility
This software is not fully compatible with all operating systems. Currently it offers support for Debian/Ubuntu and it may work on other Linux distros, although it has not been properly tested. Please feel free to contribute by submitting a pull request. Thank you!

## System requirements
- cPython >= 2.7.12
- pip >= 9.0.2
- unlocker >= 2.2.0
- wxPython >= 3.0.2

## Install and launch
```
$ make install
$ keepsake
```

## Install troubleshooting
During the software development process it was used an older version of wxPython, which by that time was not released to PyPI. If the application fails to proper install on your system, please try to install wxgtk3.0 dependency first.
```
$ apt-get install libgtk3.0-cil-dev python-wxgtk3.0
```

## About Unlocker
Unlocker is a keychain and a CLI credentials manager. Useful when you use a terminal often than GUI applications for remote connections (e.g. databases, SSH, rsync). It can store passwords and private keys. It comes with additional helper shells to encrypt your secrets and quick connect to servers passwordless.  https://github.com/lexndru/unlocker

## Features
- Passwordless connections for saved servers and supported protocols;
- Support plain passwords and private keys;
- Support connection bounces through SSH tunneling;
- Support custom naming for servers;
- List all known servers with detailed view (name, signature, bounce, port, protocol, hostname, IP address, username);
- Search through all known servers by name, signature, protocol, hostname, port and username;
- Add and remove credentials for various protocols (you can add any protocol, but not all protocols have support for passwordless connection);
- Update password or private key for a saved server;
- Update jump server (used to bounce) for a saved server;
- Validates user input on add/remove/edit;
- Copy to clipboard password or private key;
- Copy to clipboard entire or partial server properties;
- Export all or selected servers to \*.unl files;
- Import servers from \*.unl files;
- Encrypt and decrypt storage (requires GPG);
- Choose different terminals and shells from application preferences.

## Assets
The application uses icons under a GNU Lesser General Public License from http://www.iconarchive.com/artist/oxygen-icons.org.html

## Next steps
- [ ] Bind keys for application
- [ ] Port to wxPython 4.x
- [ ] Support MacOS

## License
Copyright 2018 Alexandru Catrina

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
