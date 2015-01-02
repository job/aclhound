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
    * No support for ASA 9.1.2 or higher (yet)
* Cisco IOS
    * Will autodetect IPv6 support through ```show ipv6 cef```
* Juniper (planned)

Installation notes
------------------

Step 1: get the code

```
sudo pip install aclhound
```

Copyright and license
---------------------

Copyright 2014,2015 Job Snijders. Code and documentation released under the BSD
2-Clause license.

ACLHound's inception was commissioned by the eBay Classifieds Group.

[1]: http://www.lsi.us.es/~quivir/sergio/DEPEND09.pdf "AFPL2"
[2]: http://jenkins-ci.org/ "Jenkins"
[3]: https://wiki.jenkins-ci.org/display/JENKINS/Gerrit+Trigger "Gerrit Trigger"
