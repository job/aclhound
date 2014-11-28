#Working with ACLhound

If ACLhound hasn't been installed, please see INSTALL-CONFIG.md

This documentation will explain to you how to work with ACLhound to get objects into policies, and deploy them to devices.

##Directory structure/Syntax</span>
In order to fully understand ACLhound and it's working, it is of most importance that you understand it's directory structure, as this is where you'll be spending all of your time from now on when you are building ACLs. These are the directories:

*   devices
*   policy
*   objects
*   networkconfigs (future use)

### Devices

In &quot;devices&quot; directory you add the devices which you want under control of ACLhound. It's just a text file, and it contains a couple of variables.

*   vendor, this defines what OS the device is running, currently it supports : 
    * ios
    * asa
    * junos
*   transport, this defines how aclhound should connect to the device to deploy the acl. There's 2 options here: telnet &amp; ssh
*   include statements, these mention the policies that you would like to put on the devices. Multiple entries are allowed here.

Example device file:

	mmoerman@aclhound001:~/aclhound$ cat devices/fw001
	vendor ios
	transport ssh
	include nw-management
	include test-policy


### Policies

In the 'policy' directory you'll add text files that contain the actual ACL that you are building. The name that you choose here, is also the name of the ACL on the device you deploy the policy to. In this textfile, type the complete ACL as you want it. The syntax for this is a variation of the AFPL2 language and is as following:


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

Note the @ sign, the policies allow for inclusion of object files, there are 2 type of object inclusion possibilities: hosts &amp; ports. Now this uses a suffix with their filenames, which is explained in &quot;Objects&quot;.

Keep in mind, that ACLhound automatically adds a &quot;deny any&quot; statement at the end of each ACL, so you don't have to do that yourself, this also keeps behaviour consistent across devices. 

Now if you want to log certain denied traffic, you can always add a &quot;deny any any log&quot; statement as your last line. (same theory goes for allowing traffic). 

Another thing to keep in mind, remarks are not being pushed towards the device, as it won't make sense once the actual ACL is compiled and being pushed because you'll end up with more (unclear) remarks then actual ACL lines.

Some examples to take a look at:

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




### Objects

In the 'objects' directory you'll add text files which contain either hosts/subnets or ports

*   hosts: These are files which contain hosts or host ranges. Use single IPs or class notation (ie /24, /25) per line
*   ports: These are files which contain ports. Use single port numbers per line

In order for the proper files to be included in the policy, name them accordingly. So for filenames use objectname.ports for a ports file, and use objectname.hosts for a file filled with host entries.

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

## Building something real

So, let's do an example in 5 steps where we touch everything. The example that is outlined below is only for local usage, it doesn't cover integration with GIT/Gerrit/Jenkins, documentation for this is not finished.

These 5 steps are:

*   Creating device file
*   Creating objects that are mentioned in the device file
*   Creating policies that include objects
*   Do syntax checking
*   Deploy ACL

Keep in mind, bindings of ACL's to specific interfaces are not setup within ACLhound, you do need to configure this on the device itself. However ACLHound does detect during deployment to which interfaces ACL's are bound, and does a neat trick with some switching (LOCKSTEP process) during uploading/applying to have the new ACL applied without any impact.

Let's assume we're creating a simple rule, let's say we want to have an ACL that allows all SSH, HTTP &amp; HTTPS (as requested in ticket-067) traffic from an ops vlan 10.32.1.0/24 towards web vlan 10.32.2.0/24, and we want to apply this on machine fw001.

### **First step**

Create the device by editing a new file in the devices directory:

*   vi ~/aclhound/devices/fw001

Insert this content:

	vendor asa
	transport ssh
	include ops-web-ticket-067

### **Second step**

Create the objects required (ops &amp; web)

*   vi ~/aclhound/objects/ops.hosts
*   edit it to contain 10.32.1.0/24
*   vi ~/aclhound/objects/web.hosts
*   edit it to contain 10.32.2.0/24

### **Third step**

Create the actual policy:

*   vi ~/aclhound/policy/ops-web-ticket-067
*   edit it to contain:

		allow tcp src @ops port any dst @web port 22
		allow tcp src @ops port any dst @web port 80
		allow tcp src @ops port any dst @web port 443

You have now created the policies, objects, and the devices.


### **Fourth step**

Now to actually check these ACL's we'll need to compile them into a format that is understandable by the device you're deploying to.

Use:

	aclhound build <devicename|all>
	
### **Fifth step**

Once you have done the syntax check above, and you have no problems anymore, you can safely deploy the policies towards the device (assuming you have correctly setup your .netrc file):

Use:

	aclhound deploy <devicename|all>

## How to work and submit code with aclhound in combination with GIT/Gerrit/Jenkins

To be written

* * *

Remarks or suggestions about this documentation? Send them to maarten.moerman (at) gmail.com
