from RequestMap.EndpointMap import Map
from RequestMap.Protocols.Flask import HTTPViaFlask
from RequestMap.Response.JSON import JSONStandardizer
from mongoengine import connect
import logging

logging.info("Initializing App...")

API = Map()

logging.info("Initialising RequestMap...")

FlaskProtocol = HTTPViaFlask()
API.useProtocol(FlaskProtocol)
API.useResponseHandler(JSONStandardizer())

app = FlaskProtocol.app

logging.info("RequestMap initialised. Connecting to db...")

try:
    connect('time2meet')
except Exception as e:
    logging.fatal("Could not connect to db: " + str(e))
    raise


logging.info("db connected.")
logging.info("App initialised.")