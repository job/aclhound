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
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import sys

from targets import deploy_ios
from targets import deploy_asa
#from targets import deploy_junos


class Deploy():

    def __init__(self,
                 hostname=None,
                 acls=[],
                 vendor=None,
                 transport='ssh',
                 save_config=False,
                 timeout=60):
        self.hostname = hostname
        self.acls = acls
        self.vendor = vendor
        self.transport = transport
        self.save_config = save_config
        self.timeout = timeout

    def deploy(self):
        if not self.vendor:
            sys.exit(2)
        return getattr(self, 'deploy_' + self.vendor)()

    def deploy_ios(self):
        return deploy_ios.deploy(hostname=self.hostname,
                                 acls=self.acls,
                                 transport=self.transport,
                                 save_config=self.save_config,
                                 timeout=self.timeout)

    def deploy_asa(self):
        return deploy_asa.deploy(hostname=self.hostname,
                                 acls=self.acls,
                                 transport=self.transport,
                                 save_config=self.save_config)
# TODO add juniper support
#    def deploy_junos(self, **kwargs):
#        return junos.deploy(self, **kwargs)
