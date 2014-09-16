ACLHOUND
========

[![Build Status](https://travis-ci.org/job/aclhound.svg?branch=master)](https://travis-ci.org/job/aclhound)
[![Coverage Status](https://coveralls.io/repos/job/aclhound/badge.png)](https://coveralls.io/r/job/aclhound)

Summary
-------

ACLHound takes as input policy language following a variant of the [AFPL2] [1]
syntax and compiles a representation specific for the specified vendor which
can be deployed on firewall devices.

Table of contents
-----------------

- [Design goals](#design-goals)
- [Supported devices](#supported-devices)
- [Installation notes](#installation-notes)
- [Copyright and license](#copyright-and-license)

Design goals
------------

ACLHound is designed to assist humans in managing hundreds of ACLs across 
tens of devices. One key focus point is maximum re-usability of ACL 
components such as groups of hosts, groups of ports and the policies 
themselves.

Supported devices 
-----------------

* Cisco ASA
* Cisco VSS (IOS)
* Juniper

Installation notes
------------------

Step 1: get the code

```
git clone https://github.com/job/aclhound.git
cd aclhound
virtualenv .
source ./bin/activate
pip install -r requirements.txt
make test
python setup.py install
```

Step 2: intergrate with Gerrit

Install [Jenkins] [2] with the [Gerrit Trigger] [3] plugin.

Copyright and license
---------------------

Copyright 2014 Job Snijders. Code and documentation released under the BSD
2-Clause license.


[1]: http://www.lsi.us.es/~quivir/sergio/DEPEND09.pdf "AFPL2"
[2]: http://jenkins-ci.org/ "Jenkins"
[3]: https://wiki.jenkins-ci.org/display/JENKINS/Gerrit+Trigger "Gerrit Trigger"
