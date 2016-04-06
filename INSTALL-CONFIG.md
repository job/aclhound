### How to install the package

Please don't read this how to use aclhound on a daily basis, this is just for configuration and installation.

To install the package, execute the following lines on the commandline:
<pre>
git clone https://github.com/job/aclhound.git
cd aclhound
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
make test
python setup.py install
</pre>

### **Configuration files**

**aclhound.conf**

 This can be found in the /etc/aclhound/ directory.

 This configuration file is used to configure some base settings for aclhound itself, and
 it contains settings to talke with jenkins &amp; gerrit.

 The following is an example configuration file:
<pre>
 ; ACLHound system-wide configuration
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
repository = networking
protocol = ssh
[user]
username =
location =
</pre>


**~/aclhound/.gitreview**

 This file is populated during the first/initialization run (see next chapter) of aclhound
 It contains the parameters to connect to gerrit

 Example config:
<pre> 
[gerrit]
host=gerrit.remotehost
port=29418
project=aclhound-repos.git
</pre>


**.netrc**

 This file needs to be manually edited. This contains login information to do deployments
 from the commandline using the aclhound tool (automatic logins)
 Documentation on .netrc can be found here:
 [http://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-File.html](http://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-File.html)


## **First run**

To deploy a clean working directory for ACLHound, login as a normal user on a system which
has the ACLHound software installed, and type:

 &quot;aclhound init&quot;

This little setup part of ACLHound asks you 3 questions: username, location and wether or
not you'd like to clone the repository data (configured in the aclhound.conf)

## **Jenkins integration**
<table><tbody><tr><th><h2>Syntax Validation</h2></th><th><h2>Configuration deployment</h2></th></tr><tr><td valign='top'><ul><li>Make a new &quot;freestyle project&quot;<ul><li><span>Give it a name (example: validate_aclhound_patchset)</span></li><li><span>at &quot;Source Code Management&quot; click &quot;Git&quot;</span><br /><ul><li><span>Type in the URL: </span><a href="ssh://gerrit@gerrit.remotehost:29418/networking" >ssh://gerrit@gerrit.remotehost:29418/networking</a></li><li><span>Pick offcourse the proper credentials </span></li><li><span>At &quot;Additional Behaviours&quot;, choose &quot;Gerrit Trigger&quot; as a Strategy (drop down)</span><span><br /></span></li></ul></li><li><span>Move on to build triggers, and click &quot;Gerrit event&quot;</span><br /><ul><li><span >configure the proper server</span></li><li><span>Create 2 triggers: &quot;patchset created&quot; and &quot;draft published&quot;</span></li></ul></li><li><span>Move on to &quot;Build&quot;, and click on &quot;execute shell&quot;</span><br /><ul><li><span >Insert this:</span><br /><ul><li>pwd</li><li><span>ls</span></li><li><span>echo &quot;a test build is now performed for all ACLs....&quot;</span></li><li><span>sleep 2</span></li><li><span >aclhound build all </span></li></ul></li></ul></li><li><span>Move on to &quot;Post-build actions&quot;, and configure it to send an email with the results</span></li></ul></li></ul></td><td valign='top' ><ul><li>Make a new &quot;freestyle project&quot;<ul><li><span>Give it a name (example: push_configs_to_network)</span></li><li><span>at &quot;Source Code Management&quot; click &quot;Git&quot;</span><br /><ul><li><span>Type in the URL: </span><a href="ssh://gerrit@gerrit.remotehost:29418/networking">ssh://gerrit@gerrit.remotehost:29418/networking</a></li><li><span>Pick offcourse the proper credentials</span></li></ul></li><li><span>Move on to build triggers, and click &quot;Poll SCM&quot;</span><ul><li><span>insert the following schedule to have it run every morning at 10:10 on workdays: &quot;10 10 * * 1-5&quot;</span></li></ul></li><li><span>Move on to &quot;Build&quot;, and click on &quot;execute shell&quot;</span><br /><ul><li><span>Insert this:</span><br /><ul><li><span>echo &quot;push config to network&quot;</span></li><li><span>sleep 2</span></li><li><span>aclhound deploy all</span></li></ul></li></ul></li><li><span>Move on to &quot;post build&quot;, and configure it to send an email with the results</span></li></ul></li></ul><p> </p></td></tr></tbody></table>



## **ACL hound commands**
<pre>
- init Initialise aclhound end-user configuration.
 
 Initialise user-specific settings, ask the user for username on 
 repository server, location to store aclhound policy, ask to make
 initial clone.
Usage: aclhound [-d] init [--batch]
Options:
 --batch Automatically guess all settings (non-interactive mode).
 
 
- fetch Retrieve latest ACLHound policy from repository server.

- build Compile policy into network configuration, output on STDOUT
 
Show unified build for both IPv4 and IPv6 for a device.
Usage: aclhound build <devicename>
 aclhound build all
Arguments:
 <devicename>
 The device file for which a network config must be generated.
<all>
 Build all network policies into their respective vendor specific
 representation. Useful as 'review' test in Jenkins.
Note: please ensure you run 'build' inside your ACLHound data directory 
 
 
 - deploy Deploy compiled configuration to a network device
 
 Deploy a compiled version of the ACLs on a network device
Usage: aclhound deploy <devicename>
 aclhound deploy all
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
 
 - reset Delete aclhound directory and fetch copy from repository.

</pre>


