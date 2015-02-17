#!/usr/bin/env python2.7
# Copyright (C) 2014-2015 Job Snijders <job@instituut.net>
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
# ARISING IN ANY WAY OUT OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
The ACLHound command-line client assists in ACL management.

Usage: aclhound [-d] [-j] [--version] [--help] <command> [<args>...]

Options:
    -h --help       Show this screen
    -d --debug      Enable debugging output
    -j --jenkins    Use jenkins environmental variables like WORKSPACE
    --version       Show version information

Subcommands, use 'aclhould help <subcommand>' to learn more:

    init        Initialise aclhound end-user configuration.
    fetch       Retrieve latest ACLHound policy from repository server.
    build       Compile policy into network configuration, output on STDOUT
    deploy      Deploy compiled configuration to a network device
    reset       Delete aclhound directory and fetch copy from repository.
"""

from __future__ import print_function, division, absolute_import, \
    unicode_literals

from docopt import docopt
from docopt import DocoptExit
from grako.exceptions import * # noqa
from grako.parsing import * # noqa
from subprocess import call, Popen, PIPE, check_output

import ConfigParser
import os
import sys

import aclhound
from aclhound.deploy import Deploy
from aclhound.generate import generate_policy


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


def do_init(args, write_config=True):
    """
    Initialise user-specific settings, ask the user for username on
    repository server, location to store aclhound policy, ask to make
    initial clone.

    Usage: aclhound [-d] init [--batch]

    Options:
        --batch     Automatically guess all settings (non-interactive mode).
    """
    if len(args) == 2:
        batch = True if args[1] == "--batch" else False

    if not batch:
        print("""Welcome to ACLHound!

