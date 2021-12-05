from RequestMap.EndpointMap import Map
from RequestMap.Protocols.Flask import HTTPViaFlask
from RequestMap.Response.JSON import JSONStandardizer

API = Map()

FlaskProtocol = HTTPViaFlask()
API.useProtocol(FlaskProtocol)
API.useResponseHandler(JSONStandardizer())


@API.endpoint("webroot-post", {
    'httpmethods': ['POST'],
    'httproute': '/',
})
def webroot(makeResponse):
    return makeResponse(0, message="Helloworld from POST")

@API.endpoint("webroot-delete", {
    'httpmethods': ['DELETE'],
    'httproute': '/',
})
def webroot(makeResponse):
    return makeResponse(0, message="Helloworld from DELETE (do different stuff)")


app = FlaskProtocol.app

app.run(port=8080)