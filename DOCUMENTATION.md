                    

<!DOCTYPE html>
<html>
    <head>
        <title>View Source</title>
        <link rel="canonical" href="/confluence/pages/viewpage.action?pageId=118429064" />
        <link type="text/css" rel="stylesheet" href="/confluence/s/d41d8cd98f00b204e9800998ecf8427e/en_GB-1988229788/4733/f235dd088df5682b0560ab6fc66ed22c9124c0be.44/46/_/download/superbatch/css/batch.css" media="all">
<link type="text/css" rel="stylesheet" href="/confluence/s/d41d8cd98f00b204e9800998ecf8427e/en_GB-1988229788/4733/f235dd088df5682b0560ab6fc66ed22c9124c0be.44/46/_/download/superbatch/css/batch.css?media=print" media="print">
<!--[if lt IE 9]>
<link type="text/css" rel="stylesheet" href="/confluence/s/d41d8cd98f00b204e9800998ecf8427e/en_GB-1988229788/4733/f235dd088df5682b0560ab6fc66ed22c9124c0be.44/46/_/download/superbatch/css/batch.css?conditionalComment=lt+IE+9" media="all">
<![endif]-->
<!--[if lte IE 8]>
<link type="text/css" rel="stylesheet" href="/confluence/s/d41d8cd98f00b204e9800998ecf8427e/en_GB-1988229788/4733/f235dd088df5682b0560ab6fc66ed22c9124c0be.44/46/_/download/superbatch/css/batch.css?conditionalComment=lte+IE+8" media="all">
<![endif]-->
<!--[if lte IE 9]>
<link type="text/css" rel="stylesheet" href="/confluence/s/d41d8cd98f00b204e9800998ecf8427e/en_GB-1988229788/4733/f235dd088df5682b0560ab6fc66ed22c9124c0be.44/46/_/download/superbatch/css/batch.css?conditionalComment=lte+IE+9" media="all">
<![endif]-->
<link type="text/css" rel="stylesheet" href="/confluence/s/d41d8cd98f00b204e9800998ecf8427e/en_GB-1988229788/4733/f235dd088df5682b0560ab6fc66ed22c9124c0be.44/1f2a9c4c7f2593422cc9b02d1a652a22/_/download/contextbatch/css/plugin.viewsource/batch.css" media="all">
<link type="text/css" rel="stylesheet" href="/confluence/s/d41d8cd98f00b204e9800998ecf8427e/en_GB-1988229788/4733/f235dd088df5682b0560ab6fc66ed22c9124c0be.44/dfa46ecdb6a33872de1ded6d909d4d7a/_/download/contextbatch/css/page/batch.css" media="all">
<!--[if lt IE 9]>
<link type="text/css" rel="stylesheet" href="/confluence/s/d41d8cd98f00b204e9800998ecf8427e/en_GB-1988229788/4733/f235dd088df5682b0560ab6fc66ed22c9124c0be.44/dfa46ecdb6a33872de1ded6d909d4d7a/_/download/contextbatch/css/page/batch.css?conditionalComment=lt+IE+9" media="all">
<![endif]-->
<link type="text/css" rel="stylesheet" href="/confluence/s/d41d8cd98f00b204e9800998ecf8427e/en_GB-1988229788/4733/f235dd088df5682b0560ab6fc66ed22c9124c0be.44/e62b44b7789ed5fb58ad434b837f6f01/_/download/contextbatch/css/editor-content/batch.css" media="all">
<link type="text/css" rel="stylesheet" href="/confluence/s/d41d8cd98f00b204e9800998ecf8427e/en_GB-1988229788/4733/f235dd088df5682b0560ab6fc66ed22c9124c0be.44/1.3/_/download/batch/com.atlassian.confluence.plugins.confluence-highlight-actions:highlighting-experiment-resources/com.atlassian.confluence.plugins.confluence-highlight-actions:highlighting-experiment-resources.css" media="all">
<!--[if lt IE 9]>
<link type="text/css" rel="stylesheet" href="/confluence/s/d41d8cd98f00b204e9800998ecf8427e/en_GB-1988229788/4733/f235dd088df5682b0560ab6fc66ed22c9124c0be.44/1.3/_/download/batch/com.atlassian.confluence.plugins.confluence-highlight-actions:highlighting-experiment-resources/com.atlassian.confluence.plugins.confluence-highlight-actions:highlighting-experiment-resources.css?conditionalComment=lt+IE+9" media="all">
<![endif]-->
<link type="text/css" rel="stylesheet" href="/confluence/s/en_GB-1988229788/4733/f235dd088df5682b0560ab6fc66ed22c9124c0be.44/7/_/styles/colors.css?spaceKey=RefInfrastructure" media="all">
<link type="text/css" rel="stylesheet" href="/confluence/s/en_GB-1988229788/4733/f235dd088df5682b0560ab6fc66ed22c9124c0be.44/7/_/styles/custom.css?spaceKey=RefInfrastructure" media="all">

    </head>

    <body class="mceContentBody aui-theme-default wiki-content fullsize">

