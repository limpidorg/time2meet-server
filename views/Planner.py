from Global import API

@API.endpoint('new-planner', {
    'httpmethods':['POST'],
    'httproute':'/planner',
}, )
def newPlanner(makeResponse, notBefore = None, notAfter = None):
    core.newPlanner()
    return 