A few user-specific settings are required to set up the proper
environment. The settings can always be changed by editting the
'aclhound/client.conf' file with a text editor.""")

    import getpass
    username = getpass.getuser()
    if not batch:
        username = raw_input("Username on Gerrit server [%s]: "
                             % username) or username

    location = "~/aclhound"
    if not batch:
        location = raw_input("Location for ACLHound datafiles [%s]: "
                             % location) or location
    if not os.path.exists(os.path.expanduser("~/.aclhound")):
        os.mkdir(os.path.expanduser("~/.aclhound"), 0700)
    if not os.path.exists(os.path.expanduser(location)):
        os.mkdir(os.path.expanduser(location), 0700)

    if write_config:
        cfgfile = open("%s/client.conf" % os.path.expanduser("~/.aclhound"), 'w')
        config = ConfigParser.ConfigParser()
        config.add_section('user')
        config.set('user', 'username', username)
        config.set('user', 'location', location)
        config.write(cfgfile)

    if not batch:
        clone = raw_input("Make initial clone of repository data [y]: ") or "y"
    elif batch:
        clone = 'y'
    if clone == 'y':
        cfg = Settings()
        if cfg.getboolean('general', 'local_only'):
            print("INFO: 'local_only' enabled in /etc/aclhound/aclhound.conf.")
            print("HINT: manually copy your data to %s"
                  % os.path.expanduser(location))
            print("INFO: git-review and gerrit intergration are skipped for now")
            return
        os.chdir(os.path.expanduser(location))
        run(['git', 'clone', 'ssh://%s@%s:%s/%s' %
             (username,
              cfg.get('gerrit', 'hostname'),
              cfg.get('gerrit', 'port'),
              cfg.get('gerrit', 'repository')), '.'], 0)

        if not os.path.exists('.gitreview'):
            # create .gitreview file if it does not exist
            gerritcfg = ConfigParser.ConfigParser()
            gerritcfg.add_section('gerrit')
            gerritcfg.set('gerrit', 'host', cfg.get('gerrit', 'hostname'))
            gerritcfg.set('gerrit', 'project', cfg.get('gerrit', 'repository'))
            gerritcfg.write(open('.gitreview', 'w'))
            run(['git', 'add', '.gitreview'], 0)
            run(['git', 'commit', '-am', 'add gitreview'], 0)
            run(['git', 'push'], 0)

        if not os.path.exists('.gitignore'):
            gitignore = open('.gitignore', 'w')
            gitignore.write('networkconfigs/**\n')
            gitignore.close()
            run(['git', 'add', '.gitignore'], 0)
            run(['git', 'commit', '-am', 'add gitreview'], 0)
            run(['git', 'push'], 0)

        # create directories
        for directory in ['objects', 'devices', 'policy', 'networkconfig']:
            if not os.path.exists(directory):
                os.mkdir(directory)

        # setup the review hooks
        run(['git', 'review', '--setup'], 0)

        # Rebase is better to work with in Gerrit, see
        # http://stevenharman.net/git-pull-with-automatic-rebase
        run(['git', 'config', '--local', 'branch.autosetuprebase', 'always'], 0)


def run(cmd, return_channel=0, debug=None):
    if return_channel == 0:
        print('INFO: executing: %s' % ' '.join(cmd))
        ret = call(cmd)
        if not ret == 0:
            print("ERROR: executing '%s' failed." % ' '.join(cmd))
            print('HINT: investigate manually')
            sys.exit(2)
    elif return_channel == 1:
        ret = check_output(cmd)
        if debug:
            print('INFO: executing: %s' % ' '.join(cmd))
            print(ret)
        return ret


class ACLHoundClient(object):
    """
    A client which compiles abstract ACL policy into vendor-specific network
    configurations.
    """

    def __init__(self, args):
        try:
            self._settings = Settings()
        except Exception as err:
            print("ERROR: Whoops!")
            print("ERROR: %s" % " ".join(err.args))
            print("""HINT: possible config corruption, delete it and run 'aclhound init'""")
            sys.exit(2)
        if args['jenkins'] and 'WORKSPACE' in os.environ:
            data_dir = os.environ['WORKSPACE']
        else:
            data_dir = os.path.expanduser(self._settings.get('user', 'location'))
        os.chdir(data_dir)
        print("INFO: working with data in %s" % data_dir)

    def fetch(self, args):
        """
        Retrieve latest changes in 'master' from the repository server.

        Usage: aclhound fetch
        """
        run(['git', 'checkout', 'master'])
        run(['git', 'remote', 'update'])
        run(['git', 'pull', '--rebase'])
        run(['git', 'pull', '--all', '--prune'])

    def build(self, args):
        """
        Show unified build between last commit and current state.

        Usage: aclhound [-d] [-j] build <devicename>
               aclhound [-d] [-j] build all

        Options:
            -d --debug      Enable debugging output
            -j --jenkins    Use jenkins environmental variables like WORKSPACE

        Arguments:
          <devicename>
            The device file for which a network config must be generated.

          <all>
            Build all network policies into their respective vendor specific
            representation. Useful as 'review' test in Jenkins.

        Note: please ensure you run 'build' inside your ACLHound data directory
        """
        if args['<devicename>'] == "all":
            import glob
            devices_list = set(glob.glob('devices/*')) - \
                set(glob.glob('devices/*.ignore'))
        else:
            devices_list = [args['<devicename>'].encode('ascii', 'ignore')]

        def go_build(filename):
            print("INFO: building configuration for %s" % filename)
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.split(' ')[0] == "vendor":
                        vendor = line.split(' ')[1]
                    elif line.split(' ')[0] == "transport":
                        transport = line.split(' ')[1]
                        if transport not in ['telnet', 'ssh']:
                            print("ERROR: unknown transport mechanism: %s" % transport)
                            sys.exit(2)
                    elif line.split(' ')[0] == "include":
                        polname = line.split(' ')[1]
                        print("")
                        print("")
                        print("Seed policy name: %s" % polname)
                        print("   IPv4:")
                        for line in generate_policy(polname, afi=4,
                                                    vendor=vendor).split('\n'):
                            print("   %s" % line)
                        print("     ---------")
                        print("   IPv6:")
                        for line in generate_policy(polname, afi=6,
                                                    vendor=vendor).split('\n'):
                            print("   %s" % line)
            print("")

        for device in devices_list:
            go_build(device)

    def deploy(self, args):
        """
        Deploy a compiled version of the ACLs on a network device

        Usage: aclhound [-d] [-j] deploy <devicename>
               aclhound [-d] [-j] deploy all

        Options:
            -d --debug      Enable debugging output
            -j --jenkins    Use jenkins environmental variables like WORKSPACE

        Arguments:
          <devicename>
            Hostname of the device on which the generated ACLs must be
            deployed.

         <all>
            ACLHound will take all device files from devices/ (except
            filenames with a '.ignore' suffix), compile the policy and
            upload the policies to the device. "all" is suitable for cron or
            jenkins.

        Note: please ensure you run 'deploy' inside your ACLHound data directory
        """
        if args['<devicename>'] == "all":
            import glob
            devices_list = set(glob.glob('devices/*')) - \
                set(glob.glob('devices/*.ignore'))
        else:
            devices_list = [args['<devicename>'].encode('ascii', 'ignore')]

        def do_deploy(filename):
            print("INFO: deploying %s" % filename)
            acls = {}
            hostname = os.path.basename(filename)
            with open(filename, 'r') as f:
                timeout = 60
                transport = "ssh"
                for line in f:
                    line = line.strip()
                    if line.split(' ')[0] == "vendor":
                        vendor = line.split(' ')[1]
                    elif line.split(' ')[0] == "transport":
                        transport = line.split(' ')[1]
                        if transport not in ['telnet', 'ssh']:
                            print("ERROR: unknown transport mechanism: %s" % transport)
                            sys.exit(2)
                    elif line.split(' ')[0] == "save_config":
                        save_config = str2bool(line.split(' ')[1])
                    elif line.split(' ')[0] == "timeout":
                        timeout = int(line.split(' ')[1])

                    elif line.split(' ')[0] == "include":
                        polname = line.split(' ')[1]
                        for afi in [4, 6]:
                            name = "%s-v%s" % (polname, afi)
                            policy = generate_policy(vendor=vendor,
                                                     filename=polname,
                                                     afi=afi)
                            acls[name] = {"afi": afi,
                                          "name": name,
                                          "policy": policy}
            a = Deploy(hostname=hostname, vendor=vendor, acls=acls,
                       transport=transport, save_config=save_config,
                       timeout=timeout)
            a.deploy()

        for dev in devices_list:
            do_deploy(dev)

    def reset(self, args):
        """
        Reset ACLHound data directory by deleting the directory, followed
        by a fresh clone based on ~/.aclhound/client.conf settings

        Usage: aclhound reset

        If you are terribly lost in branches and git voodoo, this is an
        easy way out.
        """

        location = os.path.expanduser(self._settings.get('user', 'location'))
        confirm = raw_input("Do you want to destroy all local work (%s) and start over? [yn] " \
                            % location)
        if confirm == "y":
            import shutil
            os.chdir(os.path.expanduser('~'))
            shutil.rmtree(location)
            do_init((None, "--batch"), write_config=False)
        else:
            print("INFO: Did not touch anything...")


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


def print_debug(func, *args):
    print('in function %s():' % func)
    from pprint import pprint
    for arg in args:
        pprint(arg)
    print('-----')

def str2bool(configstring):
    return configstring.lower() in ("yes", "true", "t", "1")

def main():
    """
    Create an ACLHound client, parse the arguments received on the command
    line, and call the appropiate method.
    """

    try:
        if sys.argv[1] == "init":
            do_init(sys.argv)
            sys.exit(0)
    except IndexError:
        pass
    args = docopt(__doc__, version=aclhound.__version__, options_first=True)
    args['debug'] = args.pop('--debug')
    args['jenkins'] = args.pop('--jenkins')
    cmd = args['<command>']
    cli = ACLHoundClient(args)

    help_flag = True if cmd == "help" else False

    # first parse commands in help context
    if help_flag:
        # concat first and second argument to get real function name
        cmd = "_".join(args['<args>'][0:2])
        # see if command is a function in the cli object
        if cmd in dir(cli):
            print(trim(getattr(cli, cmd).__doc__))
            return
        # init is special because we don't want to depend on _settings
        elif cmd == "init":
            print(trim(do_init.__doc__))
            return
        docopt(__doc__, argv=['--help'])

    if hasattr(cli, cmd):
        # lookup function method for a given subcommand
        method = getattr(cli, cmd)
    else:
        # display help message if command not found in cli object
        raise DocoptExit("Found no matching command, try 'aclhound help'")

    docstring = trim(getattr(cli, cmd).__doc__)
    if 'Usage: ' in docstring:
        args.update(docopt(docstring))
    method(args)

if __name__ == '__main__':
    main()
    sys.exit(0)