&nbsp;

## Working with ACLhound

If ACLhound hasn't been installed, please scroll down for installation instructions

### <span style="color: rgb(0,0,0);font-size: 16.0px;line-height: 1.5625;">Directory structure/Syntax</span>
<div>

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

In the 'policy' directory you'll add text files that contain the actual ACL name that you are building. The name that you choose here, is also the name of the ACL on the device you deploy the policy to. In this textfile, type the complete ACL as you want it. Keep in mind, that ACLhound automatically adds a &quot;deny any&quot; statement at the end of each ACL, so you don't have to do that, and it keeps your behaviour consistent. Now if you want to log certain denied traffic, you can always add a &quot;deny any any log&quot; statement as your last line. (same theory goes for allowing traffic). Another thing to keep in mind, <span style="line-height: 1.4285715;">remarks are not being pushed towards the device, as it won't make sense once the actual ACL is compiled and being pushed (you'll end up with more (unclear) remarks then actual ACL lines)</span>

These policies are a variation of the AFPL2 language and are build as following:
<table class="wysiwyg-macro" data-macro-name="code" style="background-image: url(/confluence/plugins/servlet/confluence/placeholder/macro-heading?definition=e2NvZGV9&amp;locale=en_GB&amp;version=2); background-repeat: no-repeat;" data-macro-body-type="PLAIN_TEXT"><tr><td class="wysiwyg-macro-body"><pre>&lt; allow | deny > \
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

<span style="line-height: 1.4285715;">Some examples to take a look at:</span>
<table class="wysiwyg-macro" data-macro-name="code" style="background-image: url(/confluence/plugins/servlet/confluence/placeholder/macro-heading?definition=e2NvZGV9&amp;locale=en_GB&amp;version=2); background-repeat: no-repeat;" data-macro-body-type="PLAIN_TEXT"><tr><td class="wysiwyg-macro-body"><pre>allow tcp src 10.0.0.0/8 port any dst 2.2.2.2 port 80 stateful # test
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

In the 'objects' directory you'll add text files which contain well, objects ![(smile)](/confluence/s/en_GB-1988229788/4733/f235dd088df5682b0560ab6fc66ed22c9124c0be.44/_/images/icons/emoticons/smile.png "(smile)") There's 2 types of these:

*   hosts: These are files which contain hosts or host ranges. Use single IPs or class notation (ie /24, /25) per line
*   ports: These are files which contain ports. Use single port numbers per line

In order for the proper files to be included in the policy, name them accordingly. So for filenames use objectname.ports for a ports file, and use objectname.hosts for a file filled with host entries.

### Example 

So, let's do an example where we touch everything. When setting up a basic ACL on a specific device you touch all 3 directories: devices, objects &amp; policy.

This example that is outlined below is only for local usage, it doesn't cover integration with GIT/Gerrit/Jenkins

Keep in mind, bindings of ACL's to specific interfaces are not setup within ACLhound, you do need to configure this on the device itself. However ACLHound does detect during deployment to which interfaces ACL's are bound, and does a neat trick with some switching (LOCKSTEP process) during uploading/applying to have the new ACL applied without any impact.

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

#### 
**Third step**

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

### <span style="color: rgb(0,0,0);font-size: 16.0px;line-height: 1.5625;">Building</span>

Now to actually check these ACL's we'll need to compile them into a format that is understandable by the device you're deploying to. 

Use:

*   aclhound build &lt;devicename|all&gt;

### Deploying

Once you have done the syntax check above, and you have no problems anymore, you can safely deploy the policies towards the device:

Use:

*   aclhound deploy &lt;devicename|all&gt;

### How to work and submit code with aclhound in combination with GIT/Gerrit/Jenkins

tbd

* * *

Please don't go beyond here for information how to use aclhound on a daily basis, this is just for configuration and installation:

<span style="color: rgb(0,0,0);font-size: 24.0px;line-height: 1.25;">Installation / Configuration</span>
</div>

### How to install the package

To install the package, execute the following lines on the commandline:
<table class="wysiwyg-macro" data-macro-name="code" style="background-image: url(/confluence/plugins/servlet/confluence/placeholder/macro-heading?definition=e2NvZGV9&amp;locale=en_GB&amp;version=2); background-repeat: no-repeat;" data-macro-body-type="PLAIN_TEXT"><tr><td class="wysiwyg-macro-body"><pre>git clone https://github.com/job/aclhound.git
cd aclhound
virtualenv .
source ./bin/activate
pip install -r requirements.txt
make test
python setup.py install</pre></td></tr></table>

