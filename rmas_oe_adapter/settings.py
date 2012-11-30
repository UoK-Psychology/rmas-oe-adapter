import os
import pika

basepath = os.path.dirname(globals()["__file__"])
dirname = os.path.abspath(os.path.join(basepath, ".."))

RMAS_BUS_WSDL='http://localhost:7789/?wsdl'
POLL_INTERVAL=5000
EVENTS=[('proposal-created', 'handlers.proposal_created'),]


TEMPLATE_DIR=os.path.abspath(os.path.join(dirname,'templates'))

OE_API_BASE_URL = 'http://127.0.0.1:8000/'
OE_API_AUTH_KEY = 'ApiKey admin:1234567890'

OE_API_USER_ENDPOINT = OE_API_BASE_URL+ 'api/v1/user/'
OE_API_APPLICATION_ENDPOINT = OE_API_BASE_URL + 'api/v1/application/'

AMQP_CONNECTION_PARAMETERS= pika.ConnectionParameters()
AMQP_EXCHANGE_NAME='openethics_events'
AMQP_EXCHANGE_TYPE='fanout'
AMQP_QUEUE_NAME='adapter'
AMQP_QUEUE_ROUTING_KEY=''