##Working with ACLhound

If ACLhound hasn't been installed, please see INSTALL-CONFIG.md

###Directory structure/Syntax</span>
*   devices
*   policy
*   objects
*   networkconfigs (future use)

### Devices

In &quot;devices&quot; directory you add the devices which you want under control of ACLhound. It's just a text file, and it contains a couple of variables.

*   vendor, this defines what OS the device is running, currently it supports : ios, asa, junos
*   transport, this defines how aclhound should connect to the device to deploy the acl. There's 2 options here: telnet &amp; ssh
*   include statements, these mention the policies that you would like to put on the devices. Multiple entries are allowed here.

### Policies

In the 'policy' directory you'll add text files that contain the actual ACL name that you are building. The name that you choose here, is also the name of the ACL on the device you deploy the policy to. In this textfile, type the complete ACL as you want it. Keep in mind, that ACLhound automatically adds a &quot;deny any&quot; statement at the end of each ACL, so you don't have to do that, and it keeps your behaviour consistent. Now if you want to log certain denied traffic, you can always add a &quot;deny any any log&quot; statement as your last line. (same theory goes for allowing traffic). Another thing to keep in mind,B <span style="line-height: 1.4285715;">remarks are not being pushed towards the device, as it won't make sense once the actual ACL is compiled and being pushed (you'll end up with more (unclear) remarks then actual ACL lines)</span>

These policies are a variation of the AFPL2 language and are build as following:
<table><tr><td class="wysiwyg-macro-body"><pre>&lt; allow | deny > \
&lt; tcp | udp | any > \
src &lt; prefix | $ip | @hostgroup | any > [ port number | range | @portgroup | any ]
dst &lt; prefix | $ip | @hostgroup | any > [ port number | range | @portgroup | any ]
[ stateful ] \
[ expire YYYYMMDD ] [ log ] \
[ # comment ]

&lt; allow | deny > &lt; icmp > &lt; any | type &lt;code|any> >
src &lt; prefix | $ip | @hostgroup | any > 
dst &lt; prefix | $ip | @hostgroup | any >
[ expire YYYYMMDD ] [ log ] \
[ # comment ]</pre></td></tr></table>

Some examples to take a look at:
<table ><tr><td class="wysiwyg-macro-body"><pre>allow tcp src 10.0.0.0/8 port any dst 2.2.2.2 port 80 stateful # test
deny tcp src 2.2.2.2 dst 2.2.2.2
allow tcp src 2.2.2.2 dst 10.0.0.0/8 port 15-10
allow tcp src 2.2.2.2 dst 10.0.0.0/8 port 5-10 expire 20140504
allow tcp src @mp-servers dst 10.0.0.0/8
deny tcp src @bgp-peers port any dst @mp-servers port @webports # another comment
allow tcp src 2.2.2.2 port 1 dst 10.0.0.0/8 port 2,1-2,4
allow tcp src 2.2.2.2 port 1 dst 10.0.0.0/8 port 2,2,3,4
allow icmp 128 0 src any dst 192.0.2.0/24 # icmpv6 echo request
allow icmp 129 0 src 192.0.2.0/24 dst any # icmpv6 echo reply</pre></td></tr></table>

As you can see, the policies allow for inclusion of object files, there are 2 type of object inclusion possibilities: hosts &amp; ports. There's something tricky (it uses a suffix) with their filenames which is explained in &quot;Objects&quot;.

### Objects

In the 'objects' directory you'll add text files which contain well, objects. There's 2 types of these:

*   hosts: These are files which contain hosts or host ranges. Use single IPs or class notation (ie /24, /25) per line
*   ports: These are files which contain ports. Use single port numbers per line

In order for the proper files to be included in the policy, name them accordingly. So for filenames use objectname.ports for a ports file, and use objectname.hosts for a file filled with host entries.

### ExampleB 

So, let's do an example where we touch everything. When setting up a basic ACL on a specific device you touch all 3 directories: devices, objects &amp; policy.

This example that is outlined below is only for local usage, it doesn't cover integration with GIT/Gerrit/Jenkins

Keep in mind, bindings of ACL's to specific interfaces are not setup within ACLhound, you do need to configure this on the device itself. However ACLHound does detect during deploymentB to which interfaces ACL's are bound, and does a neat trick with some switching (LOCKSTEP process) during uploading/applyingB to have the new ACL applied without any impact.

Let's assume we're creating a simple rule, let's say we want to have an ACL that allows all SSH, HTTP &amp; HTTPS (as requested in SO-99999) traffic from an marktplaats-ops vlan 10.32.1.0/24 towards marktplaats-web vlan 10.32.2.0/24, and we want to apply this on machine fw001.

#### **First step**

Create the device by editing a new file in the devices directory:

*   vi ~/aclhound/devices/fw001

Insert this content:
<pre>   vendor asa
   transport ssh
   include nw-management</pre>

#### **Second step**

Create the objects required (marktplaats-ops &amp; marktplaats-web)

*   vi ~/aclhound/objects/marktplaats-ops.hosts
*   edit it to contain 10.32.1.0/24
*   vi ~/aclhound/objects/marktplaats-web.hosts
*   edit it to contain 10.32.2.0/24

#### **Third step**

Create the actual policy:

*   vi ~/aclhound/policy/marktplaats-ops-web-so-99999
*   edit it to contain:<pre>      allow tcp src @marktplaats-ops port any dst @marktplaats-web port 22
      allow tcp src @marktplaats-ops port any dst @marktplaats-web port 80
      allow tcp src @marktplaats-ops port any dst @marktplaats-web port 443</pre>

You have now created the policies, objects, and the devices.

#### **Fourth step**

To check for syntax, type:

*   aclhound build

#### **Fifth step**

If this succeeded, then you can deploy this towards the devices as well with:

*   aclhound deploy &lt;devicename|all&gt;

### **Building**

Now to actually check these ACL's we'll need to compile them into a format that is understandable by the device you're deploying to.B 

Use:

*   aclhound build &lt;devicename|all&gt;

### **Deploying**

Once you have done the syntax check above, and you have no problems anymore, you can safely deploy the policies towards the device:

Use:

*   aclhound deploy &lt;devicename|all&gt;

### How to work and submit code with aclhound in combination with GIT/Gerrit/Jenkins

To be written

* * *

