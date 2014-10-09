# Copyright (C) 2014 Job Snijders <job@instituut.net>
# Copyright (C) 2011-2013 Kristian Larsson, Lukas Garberg
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
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import ConfigParser

class AclhoundConfig(ConfigParser.SafeConfigParser):
    """ Makes configuration data available.

        Implemented as a class with a shared state; once an instance has been
        created, new instances with the same state can be obtained by calling
        the custructor again.
    """

    __shared_state = {}
    _config = None
    _cfg_path = None

    def __init__(self, cfg_path=None, default={}):
        """ Takes config file path and command line arguments.
        """

        self.__dict__ = self.__shared_state
        if len(self.__shared_state) == 0:
            # First time - create new instance!
            self._cfg_path = cfg_path
            ConfigParser.ConfigParser.__init__(self, default)
            self.read_file()

    def read_file(self):
        """ Read the configuration file
        """

        # don't try to parse config file if we don't have one set
        if not self._cfg_path:
            return
        try:
            cfg_fp = open(self._cfg_path, 'r')
            self.readfp(cfg_fp)
        except IOError as exc:
            raise AclhoundConfigError(str(exc))

class AclhoundConfigError(Exception):
    pass
