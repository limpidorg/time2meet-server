import hashlib
from Global import API
from RequestMap.Exceptions import ValidationError
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
    if 'password' in properties:
        return makeResponse(-104, 'Due to security reasons, you can only update password using the PATCH /password endpoint which requires password authentication.')

    if user:
        if core.user.editUser(userId, properties):
            # Return updated user
            user = core.user.getUser(userId)
            return makeResponse(0, user=security.desensitizer.desensitizeUser(json.loads(user.to_json())))
        else:
            return makeResponse(-1)
    return makeResponse(-200)


@API.endpoint('update-password', {
    'httpmethods': ['PATCH'],
    'httproute': '/password',
    'authlevel': 'verify-password'
}, userId=str, password=str)
def updatePassword(userId, password, makeResponse):
    user = core.user.getUser(userId)
    if user:
        passwordHash = hashlib.sha256(
            str(password + user.salt).encode('utf-8')).hexdigest()
        if core.user.editUser(userId, properties={'password': passwordHash}, protectProperties=False):
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
