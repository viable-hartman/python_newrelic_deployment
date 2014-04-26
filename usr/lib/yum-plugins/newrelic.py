#! /usr/bin/python -tt

from yum.plugins import TYPE_CORE
from yum.constants import *
from yum.packages import parsePackages

import sys
sys.path.append('/usr/lib/yum-plugins')
from mark import markDeployment
import socket
# import json
import logging

requires_api_version = '2.6'
plugin_type = (TYPE_CORE,)
__package_name__ = "newrelic"


def posttrans_hook(conduit):
    logger = logging.getLogger("yum.verbose.main")
    ts = conduit.getTsInfo()

    removes = ts.getMembersWithState(output_states=TS_REMOVE_STATES)
    updates = ts.getMembersWithState(output_states=[TS_INSTALL_STATES, TS_UPDATE, TS_OBSOLETING])

    statusstr = ""
    if updates:
        statusstr = "MODIFIED: "
        for txmbr in updates:
            statusstr = "%s%s-%s-%s " % (statusstr, txmbr.po.name, txmbr.version, txmbr.release)

    if removes:
        statusstr = "%sREMOVED: " % (statusstr)
        for txmbr in removes:
            statusstr = "%s%s-%s-%s " % (statusstr, txmbr.po.name, txmbr.version, txmbr.release)

    if statusstr:
        nrurl = conduit.confString('main', 'nrurl', 'https://rpm.newrelic.com/deployments.xml')
        apikey = conduit.confString('main', 'apikey')
        appid = conduit.confString('main', 'appid')
        hostname = conduit.confString('main', 'hostname', socket.gethostname())
        statusstr = "%s %s" % (hostname, statusstr)
        user = conduit.confString('main', 'user', 'Packager')
        result = markDeployment(nrurl, apikey, appid, statusstr, "Package Update %s" % (hostname), "", user)
    if result['code'] != 201:
        logger.warn("FAILED to mark deployment in NewRelic")
        # f = open('/tmp/newrelic.log', 'w')
        # f.write(json.dumps(result, indent=4))
        # f.close()


if __name__ == '__main__':
    print "This is a plugin that is supposed to run from inside YUM"
