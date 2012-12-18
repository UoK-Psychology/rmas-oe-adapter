'''
    This is the main settings module for your adapter.
    It will be imported and available to your adapter package:::
    
        from rmas_adapter.conf import settings
        poll_interval = settings.POLL_INTERVAL
        
    You will need to have some code somehwere (usually in your runner.py) that sets
    the location of this settings module, as you won't use this module directly, instead
    it is imported into the rmas_adapter.conf.settings module.::
        
        os.environ.setdefault("RMAS_ADAPTER_SETTINGS", "rmas_oe_adapter.settings")
    
    This is so that your settings are all in the same predicatable location (as there are settings that the RMAS Adapter 
    framework rely on). This pattern is borrowed from the way that Django manages its settings.
    
    There are a couple of required settings:
    
    * **RMAS_BUS_WSDL** : This is the url for the RMAS bus (specifically the wsdl file for this soap service)
    * **POLL_INTERVAL** : This is the duration in milliseconds that the adapter will pause between polling the bus for messages
    * **EVENTS**: This is a list of tuples describing the RMAS Events to listen for and the event handling that
    
    should be called when this event of one of these events occuring.
    
    The tuple should look like:::
    
        ('name of rmas event', 'location to the handler module')
    
    The rest of the settings in this module are specific to the RMAS-to-Openethics adapter

'''

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