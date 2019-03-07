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
