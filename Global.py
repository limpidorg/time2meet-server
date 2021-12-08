from RequestMap.EndpointMap import Map
from RequestMap.Protocols.Flask import HTTPViaFlask
from RequestMap.Response.JSON import JSONStandardizer
from security.Validators import AuthenticationValidator, PlannerPermissionValidator
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
    -103: "The password is invalid",
    -104: "Access is denied. An elevated permission is required.",
    -105: "Access is denied.",
    -200: "User does not exist",
    -300: "Planner does not exist"
})

API.useProtocol(FlaskProtocolInstance)
API.useResponseHandler(JSONStandardizerInstance)

# The validator is not ready to go; it will always return True.
# For more information about this validator, go to security > Validators
#
# Brief explanation of how it works:
# - The validator (AuthenticationValidator()) will read the metadata of the endpoint and return the corresponding evaluationFunction.
# - RequestMap will then inspect the evaluationFunction and get its required and optional parameters.
# - RequestMap will try and fetch above values from the request data; If those values are missing, then the request will be rejected and a MissingParameter() exception will be raised.
# - The evaluationFunction will then be called. If there's no exception, then RequestMap assumes that the request is valid. (and if there is any errors, say the user's token is invalid, then a ValidationError() exception should be raised)

API.useValidator(AuthenticationValidator())
API.useValidator(PlannerPermissionValidator())

app = FlaskProtocolInstance.app

logging.info("RequestMap initialised. Connecting to db...")

try:
    connect('time2meet')
except Exception as e:
    logging.fatal("Could not connect to db: " + str(e))
    raise


logging.info("db connected.")
logging.info("App initialised.")
