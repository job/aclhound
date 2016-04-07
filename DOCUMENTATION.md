[link_install-config]: https://github.com/job/aclhound/blob/master/INSTALL-CONFIG.md
[link_maarten-moerman]: https://github.com/mgmoerman

#Working with ACLhound

If ACLhound hasn't been installed or configured, please see [INSTALL-CONFIG.md][link_install-config]

This documentation will explain to you how to work with ACLhound to get objects into policies, and deploy them to devices.

##Directory structure/Syntax

In order to fully understand ACLhound and its operation, it is of most importance that you understand its directory structure, as this is where you'll be spending most of your time when building ACLs.

The root directory containing the ACLs is defined in `~/.aclhound/client.conf` (e.g., `location = ~/aclhound`).  This directory should be checked into version control, and an appropriate workflow defined for reviewing and accepting changes.

The root directory contains the following subdirectories:

*   devices
*   policy
*   objects
*   networkconfigs (future use)

### Directory : devices

In the &quot;devices&quot; directory you'll add the devices which you want under control of ACLhound. It's just a text file, and it contains a couple of variables.

*   vendor, this defines what OS the device is running, currently it supports : 
    * ios
    * asa
    * junos
*   transport, this defines how ACLhound should connect to the device to deploy ACLs. There's 2 options here: telnet &amp; ssh
*   save_config, this defines wether you want to save the configuration onto the device after a deployment has been done. There's 2 options here: true & false. If not specified, it defaults to false.
*   include statements, these mention the policies that you would like to put on the devices. Multiple entries are allowed here.

Example device file:

```
mmoerman@aclhound001:~/aclhound$ cat devices/fw001
vendor ios
transport ssh
save_config true
include nw-management
include test-policy
```


### Directory : policy

In the 'policy' directory you'll add text files that contain the actual ACL that you are building. The name that you choose here, is also the name of the ACL on the device you deploy the policy to. In this textfile, type the complete ACL as you want it. 

