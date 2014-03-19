#!/usr/bin/env python

import contextlib
import os
import subprocess
import sys
import tempfile

DEFAULT_ROWS = 2
USAGE = "usage: iterm_exec.py [-r rows] <host> [...] <command>"
APPLE_SCRIPT = r"""
launch "iTerm"

tell application "iTerm"
    activate

    -- figure out the current terminal
    if current terminal exists then
        set current_term to (current terminal)
    else
        set current_term to (make new terminal)
    end if

    tell current_term
        -- create new tab
        launch session ""

        -- create all the sessions


{}


    end tell
end tell
"""
KEYSTROKE = r"""tell i term application "System Events" to keystroke "{}" {}"""
SSH_COMMAND = r"""ssh -t {} '{}' '; exec /bin/bash -i'\n"""


def keystroke(keys, command=False):
    return KEYSTROKE.format(keys, "using command down" if command else "")


def ssh_command(host, command):
    return keystroke(SSH_COMMAND.format(host, command.replace(r'"', r'\"')))


@contextlib.contextmanager
def make_temp_file(mode='w'):
    fd, path = tempfile.mkstemp()
    with open(path, mode) as temp_file:
        yield temp_file
    os.remove(path)


def parse_argv(argv):
    rows = DEFAULT_ROWS
    if len(argv) < 3:
        sys.stderr.write(USAGE + "\n")
        sys.exit(1)
    if argv[1] == '-r':
        argv.pop(1)
        try:
            rows = int(argv.pop(1))
            if rows < 1:
                raise ValueError
        except ValueError:
            sys.stderr.write(USAGE + "\n")
            sys.exit(1)
    if len(argv) < 3:
        sys.stderr.write(USAGE + "\n")
        sys.exit(1)

    return rows, argv[1:-1], argv[-1]


def main(rows, hosts, command):
    sessions = []
    column_hosts = [host for i, host in enumerate(hosts) if not i % rows]

    # spawn the columns
    for i, host in enumerate(column_hosts):
        if i != 0:
            sessions.append(keystroke('d', True))
        sessions.append(ssh_command(host, command))

    # backup to first column
    sessions.append(keystroke('[' * (len(column_hosts) - 1), True))

    # launch remaining hosts
    for i, host in enumerate(hosts):
        if i % rows:
            sessions.append(keystroke('D', True))
            sessions.append(ssh_command(host, command))

            # skip to the next column
            if i % rows == rows - 1:
                sessions.append(keystroke(']', True))

    with make_temp_file() as f:
        f.write(APPLE_SCRIPT.format("\n\n".join(sessions)))
        f.close()
        subprocess.call(["osascript", f.name])


if __name__ == '__main__':
    main(*parse_argv(sys.argv))
