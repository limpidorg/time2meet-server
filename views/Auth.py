from Global import API
import core.auth
import core.user
import security.desensitizer
import json
from RequestMap.Exceptions import ValidationError


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

    return makeResponse(0, f'The token has been generated which expires in {str(maxAge)} seconds. Please persist the token for future use.', token=token, user=userInfo, userId=userId, scopes=scopes)