### <span style="color: rgb(0,0,0);font-size: 20.0px;line-height: 1.5;">Configuration files</span>

**aclhound.conf**

 This can be found in the /etc/aclhound/ directory.

 This configuration file is used to configure some base settings for aclhound itself, and 
 it contains settings to talke with jenkins &amp; gerrit.

 The following is an example configuration file:
<table class="wysiwyg-macro" data-macro-name="code" style="background-image: url(/confluence/plugins/servlet/confluence/placeholder/macro-heading?definition=e2NvZGV9&amp;locale=en_GB&amp;version=2); background-repeat: no-repeat;" data-macro-body-type="PLAIN_TEXT"><tr><td class="wysiwyg-macro-body"><pre> ; ACLHound system-wide configuration
[general]
local_only = false
policy_output_directory = /opt/aclhound/networkconfigs
project_name =
[jenkins]
hostname = aclhound001
port = 8080
username = aclhound
password =
[gerrit]
hostname = gerrit001
port = 29418
repository = aclhound-repos
protocol = ssh
[user]
username =
location =</pre></td></tr></table>

**
**

**~/aclhound/.gitreview**

 This file is populated during the first/initialization run (see next chapter) of aclhound
 It contains the parameters to connect to gerrit

 Example config:
<table class="wysiwyg-macro" data-macro-name="code" style="background-image: url(/confluence/plugins/servlet/confluence/placeholder/macro-heading?definition=e2NvZGV9&amp;locale=en_GB&amp;version=2); background-repeat: no-repeat;" data-macro-body-type="PLAIN_TEXT"><tr><td class="wysiwyg-macro-body"><pre> [gerrit]
 host=gerrit.ecg.so
 port=29418
 project=aclhound-repos.git</pre></td></tr></table>

