'''
    This module handles the polling of the RMAS ESB, passing any messages that are received from
    it to the adapter module for processing.

'''


from threading import Timer
from suds.client import Client
import datetime
import logging
from rmas_oe_adapter.adapter import handle_event


last_poll = None


def poll_for_events():
    logging.info('Polling ESB')
    
    global last_poll
    
    client = Client('http://localhost:7789/?wsdl', cache=None)
    events = client.service.getEvents(last_poll.isoformat())

    if hasattr(events, 'string'):
        for event in events.string:
            handle_event(event)
        
        
    #update the last_poll time - we only want new events after this time.
    last_poll = datetime.datetime.now()
    Timer(5, poll_for_events).start()#poll again in 2 seconds time!

if __name__=='__main__':
    
    logging.basicConfig(level=logging.INFO)
    last_poll = datetime.datetime.now()
    poll_for_events()
