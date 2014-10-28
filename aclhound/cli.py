#!/usr/bin/env python2.7
# Copyright (C) 2014 Job Snijders <job@instituut.net>
#
# This file is part of ACLHound
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF TH

"""
The ACLHound command-line client assists in ACL management.

Usage: aclhound [-d] [--version] [--help] <command> [<args>...]

Options:
    -h --help       Show this screen
    -d --debug      Enable debugging output
    --version       Show version information

Subcommands, use 'aclhould help <subcommand>' to learn more:

    init        Initialise aclhound end-user configuration.
    fetch       Retrieve latest ACLHound policy from repository server.
    start       Start working on a new proposed change.
    diff-all    Compare all network configurations with the previous version.
    diff        Compare a single file with the previous version.
    submit      Push policy for review to repository server.
    build-all   Compile all ACLHound policy into network configurations.
    build       Compile a specific policy file into a network configuration.
    status      Show in which task you are currently working
"""

from __future__ import print_function, division, absolute_import, \
    unicode_literals

from docopt import docopt
from grako.exceptions import * # noqa
from grako.parsing import * # noqa
from subprocess import call

import ConfigParser
import os
import sys

import aclhound
from aclhound.aclsemantics import grammarSemantics
from aclhound.parser import grammarParser
from aclhound.render import Render


def parse_policy(filename, startrule='start', trace=False, whitespace=None):

    seen = [filename]

    def walk_file(filename, seen=[], policy=[]):
        try:
            f = open(os.path.join(filename)).read().splitlines()
        except IOError:
            print("filename %s referenced in %s does not exist"
                  % (filename, seen[-1]))
            sys.exit()
        for line in f:
            if line.startswith('@'):
                filename = "policy/%s" \
                    % line.split('#')[0][1:]
                if filename not in seen:
                    seen.append(filename)
                    policy = policy + walk_file(filename, seen, policy)
            elif line.startswith(('allow', 'deny')) and line not in policy:
                policy.append(line)
        return policy

    parser = grammarParser(parseinfo=False, semantics=grammarSemantics())
    acl = Render(name="test")
    for line in walk_file(filename, seen):
        ast = parser.parse(line, startrule)
        acl.add(ast)
    output = "\n".join(acl.output(vendor="ciscoasa"))
    return output


class Settings(ConfigParser.ConfigParser):
    """
    Settings are a combination of system-wide settings and
    user specific settings.

    Configuration is derived by taking 'etc/aclhound/aclhound.conf'
    and overlaying that with '~/.aclhound/client.conf'
    """
    def __init__(self):
        """
        Test whether appropiate files exist, return config object
        """
        user_path = os.path.expanduser('~/.aclhound')
        if not os.path.exists('/etc/aclhound/aclhound.conf'):
            print("ERROR: Could not open /etc/aclhound/aclhound.conf")
            print("Has ACLHound been properly installed? Contact your admin")
            sys.exit(2)

        if not os.path.isdir(user_path):
            err = "~/.aclhound/ does not exist yet"
            raise Exception(err)
        elif not os.path.exists('%s/client.conf' % user_path):
            err = "~/.aclhound/client.conf does not exist yet"
            raise Exception(err)

        ConfigParser.ConfigParser.__init__(self)
        self.readfp(open('/etc/aclhound/aclhound.conf'))
        self.read([os.path.expanduser("~/.aclhound/client.conf")])


def do_init():
    """
    Initialise user-specific settings, ask the user for username on
    repository server, location to store aclhound policy, ask to make
    initial clone.

    Usage: aclhound init
    """

    print("""Welcome to ACLHound!

A few user-specific settings are required to set up the proper environment.
The settings can always be changed by editting the 'aclhound/client.conf'
file with a text editor.
""")

    import getpass
    suggested_username = getpass.getuser()
    username = raw_input("Username on Gerrit server [%s]: "
                         % suggested_username)
    if not username:
        username = suggested_username

    suggested_location = "~/aclhound"
    location = raw_input("Location for ACLHound datafiles [%s]: "
                         % suggested_location)
    if not location:
        location = suggested_location
    if not os.path.exists(os.path.expanduser("~/.aclhound")):
        os.mkdir(os.path.expanduser("~/.aclhound"), 0700)
    if not os.path.exists(os.path.expanduser(location)):
        os.mkdir(os.path.expanduser(location), 0700)

    # write
    cfgfile = open("%s/client.conf" % os.path.expanduser("~/.aclhound"), 'w')
    config = ConfigParser.ConfigParser()
    config.add_section('user')
    config.set('user', 'username', username)
    config.set('user', 'location', location)
    config.write(cfgfile)

    clone = raw_input("Make initial clone of repository data [y]: ")
    if not clone or clone == 'y':
        cfg = Settings()
        os.chdir(os.path.expanduser(location))
        run(['git', 'clone', 'ssh://%s@%s:%s/%s' %
             (username,
              cfg.get('gerrit', 'hostname'),
              cfg.get('gerrit', 'port'),
              cfg.get('gerrit', 'repository')), '.'])

        if not os.path.exists('.gitreview'):
            # create .gitreview file if it does not exist
            gerritcfg = ConfigParser.ConfigParser()
            gerritcfg.add_section('gerrit')
            gerritcfg.set('gerrit', 'host', cfg.get('gerrit', 'hostname'))
            gerritcfg.set('gerrit', 'project', cfg.get('gerrit', 'repository'))
            gerritcfg.write(open('.gitreview', 'w'))
            run(['git', 'add', '.gitreview'])
            run(['git', 'commit', '-am', 'add gitreview'])
            run(['git', 'push'])

        if not os.path.exists('.gitignore'):
            gitignore = open('.gitignore', 'w')
            gitignore.write('networkconfigs/**\n')
            gitignore.close()
            run(['git', 'add', '.gitignore'])
            run(['git', 'commit', '-am', 'add gitreview'])
            run(['git', 'push'])

        # create directories
        for directory in ['objects', 'devices', 'policy', 'networkconfig']:
            if not os.path.exists(directory):
                os.mkdir(directory)

        # setup the review hooks
        run(['git', 'review', '--setup'])

        # Rebase is better to work with in Gerrit, see
        # http://stevenharman.net/git-pull-with-automatic-rebase
        run(['git', 'config', '--local', 'branch.autosetuprebase', 'always'])


