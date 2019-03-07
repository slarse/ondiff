[![Build Status (Linux/macOS)](https://travis-ci.com/slarse/ondiff.svg)](https://travis-ci.com/slarse/ondiff)
[![Build Status (Windows)](https://ci.appveyor.com/api/projects/status/hqd6qunq62e5pw38/branch/master?svg=true)](https://ci.appveyor.com/project/slarse/ondiff/branch/master)
[![Code Coverage](https://codecov.io/gh/slarse/ondiff/branch/master/graph/badge.svg)](https://codecov.io/gh/slarse/ondiff)
![Supported Python Versions](https://img.shields.io/badge/python-3.6%2C%203.7-blue.svg)
![Supported Platforms](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows%2010-blue.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
# ondiff - Run commands automatically when files change ondiff is a simple
utility for running commands when files change (i.e. _on a diff_). Use cases
include watching a tex file for changes and running latex when it changes and
watching source code and running tests automatically. ondiff is currently in
early development and is not ready to be used yet. I am dogfooding the
application during development, which is why it is available on PyPi. **I
strongly urge against using ondiff at this time.** An alpha version should be
available within a week or so.

## Planned features
ondiff has a slew of features planned. Here are some of the most important
ones:

* Watch one or more files for diffs, and run arbitrary commands when a diff is
  detected.
* Recursive watching of directories.
* Simple string-formatting for commands that can make use of the name of the
  changed file.
* Cross-platform: Compatible with Linux-based operating systems, Windows 10 and
  macOS.
