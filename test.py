#!/usr/bin/env python

# Production Imports
import sys
sys.path.append('/usr/lib/yum-plugins')
from mark import markDeploymentWrap
# Imports for testing only
import json
import random
# import inspect


@markDeploymentWrap("https://rpm.newrelic.com/deployments.xml", "<YOUR API KEY>", "<YOUR APP ID>", "<LOG STRING>", "<DEPLOY MESSAGE>", "<REVISION>", "<USERNAME>")
def testMarkDeployment(somearg):
    print("Performing some action and randomly selecting success or failure")
    results = [{'status': 'Error: Failure in action foo', 'data': somearg},
               {'status': 'Success: Action find planet-X succeeded', 'data': somearg},
               {'nostatus': 'Test with no status at all, perhaps an exception', 'data': somearg}]
    return random.choice(results)


if __name__ == "__main__":
    resp = testMarkDeployment('Python Rules')
    # print(inspect.getmembers(resp['markresp'], predicate=inspect.ismethod))
    print(json.dumps(resp))
