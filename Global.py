from RequestMap.EndpointMap import Map
from RequestMap.Protocols.Flask import HTTPRequestByEndpointIdentifier, HTTPViaFlask, HTTPBatchRequestViaFlask
from RequestMap.Response.JSON import JSONStandardizer
from logger import JSONStandardizerWithLogs
from security.Validators import AuthenticationValidator, PlannerPermissionValidator
from mongoengine import connect
from flask import Flask
import logger

logger.info("Initializing App...")

API = Map()

logger.info("Initialising RequestMap...")

FlaskApp = Flask(__name__)
FlaskProtocolInstance = HTTPViaFlask(FlaskApp)
FlaskBatchProtocolInstance = HTTPBatchRequestViaFlask(FlaskApp, route="/batch")
HTTPRequestByEndpointIdentifierInstance = HTTPRequestByEndpointIdentifier(FlaskApp, route='/science')
API.useProtocol(FlaskProtocolInstance)
API.useProtocol(FlaskBatchProtocolInstance)
API.useProtocol(HTTPRequestByEndpointIdentifierInstance)

JSONStandardizerInstance = JSONStandardizerWithLogs(standardMessages={ # Using a modified version of the JSONStandardizer that logs exceptions
    0: "Success",
    -1: "Could not complete the request.",
    -100: "No authentication method is available",
    -101: "The token is invalid",
    -102: "Either the email is invalid or it's already used by another account.",
    -103: "The password is invalid",
    -104: "Access is denied. An elevated permission is required.",
    -105: "Access is denied.",
    -106: "The user's email address had already been verified.",
    -107: "Invalid OTP. The code might have expired, or the current OTP's permission does not match its intended purpose. Please try again.",
    -200: "User does not exist",
    -300: "Planner does not exist"
})

API.useResponseHandler(JSONStandardizerInstance)

# The validator is not ready to go; it will always return True.
# For more information about this validator, go to security > Validators
#
# Brief explanation of how it works:
# - The validator (AuthenticationValidator()) will read the metadata of the endpoint and return the corresponding evaluationFunction.
# - RequestMap will then inspect the evaluationFunction and get its required and optional parameters.
# - RequestMap will try and fetch above values from the request data; If those values are missing, then the request will be rejected and a MissingParameter() exception will be raised.
# - The evaluationFunction will then be called. If there's no exception, then RequestMap assumes that the request is valid. (and if there is any errors, say the user's token is invalid, then a ValidationError() exception should be raised)

API.useValidator(logger.Log()) # Not a validator. Just a logger.
API.useValidator(AuthenticationValidator())
API.useValidator(PlannerPermissionValidator())

app = FlaskProtocolInstance.app

logger.info("RequestMap initialised. Connecting to db...")

import json
try:
    with open("secrets.json", "r") as f:
        secrets = json.load(f)
        assert 'dbURL' in secrets
        connect(host=secrets['dbURL'])
except Exception as e:
    logger.fatal("Could not connect to db: " + str(e))
    raise


logger.info("db connected.")
logger.info("App initialised.")
