ACLHOUND
========

Summary
-------

ACLHound takes as input policy language following a variant of the [AFPL2] [1]
syntax and compiles a representation specific for the specified vendor which
can be deployed on firewall devices.

Supported Devices
-----------------

* Cisco ASA
* Cisco VSS
* Juniper

Installation notes
------------------

```
git clone https://github.com/job/aclhound.git
cd aclhound
virtualenv .
source ./bin/activate
pip install -r requirements.txt
./bin/test.py
```

[1]: http://www.lsi.us.es/~quivir/sergio/DEPEND09.pdf "AFPL2"
