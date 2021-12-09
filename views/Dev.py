from Global import API
import copy
import json


@API.endpoint("example-addition", {  # Endpoint Identifier
    'httpmethods': ['GET'],  # Metadata for the Flask protocol handler
    'httproute': '/addition',
    'authlevel': 'public'
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


@API.endpoint("endpoint-info", {
    'httpmethods': ['GET'],
    'httproute': '/dev/endpoint-info',
    'authlevel': 'public'
})
def endpointInfo(makeResponse, path=None, identifier=None):
    def JSONSafe(object):
        if isinstance(object, dict):
            current = {}
            for key, value in object.items():
                current[key] = JSONSafe(value)
            return current
        elif isinstance(object, list):
            current = []
            for value in object:
                current.append(JSONSafe(value))
            return current
        elif isinstance(object, str):
            return object
        elif isinstance(object, int):
            return object
        elif isinstance(object, float):
            return object
        elif isinstance(object, bool):
            return object
        elif object == None:
            return object
        else:
            return str(object)

    endpoints = {}
    if identifier:
        if identifier in API.endpointMap:
            endpoints[identifier] = API.endpointMap[identifier]
    if path:
        for identifier, endpoint in API.endpointMap.items():
            try:
                if endpoint['metadata']['httproute'] == path:
                    endpoints[identifier] = endpoint
            except Exception as e:
                return makeResponse(-1, f'Could not generate endpoint information for path {path}: {str(e)}')
    if not identifier and not path:
        endpoints = API.endpointMap
    if not endpoints:
        return makeResponse(-1, f'Could not find endpoint information for path {path}. Please try again or use the identifier.')

    return makeResponse(0, endpoints=JSONSafe(endpoints))
