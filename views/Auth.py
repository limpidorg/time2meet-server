from Global import API
import core.auth
import core.user
import security.desensitizer
import json
from RequestMap.Exceptions import ValidationError
import hashlib


@API.endpoint('login', {
    'httpmethods': ['POST'],
    'httproute': '/login',
    'authlevel': 'login'
}, maxAge=float, scopes=json.loads)
@API.endpoint('new-token', {
    'httpmethods': ['POST'],
    'httproute': '/token',
    'authlevel': 'login'
}, maxAge=float, scopes=json.loads)
def login(email, makeResponse, maxAge=86400 * 7, scopes=[]):
    # Note: This endpoint will only be called if the password is correct.
    # The password auth is done in the security.Validators (which uses core.auth.verifyPassword)

    # user must exist - otherwise the password auth would have failed. There is no need to check for user=None.
    if not isinstance(scopes, list):
        raise ValidationError(-1, 'scopes must be a list')

    user = core.user.getUserByEmail(email)
    userId = user.userId
    token = core.auth.generateToken(userId, maxAge, scopes=scopes)
    if not token:
        raise Exception("Token generation failed. Please try again.")

    userInfo = security.desensitizer.desensitizeUser(
        json.loads(user.to_json()))

    return makeResponse(0, f'The token has been generated which expires in {str(maxAge)} seconds. Please persist the token for future use.', token=token, user=userInfo, userId=userId, scopes=scopes, maxAge=maxAge)


@API.endpoint('logout', {
    'httpmethods': ['POST'],
    'httproute': '/logout',
    'authlevel': 'verify-token'
})
@API.endpoint('invalidate-token', {
    'httpmethods': ['DELETE'],
    'httproute': '/token',
    'authlevel': 'verify-token'
})
def logout(userId, token, makeResponse):
    if core.auth.deleteToken(userId, token):
        return makeResponse(0, 'Token has been invalidated.')
    else:
        return makeResponse(-1, 'Token could not be invalidated.')


@API.endpoint('get-token-info', {
    'httpmethods': ['GET'],
    'httproute': '/token',
    'authlevel': 'verify-token'
})
def getTokenInfo(userId, token, makeResponse):
    tokenInfo = core.auth.getToken(userId, token)
    if not tokenInfo:
        raise Exception("Impossible case!")
    else:
        return makeResponse(0, token=security.desensitizer.desensitizeTokenInfo(json.loads(tokenInfo.to_json())))


@API.endpoint('send-email-verification', {
    'httpmethods': ['GET'],
    'httproute': '/email-verification',
    'authlevel': 'verify-token'
})
def sendEmailVerification(userId, makeResponse):
    user = core.user.getUser(userId)
    if not user:
        return makeResponse(-200)
    else:
        if user.status != 'require-email-verification':
            return makeResponse(-106)
        if core.auth.sendEmailOTP(userId, 'verify-email'):
            return makeResponse(0, 'Email verification code has been sent.')
        else:
            return makeResponse(-1, 'Could not send OTP')


@API.endpoint('verify-email', {
    'httpmethods': ['POST'],
    'httproute': '/email-verification',
    'authlevel': 'verify-token'
}, otp=str)
def verifyEmail(userId, otp, makeResponse):
    otp = otp.upper()
    user = core.user.getUser(userId) # Must exist - otherwise the token auth would have failed.
    if core.auth.verifyOTP(userId, otp, permission='verify-email'):
        try:
            user.status = 'active'
            user.save()
        except Exception as e:
            return makeResponse(-1, 'Could not update user status')
        return makeResponse(0, 'Email has been verified.')
    else:
        return makeResponse(-107)

@API.endpoint('reset-password', {
    'httpmethods': ['GET'],
    'httproute': '/reset-password',
    'authlevel': 'public'
}, otp=str)
def resetPassword(userId, makeResponse):
    if core.auth.sendEmailOTP(userId, 'reset-password'):
        return makeResponse(0, 'Password reset code has been sent.')
    else:
        return makeResponse(-1, 'Could not send OTP')

@API.endpoint('verify-reset-password', {
    'httpmethods': ['POST'],
    'httproute': '/reset-password',
    'authlevel': 'public'
}, otp=str, password=str)
def verifyResetPassword(userId, otp, newPassword, makeResponse):
    if core.auth.verifyOTP(userId, otp, permission='reset-password'):
        user = core.user.getUser(userId)
        if user:
            passwordHash = hashlib.sha256(
                str(newPassword + user.salt).encode('utf-8')).hexdigest()
            if core.user.editUser(userId, properties={'password': passwordHash}, protectProperties=False):
                # Return updated user
                user = core.user.getUser(userId)
                return makeResponse(0, user=security.desensitizer.desensitizeUser(json.loads(user.to_json())))
            else:
                return makeResponse(-1)
        return makeResponse(-200)
    return makeResponse(-107)
