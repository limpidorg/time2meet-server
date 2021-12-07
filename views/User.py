from Global import API
import core.user
import security.desensitizer
import json


@API.endpoint('create-user', {
    'httpmethods': ['POST'],
    'httproute': '/user',
    'authlevel': 'public'
}, timeShift=float)
def createUser(userName, email, password, makeResponse, timeShift=0):
    userId = core.user.createUser(userName, email, password, timeShift)
    if userId:
        return makeResponse(0, userId=userId)
    return makeResponse(-102)


@API.endpoint('get-user', {
    'httpmethods': ['GET'],
    'httproute': '/user',
    'authlevel': 'verify-token'
})
def getUser(userId, makeResponse, targetUserId=None):
    if targetUserId:
        desensitizeFor = 'user'
    else:
        desensitizeFor = 'owner'
        targetUserId = userId

    user = core.user.getUser(targetUserId)
    if user:
        userDict = security.desensitizer.desensitizeUser(
            json.loads(user.to_json()), desensitizeFor=desensitizeFor)
        return makeResponse(0, user=userDict)
    return makeResponse(-200)


@API.endpoint('edit-user', {
    'httpmethods': ['PATCH'],
    'httproute': '/user',
    'authlevel': 'verify-token'
}, userId=str, properties=json.loads)
def editUser(userId, properties, makeResponse):
    user = core.user.getUser(userId)
    if user:
        if core.user.editUser(userId, properties):
            # Return updated user
            user = core.user.getUser(userId)
            return makeResponse(0, user=security.desensitizer.desensitizeUser(json.loads(user.to_json())))
        else:
            return makeResponse(-1)
    return makeResponse(-200)


@API.endpoint('delete-user', {
    'httpmethods': ['DELETE'],
    'httproute': '/user',
    'authlevel': 'verify-password'
}, userId=str)
def deleteUser(userId, makeResponse):
    if core.user.getUser(userId):
        if core.user.deleteUser(userId):
            return makeResponse(0)
        return makeResponse(-1)
    return makeResponse(-200)
