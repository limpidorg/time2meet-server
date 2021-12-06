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
def getUser(userId, makeResponse):
    user = core.user.getUser(userId)
    if user:
        userDict = security.desensitizer.desensitizeUser(
            json.loads(user.to_json()))
        return makeResponse(0, user=userDict)
    return makeResponse(-200)
