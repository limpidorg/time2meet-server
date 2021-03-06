from Global import API
import core.planner
import core.auth
import time
import json
import security.desensitizer


@API.endpoint('create-planner', {
    'httpmethods': ['POST'],
    'httproute': '/planner',
    'authlevel': 'verify-token'
}, notBefore=float, notAfter=float, permissions=json.loads)
def newPlanner(makeResponse, plannerName, userId, notBefore=None, notAfter=None, permissions=[]):
    if not isinstance(permissions, list):
        return makeResponse(-1, 'Permissions must be a JSON list')

    if not notBefore:
        notBefore = time.time()
    if not notAfter:
        notAfter = time.time() + 3600*24*7
    plannerId = core.planner.newPlanner(
        plannerName=plannerName, notBefore=notBefore, notAfter=notAfter, createdBy=userId)
    return makeResponse(0, plannerId=plannerId)


@API.endpoint('get-planner', {
    'httpmethods': ['GET'],
    'httproute': '/planner',
    'authlevel': 'verify-token',
    'plannerpermission': 'read'
})
def getPlanner(makeResponse, plannerId):
    plannerObj = core.planner.getPlanner(plannerId)
    if plannerObj:
        plannerObj = security.desensitizer.desensitizePlanner(
            json.loads(plannerObj.to_json()))
        return makeResponse(0, planner=plannerObj)
    return makeResponse(-1, message='Planner not found')


@API.endpoint('edit-planner', {
    'httpmethods': ['PATCH'],
    'httproute': '/planner',
    'authlevel': 'verify-token',
    'plannerpermission': 'write'
}, properties=json.loads)
def editPlanner(makeResponse, plannerId, properties):
    result = core.planner.editPlanner(plannerId, properties)
    if result:
        updatedPlanner = core.planner.getPlanner(plannerId)
        return makeResponse(0, message='Planner updated', planner=security.desensitizer.desensitizePlanner(json.loads(updatedPlanner.to_json())))
    return makeResponse(-1, message='Could not update')


@API.endpoint('delete-planner', {
    'httpmethods': ['DELETE'],
    'httproute': '/planner',
    'authlevel': 'verify-token',
    'plannerpermission': 'delete'
})
def deletePlanner(makeResponse, plannerId):
    result = core.planner.deletePlanner(plannerId)
    if result:
        return makeResponse(0, message='Planner deleted')
    return makeResponse(-1, message='Could not delete')


@API.endpoint('update-user-planner-permissions', {
    'httpmethods': ['PATCH', 'POST'],
    'httproute': '/user-permissions',
    'authlevel': 'verify-token',
    'plannerpermission': 'write'
}, permissions=json.loads)
def updateUserPermissions(makeResponse, userId, plannerId, permissions, targetUserId=None):
    if not targetUserId:
        targetUserId = userId
    if not isinstance(permissions, list):
        return makeResponse(-1, message='Permissions must be a JSON list represented in string')
    result = core.auth.updateUserPlannerPermissions(
        userId=targetUserId, plannerId=plannerId, permissions=permissions)
    if result:
        return makeResponse(0, message='Permissions updated', permissions=permissions)
    return makeResponse(-1, message='Failed to update permissions.')


@API.endpoint('list-user-planners', {
    'httpmethods': ['GET'],
    'httproute': '/planners',
    'authlevel': 'verify-token'
})
def listUserPlanners(makeResponse, userId, targetUserId=None):
    if not targetUserId:
        targetUserId = userId
    plannerIds = core.planner.listUserPlannerIds(userId)
    return makeResponse(0, plannerIds=plannerIds)
