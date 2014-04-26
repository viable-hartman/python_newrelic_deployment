python_newrelic_deployment
==========================

A simple YUM plugin that allows you to automatically report package installs, updates, or deletes as deployment markers in your NewRelic application graphs.

You can also simply import the mark.py script by itself to allow you to add random event/deployment markers to NewRelic from other Python projects.  


Usage of mark.py by itself
--------------------------
mark.py was created to allow deployment markers in 2 different ways:

* Method 1 calls markDeployment directly
```
import sys
sys.path.append('/usr/lib/yum-plugins')
from mark import markDeployment

markDeployment('https://rpm.newrelic.com/deployments.xml',
               '<YOUR API KEY>', '<YOUR APP ID>', '<CHANGELOG>', '<DESCRIPTION>', '<REVISION>', '<USER>')
```

* Method 2 uses a decorator

```
import sys
sys.path.append('/usr/lib/yum-plugins')
from mark import markDeploymentWrap

@markDeploymentWrap("https://rpm.newrelic.com/deployments.xml",
                    '<YOUR API KEY>', '<YOUR APP ID>', '<CHANGELOG>', '<DESCRIPTION>', '<REVISION>', '<USER>')
def testMarkDeployment(somearg):
    # Decorated code here
```

Usage as a YUM plugin
---------------------
1. Make sure plugins are enabled in YUM by setting plugins=1 in /etc/yum.conf
2. Copy the files in usr/lib/yum-plugins/ of this repository to /usr/lib/yum-plugins/ on your YUM based system.
3. Copy etc/yum/pluginconf.d/newrelic.conf to /etc/yum/pluginconf.d/newrelic.conf and modify the parameters inside as desired.