#### Policy language
The syntax for this is a variation of the AFPL2 language and is as following:


	< allow | deny > \
	< tcp | udp | any > \
	src < prefix | $ip | @hostgroup | any > [ port number | range | @portgroup | any ] \
	dst < prefix | $ip | @hostgroup | any > [ port number | range | @portgroup | any ] \
	[ stateful ] \
	[ expire YYYYMMDD ] [ log ] \
	[ # comment ]

	< allow | deny > < icmp > < any | type <code|any> > \ 
	src < prefix | $ip | @hostgroup | any > \
	dst < prefix | $ip | @hostgroup | any > \
	[ expire YYYYMMDD ] [ log ] \
	[ # comment ]
	
	@policy_name

##### Range statement

Ranges can be configured in three different ways:

*    Specified as an actual range: 1024-2048 , this specifies port 1024 upto and including 2048
*    Specified as "greater then": 1024- , this specifies port 1024 up to and including 65535 
*    Specified as "less then": -1024 , this specifies port 0 up to and including 1024

##### Expire statement
Note the expire statement. This is something that does not translate as part of an ACL to the device, but is used during the build & deployment process to check if a certain policy/ACL is still valid. Once past the date mentiond in the expire statement, it will not be pushed towards the device.

#### Policy behaviour
Policies allow for inclusions, there are 3 type of object inclusion possibilities: 

*    hosts 
*    ports
*    policies

You do these inclusions by adding an @ sign in front of it. Now hosts & ports use a suffix with their filenames, which is explained in &quot;Objects&quot;. Policies can simple be included by just including the policy on a single line (@policy_name).

Keep in mind, that ACLhound does automatically add a &quot;deny any&quot; statement at the end of each ACL, so you don't have to do that yourself, this also keeps behaviour consistent across devices. 

Tip: If you want to log certain denied traffic, you can always add a &quot;deny any any log&quot; statement as your last line. (same theory goes for allowing traffic). 

With regards to IPv4 & IPv6, ACLhound doesn't care if you mix and match IPv4 & IPv6 in a policy, it will just build/output 2 ACLs, one for IPv4 , and one for IPv6. These will have the suffix -v4 or -v6. 

ACLhound is smart as in, it identifies if rules that are built are IP version specific and puts them in the correct (IPv4 or IPv6) ACL. If they are generic, such as "deny any any log", it will place them in both IPv4 and IPv6 ACLs.

One last thing to keep in mind, remarks/comments are not being pushed towards the device, as it won't make sense once the actual ACL is compiled and being pushed, as you might end up with the same or more amount of remarks (because of iteration that could take place) then actual ACL lines.

####Example:

	allow tcp src 10.0.0.0/8 port any dst 2.2.2.2 port 80 stateful # test
	deny tcp src 2.2.2.2 dst 2.2.2.2
	allow tcp src 2.2.2.2 dst 10.0.0.0/8 port 15-10
	allow tcp src 2.2.2.2 dst 10.0.0.0/8 port 5-10 expire 20140504
	allow tcp src @mp-servers dst 10.0.0.0/8
	deny tcp src @bgp-peers port any dst @mp-servers port @webports # another comment
	allow tcp src 2.2.2.2 port 1 dst 10.0.0.0/8 port 2,1-2,4
	allow tcp src 2.2.2.2 port 1 dst 10.0.0.0/8 port 2,2,3,4
	allow icmp 128 0 src any dst 192.0.2.0/24 # icmpv6 echo request
	allow icmp 129 0 src 192.0.2.0/24 dst any # icmpv6 echo reply



### Directory : objects

In the 'objects' directory you'll add text files which contain either hosts/subnets or ports

*   hosts: These are files which contain hosts or host ranges. Use single IPs or class notation (ie /24, /25) per line
*   ports: These are files which contain ports. Use single port numbers per line

In order for the proper files to be included in the policy, name them accordingly. So  filename wise use objectname.ports for a ports file, and use objectname.hosts for a file filled with host entries.

Examples could be:

	mmoerman@aclhound001:~/aclhound$ cat objects/mailcluster.hosts
	10.32.2.0/24
	10.34.2.2
	10.34.2.3
	
	mmoerman@aclhound001:~/aclhound$ cat objects/mailcluster.ports
	25
	110
	143
	993
	465

## Building & Deploying with ACLhound
### Building

Building the ACLs for one or all devices is done by executing:

    aclhound build <devicename|all>

This will perform a syntax check and output the complete ACL's on stdout of what you have defined in the object & policy directories for either a specific device, or all of them.

### Deploying

Deploying the ACLs towards one or all devices is done by executing:

    aclhound deploy <devicename|all>

This will perform a deployment of what you have defined in the object & policy directories for either a specific device, or all of them.

ACLhound expects a properly set up .netrc file if you want it to run automated. Otherwise it will just ask you to authenticate for all of the devices you are deploying to.

With regards to IPv4 & IPv6, ACLhound checks during deployment if the device is capable of IPv6, and only deploys these IPv6 ACLs when the device is actually capable of doing so. On Cisco IOS this is done by checking the output of the 'show ipv6 cef' command. Cisco ASA does do proper IPv6 already (keep in mind, currently, version 1.5 does not support ASA software 9.1.2 or higher).

There's a little trick going on the first time you are deploying ACLs to a device, as it will rename the existing ACLs, and replace them with a -v4 or -v6 suffix. See also next topic on actual binding, and the LOCKSTEP process.

#### ACL bindings / LOCKSTEP process
Binding of ACLs to specific interfaces is not setup within ACLhound. You do need to configure this on the device itself. This is only for the initial binding of a specific ACL on an interface. When deploying, ACLHound does detect to which interfaces ACLs are bound, and does a neat trick with some switching (LOCKSTEP process) during uploading/applying to have the new ACL applied without any impact.

This process is as follows:

*   Upload ACL with -LOCKSTEP suffix
*   Change ACL on interface towards the new ACL with the -LOCKSTEP suffix
*   Remove old ACL
*   Upload ACL without suffix
*   Change ACL on interface towards the new ACL without the suffix


---
## Building something real

So, let's do an example where we touch everything. Let's assume we're creating a simple rule, let's say we want to have an ACL that allows all SSH, HTTP &amp; HTTPS  traffic from an ops vlan 10.32.1.0/24 towards a web vlan 10.32.2.0/24, and we want to apply this on machine fw001.

We will break this down in 5 steps:

*   Creating device file
*   Creating objects that are mentioned in the device file
*   Creating policies that include objects
*   Do syntax checking
*   Deploy ACL


### **First step**

Create the device by editing a new file in the devices directory:

    vi ~/aclhound/devices/fw001

Insert this content:

	vendor asa
	transport ssh
	save_config true
	include ops-2-web-traffic

### **Second step**

Create the objects required (ops &amp; web)

*   vi ~/aclhound/objects/ops.hosts
*   edit it to contain 10.32.1.0/24
*   vi ~/aclhound/objects/web.hosts
*   edit it to contain 10.32.2.0/24

### **Third step**

Create the actual policy:

*   vi ~/aclhound/policy/ops-2-web-traffic
*   edit it to contain:

		allow tcp src @ops port any dst @web port 22
		allow tcp src @ops port any dst @web port 80
		allow tcp src @ops port any dst @web port 443

You have now created the policies, objects, and the devices.


### **Fourth step**

Now to actually check these ACL's we'll need to compile them into a format that is understandable by the device you're deploying to.

Use:

	aclhound build ~/aclhound/devices/fw001
	
### **Fifth step**

Once you have done the syntax check above, and you have no problems anymore, you can safely deploy the policies towards the device (assuming you have correctly setup your .netrc file):

Use:

	aclhound deploy ~/aclhound/devices/fw001

---

######Documentation written by [Maarten Moerman][link_maarten-moerman]. Remarks or suggestions are very much welcome.