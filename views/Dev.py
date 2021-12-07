from Global import API


@API.endpoint("example-addition", {  # Endpoint Identifier
    'httpmethods': ['GET'],  # Metadata for the Flask protocol handler
    'httproute': '/addition',
    'authlevel': 'verify-password'
}, a=float, b=float, c=float)  # Type conversion functions for parameters
def example(a, b, makeResponse, c=0):
    # Both a and b are neccessary but c is optional - it has a default value of 0.
    #
    # makeResponse is a special function passed from the RequestMap that
    # parses the response according to the responseHandler (RequestMap.Response).
    # The order of makeResponse does not matter.
    #
    # In this app, we are using RequestMap.Response.JSON.JSONStandardizer (see Global.py)
    return makeResponse(0, result=a + b + c)
