from Global import API

import secrets

@API.endpoint('user-login', {
    'httpmethods': ['GET'],
    'httproute': '/login'
})
def login(username, password, makeResponse):
    # Stub
    token = secrets.token_hex(16)
    return makeResponse(0, 'Login was successful', token=token, username=username)
