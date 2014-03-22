iterm-exec is a python script that creates an applescript that will execute a
given command on multiple different servers in different splits.  You can
control how many rows of splits it makes.  After the temporary applescript is
ran it will be deleted.

Usage
=====

::

    iterm_exec.py [-r rows] <host> [...] <command>

This will run whoami on server1 and server2::

    iterm_exec.py server1 server2 whoami

If your command has spaces in it you will need to quote it::

    iterm_exec.py server1 server2 'hostname -f'

If you want a different amount of rows (defaults to two) then do this::

    iterm_exec.py -r 3 server1 server2 server3 server4 whoami

Installation
============

Copy the iterm_exec.py script somewhere into your PATH::

    # download the script
    curl https://raw.github.com/jasonkeene/iterm-exec/master/iterm_exec.py > iterm_exec.py

    # make sure the script is executable
    chmod +x iterm_exec.py
    
    # move the script into your PATH, for instance my local path is ~/.local/bin/
    mv iterm_exec.py ~/.local/bin/

Defining SSH Hosts
==================

You can use the format user@hostname to specifiy a user for the server but
this format does not allow you to specify a port number or identfile.  To do
this you must add a Host entry to your SSH conf.

#. Edit ``~/.ssh/config``
#. Add a Host section like this::

    Host server1
        User user1
        IdentityFile ~/.ssh/server1_id_rsa
        HostName server1.someotherhostname.com
        Port 9999

Now you can type ``iterm_exec.py server1 whoami`` and it will connect to server
one with the given user/port/identfile/etc.

If you wish to enable tab completion in bash for your ssh conf hosts check out
this: https://github.com/jasonkeene/dotfiles/blob/master/.bash_darwin#L37