def run(cmd, return_channel=0):
    print('INFO: executing: %s' % ' '.join(cmd))
    ret = call(cmd)
    if not ret == 0:
        print("ERROR: executing '%s' failed." % ' '.join(cmd))
        print('HINT: investigate manually')
        sys.exit(2)


class ACLHoundClient(object):
    """
    An client which compiles abstract ACL policy into vendor-specific network
    configurations.
    """

    def __init__(self):
        try:
            self._settings = Settings()
        except Exception as err:
            print("ERROR: Whoops!")
            print("ERROR: %s" % " ".join(err.args))
            print("""HINT: possible config corruption, delete it and run 'aclhound init'""")
            sys.exit(2)
        os.chdir(os.path.expanduser(self._settings.get('user', 'location')))

    def status(self, args):
        """
        Show status of current working directory.

        Usage: aclhound status
        """
        run(['git', 'status', '--porcelain', '-b'], 1)

    def submit(self, args):
        """
        Submits changes for review.

        Usage: aclhound submit

        The 'submit' command will perform the following steps:
            * aclhound diff-all
            * git add -A *
            * git commit -a
            * git review -v
        """
        self.diff_all(args)
        run(['git', 'add', '-A', '*'])
        run(['git', 'commit', '-a'])
        run(['git', 'review'])
        print("INFO: submitted changes, returning to master branch")
        run(['git', 'checkout', 'master'])

    def diff_all(self, args):
        """
        Show differences between last commit and current files.

        Usage: aclhound diff-all
        """
        pass

    def diff(self, args):
        """
        Show difference for single device or policy between last commit and current state

        Usage: aclhound diff <filename> [(ios | asa | junos)]

        Arguments:
            <filename>
                The policy or device file for which a unified diff must be generated.
                When referring to a policy file, a vendor must be specified as well.
        """

    def start(self, args):
        """
        Start change process.

        Usage: aclhound start <taskname>

        Arguments:
            <taskname>
                Taskname refers to a JIRA ticket, or other reference by which the change
                will be known in the review system.
        """
        taskname = args['<taskname>']
        run(['git', 'checkout', '-b', taskname])
        print("INFO: You can now work on change %s" % taskname)
        print("INFO: When you are finished type 'aclhound submit'")

    def fetch(self, args):
        """
        Retrieve latest changes from the repository server.

        Usage: aclhound fetch
        """
        run(['git', 'checkout', 'master'])
        run(['git', 'remote', 'update'])
        run(['git', 'pull', '--rebase'])


#    print('assessing changes ... ')
#    if sys.argv[-1] == 'init':
#        print("""
#git clone ssh://gerrit.ecg.so:29418/ecg-networking
#cd ecg-networking
#git review --setup -v
#git checkout -B $project_name
#git add files
#git commit""")
#        sys.exit()
#
#    if sys.argv[-1] == 'help':
#        print("""
#To submit a patchset for review do the following steps
#* change files
#* git add *
#* git commit -a
#* git-review -v
#""")
#        sys.exit()
#
#    if sys.argv[-1] == 'build':
#        output = parse_policy('policy/management.acl')
#        print(output)
#        f = open('/opt/firewall-configs/testasa.asa', 'w')
#        f.write(output)
#        f.write('\n')
#        f.close()
#        sys.exit(0)



def trim(docstring):
    """
    Function to trim whitespace from docstring

    c/o PEP 257 Docstring Conventions
    <http://www.python.org/dev/peps/pep-0257/>
    """
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)


def parse_args(cmd):
    """
    Parses command-line args applying shortcuts and looking for help flags.
    """
    if cmd == 'help':
        cmd = sys.argv[-1]
        help_flag = True
    else:
        cmd = sys.argv[1]
        help_flag = False
    # convert - to _
    if '-' in cmd:
        cmd = '_'.join(cmd.split(':'))
    return cmd, help_flag


def main():
    """
    Create an ACLHound client, parse the arguments received on the command
    line, and call the appropiate method.
    """

    try:
        if sys.argv[1] == "init":
            do_init()
            sys.exit(0)
    except IndexError:
        pass
    cli = ACLHoundClient()
    args = docopt(__doc__, version=aclhound.__version__, options_first=True)
    cmd = args['<command>']
    cmd, help_flag = parse_args(cmd)
    # print help when asked
    if help_flag:
        if cmd != 'help' and cmd in dir(cli):
            print(trim(getattr(cli, cmd).__doc__))
            return
        if cmd == "init":
            print(trim(do_init.__doc__))
            return
        docopt(__doc__, argv=['--help'])
    if hasattr(cli, cmd):
        method = getattr(cli, cmd)
    else:
        raise DocoptExit('Found no matching command, try `aclhound help`')
    docstring = trim(getattr(cli, cmd).__doc__)
    if 'Usage: ' in docstring:
        args.update(docopt(docstring))
    method(args)

if __name__ == '__main__':
    main()
    sys.exit(0)
