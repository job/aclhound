
Please don't go beyond here for information how to use aclhound on a daily basis, this is just for configuration and installation:



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

## <span style="line-height: 1.5;">B </span>

## **First run**

## <span style="line-height: 1.5;">B </span>

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
<pre>B </pre><pre>- init Initialise aclhound end-user configuration.

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
 which the change will be known in the review system.</pre><pre>B </pre><pre>- diff Compare current working directory with the previous version.</pre><pre>Show unified diff between last commit and current state.</pre><pre>Usage: aclhound diff &lt;filename&gt;
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


