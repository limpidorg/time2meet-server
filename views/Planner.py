from Global import API
import core.planner
import time
import json


@API.endpoint('new-planner', {
    'httpmethods': ['POST'],
    'httproute': '/planner',
}, )
def newPlanner(makeResponse, plannerName, notBefore=None, notAfter=None):
    if not notBefore:
        notBefore = time.time()
    if not notAfter:
        notAfter = time.time() + 3600*24*7
    plannerId = core.planner.newPlanner(
        plannerName=plannerName, notBefore=notBefore, notAfter=notAfter)
    return makeResponse(0, plannerId=plannerId)


@API.endpoint('get-planner', {
    'httpmethods': ['GET'],
    'httproute': '/planner',
})
def getPlanner(makeResponse, plannerId):
    plannerObj = core.planner.getPlanner(plannerId)
    if plannerObj:
        return makeResponse(0, plannerObj=json.loads(plannerObj.to_json()))
    return makeResponse(-1, message='Planner not found')


@API.endpoint('edit-planner', {
    'httpmethods': ['PATCH'],
    'httproute': '/planner'
}, properties=json.loads)
def editPlanner(makeResponse, plannerId, properties):
    result = core.planner.editPlanner(plannerId, properties)
    if result:
        updatedPlanner = core.planner.getPlanner(plannerId)
        return makeResponse(0, message='Planner updated', updatedPlanner=json.loads(updatedPlanner.to_json()))
    return makeResponse(-1, message='Could not update')

@API.endpoint('delete-planner', {
    'httpmethods': ['DELETE'],
    'httproute': '/planner'
})
def deletePlanner(makeResponse, plannerId):
    result = core.planner.deletePlanner(plannerId)
    if result:
        return makeResponse(0, message='Planner deleted')
    return makeResponse(-1, message='Could not delete')

