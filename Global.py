from RequestMap.EndpointMap import Map
from RequestMap.Protocols.Flask import HTTPViaFlask
from RequestMap.Response.JSON import JSONStandardizer
from security.Validators import AuthenticationValidator
from mongoengine import connect
import logging

logging.info("Initializing App...")

API = Map()

logging.info("Initialising RequestMap...")

FlaskProtocolInstance = HTTPViaFlask()
JSONStandardizerInstance = JSONStandardizer(standardMessages={
    0: "Success",
    -1: "Could not complete the request.",
    -100: "No authentication method is available",
    -101: "The token is invalid",
    -102: "Either the email is invalid or it's already used by another account.",
    -200: "User does not exist",
})

API.useProtocol(FlaskProtocolInstance)
API.useResponseHandler(JSONStandardizerInstance)

# Not using the validator just yet as it is not ready.
# This means that no authentication will be required for any endpoint.
# API.useValidator(AuthenticationValidator())

app = FlaskProtocolInstance.app

logging.info("RequestMap initialised. Connecting to db...")

try:
    connect('time2meet')
except Exception as e:
    logging.fatal("Could not connect to db: " + str(e))
    raise


logging.info("db connected.")
logging.info("App initialised.")
