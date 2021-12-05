from RequestMap.EndpointMap import Map
from RequestMap.Protocols.Flask import HTTPViaFlask
from RequestMap.Response.JSON import JSONStandardizer

API = Map()

FlaskProtocol = HTTPViaFlask()
API.useProtocol(FlaskProtocol)
API.useResponseHandler(JSONStandardizer())

app = FlaskProtocol.app