**
.netrc**

 This file needs to be manually edited. This contains login information to do deployments 
 from the commandline using the aclhound tool (automatic logins) 
 Documentation on .netrc can be found here: 
 [http://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-File.html](http://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-File.html)

## <span style="line-height: 1.5;"> </span>

## **First run**

## <span style="line-height: 1.5;"> </span>

To deploy a clean working directory for ACLHound, login as a normal user on a system which 
has the ACLHound software installed, and type:

 &quot;aclhound init&quot;

This little setup part of ACLHound asks you 3 questions: username, location and wether or 
not you'd like to clone the repository data (configured in the aclhound.conf)

## <span style="line-height: 1.5;">Jenkins integration</span>

The two minimum used cases to implement in Jenkins are &quot;Syntax Validation&quot; &amp; &quot;Configuration deployment&quot;
<table class="confluenceTable"><tbody><tr><th class="confluenceTh">Syntax Validation</th><th class="confluenceTh">Configuration deployment</th></tr><tr><td class="confluenceTd">

*   Make a new &quot;freestyle project&quot;

        *   <span style="line-height: 1.4285715;">Give it a name (example: validate_aclhound_patchset)</span>
    *   <span style="line-height: 1.4285715;">at &quot;Source Code Management&quot; click &quot;Git&quot;</span>

            *   <span style="line-height: 1.4285715;">Type in the URL: </span>[ssh://gerrit@gerrit.ecg.so:29418/ecg-networking](ssh://gerrit@gerrit.ecg.so:29418/ecg-networking)
        *   <span style="line-height: 1.4285715;">Pick offcourse the proper credentials </span>
        *   <span style="line-height: 1.4285715;">At &quot;Additional Behaviours&quot;, choose &quot;Gerrit Trigger&quot; as a Strategy (drop down)</span><span style="line-height: 1.4285715;">
</span>
    *   <span style="line-height: 1.4285715;">Move on to build triggers, and click &quot;Gerrit event&quot;</span>

            *   <span style="line-height: 1.4285715;">configure the proper server</span>
        *   <span style="line-height: 1.4285715;">Create 2 triggers: &quot;patchset created&quot; and &quot;draft published&quot;</span>
    *   <span style="line-height: 1.4285715;">Move on to &quot;Build&quot;, and click on &quot;execute shell&quot;</span>

            *   <span style="line-height: 1.4285715;">Insert this:</span>

                    *   pwd
            *   <span style="line-height: 1.4285715;">ls</span>
            *   <span style="line-height: 1.4285715;">echo &quot;a test build is now performed for all ACLs....&quot;</span>
            *   <span style="line-height: 1.4285715;">sleep 2</span>
            *   <span style="line-height: 1.4285715;">aclhound build all </span>
    *   <span style="line-height: 1.4285715;">Move on to &quot;Post-build actions&quot;, and configure it to send an email with the results</span></td><td class="confluenceTd">

*   Make a new &quot;freestyle project&quot;

        *   <span style="line-height: 1.4285715;">Give it a name (example: push_configs_to_network)</span>
    *   <span style="line-height: 1.4285715;">at &quot;Source Code Management&quot; click &quot;Git&quot;</span>

            *   <span style="line-height: 1.4285715;">Type in the URL: </span>[ssh://gerrit@gerrit.ecg.so:29418/ecg-networking](ssh://gerrit@gerrit.ecg.so:29418/ecg-networking)
        *   <span style="line-height: 1.4285715;">Pick offcourse the proper credentials</span>
    *   <span style="line-height: 1.4285715;">Move on to build triggers, and click &quot;Poll SCM&quot;</span>

                *   <span style="line-height: 1.4285715;">insert the following schedule to have it run every morning at 10:10 on workdays: &quot;10 10 * * 1-5&quot;</span>
    *   <span style="line-height: 1.4285715;">Move on to &quot;Build&quot;, and click on &quot;execute shell&quot;</span>

            *   <span style="line-height: 1.4285715;">Insert this:</span>

                    *   <span style="line-height: 1.4285715;">echo &quot;push config to network&quot;</span>
            *   <span style="line-height: 1.4285715;">sleep 2</span>
            *   <span style="line-height: 1.4285715;">aclhound deploy all</span>
    *   <span style="line-height: 1.4285715;">Move on to &quot;post build&quot;, and configure it to send an email with the results</span>

</td></tr></tbody></table>

<div>

<span style="color: rgb(0,0,0);font-size: 20.0px;line-height: 1.5;">ACL hound commands</span>
<pre> </pre><pre>- init Initialise aclhound end-user configuration.

 Initialise user-specific settings, ask the user for username on 
 repository server, location to store aclhound policy, ask to make
 initial clone.</pre><pre>Usage: aclhound [-d] init [--batch]</pre><pre>Options:
 --batch Automatically guess all settings (non-interactive mode).

 - fetch Retrieve latest ACLHound policy from repository server.</pre><pre>- task Manage change proposals (creation, submission, etc)</pre><pre>Start, continue or submit a piece of work for review.</pre><pre>Usage: aclhound [-d] task list
 aclhound [-d] task submit
 aclhound [-d] task start &lt;taskname&gt;
 aclhound [-d] task edit &lt;taskname&gt;
 aclhound [-d] task status
 aclhound [-d] task clean</pre><pre>Arguments:
 list List locally stored branches
 submit Submit current task for review
 start Create a new branch to work on a task
 edit Continue working on a task/branch
 status Show current task information
 clean Clean up old tasks (which have been merged)</pre><pre>&lt;taskname&gt;
 Taskname refers to for example a JIRA ticket, or other reference by
 which the change will be known in the review system.</pre><pre> </pre><pre>- diff Compare current working directory with the previous version.</pre><pre>Show unified diff between last commit and current state.</pre><pre>Usage: aclhound diff &lt;filename&gt;
 aclhound diff all</pre><pre>Arguments:
 &lt;filename&gt;
 The policy or device file for which a unified diff must be
 generated.</pre><pre>Note: please ensure you run 'diff' inside your ACLHound data directory</pre><pre>- build Compile policy into network configuration, output on STDOUT

Show unified build between last commit and current state.</pre><pre>Usage: aclhound build &lt;devicename&gt;
 aclhound build all</pre><pre>Arguments:
 &lt;devicename&gt;
 The device file for which a network config must be generated.</pre><pre>&lt;all&gt;
 Build all network policies into their respective vendor specific
 representation. Useful as 'review' test in Jenkins.</pre><pre>Note: please ensure you run 'build' inside your ACLHound data directory 

 - deploy Deploy compiled configuration to a network device

 Deploy a compiled version of the ACLs on a network device</pre><pre>Usage: aclhound deploy &lt;devicename&gt;
 aclhound deploy all</pre><pre>Arguments:
 &lt;devicename&gt;
 Hostname of the device on which the generated ACLs must be
 deployed.</pre><pre>&lt;all&gt;
 ACLHound will take all device files from devices/ (except
 filenames with a '.ignore' suffix), compile the policy and
 upload the policies to the device. &quot;all&quot; is suitable for cron or
 jenkins.</pre><pre>Note: please ensure you run 'deploy' inside your ACLHound data directory

 - reset Delete aclhound directory and fetch copy from repository.</pre></div>

&nbsp;

    </body>
</html>
