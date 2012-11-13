'''
This module encapsulates the functionality for interacting with RMAS bus

@author: jasonmarshall
'''

from suds.client import Client
from rmas_oe_adapter import settings
def get_events(timestamp):
    '''
        Returns all the events that have occured since the timestamp
    '''
    
    client = Client(settings.RMAS_BUS_WSDL, cache=None)
    return client.service.getEvents(timestamp)
    
def push_event(event):
    '''
        Pushes the event to the RMAS bus.
    '''
    client = Client(settings.RMAS_BUS_WSDL, cache=None)
    return client.service.pushEvent(event)
