'''
    This module handles the polling of the RMAS ESB, passing any messages that are received from
    it to the adapter module for processing.

'''


from threading import Timer

import datetime
import logging
from rmas_oe_adapter.adapter import handle_event
import lifecycle_consumer
from rmas_oe_adapter.rmas_bus import get_events


last_poll = None


def poll_for_events():
    logging.info('Polling ESB')
    
    global last_poll
    events = get_events(last_poll.isoformat())
    
    if hasattr(events, 'string'):
        for event in events.string:
            handle_event(event)
        
        
    #update the last_poll time - we only want new events after this time.
    last_poll = datetime.datetime.now()
    Timer(5, poll_for_events).start()#poll again in 2 seconds time!

if __name__=='__main__':
    
    logging.basicConfig(level=logging.INFO)
    last_poll = datetime.datetime.now()
    lifecycle_consumer.connect()#connect to the message queue to start consuming AMQP messages
    poll_for_events()
