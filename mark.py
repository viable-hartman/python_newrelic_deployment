#!/usr/bin/env python

import urllib
import urllib2
from functools import wraps


def markDeployment(target, apikey, appid, changelog, desc, revision, user):
    request_data = {
        'deployment[application_id]': appid,
        'deployment[changelog]': changelog,
        'deployment[description]': desc,
        'deployment[revision]': revision,
        'deployment[user]': user,
    }
    try:
        request = urllib2.Request(
            target,
            data=urllib.urlencode(request_data),
            headers={
                "x-api-key": apikey,
            })
        return urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        return 'Error reporting: %s\n%s\n%s' % (e.code, e.headers, e.fp.read())


def markDeploymentWrap(target, apikey, appid, changelog, desc, revision, user):
    def closuref(func):
        def innerclosuref(*args, **kwargs):
            deployres = func(*args, **kwargs)
            deployres['markresp'] = "UNKNOWN"
            if not('status' in deployres) or (('status' in deployres) and not("error" in deployres['status'].lower())):
                deployres['markresp'] = markDeployment(target, apikey, appid, changelog, desc, revision, user)
            return deployres
        return wraps(func)(innerclosuref)
    return closuref
