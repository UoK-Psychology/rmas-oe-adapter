'''
Created on Oct 17, 2012

@author: jasonmarshall
'''
import logging

def handle_event(event):
    '''
        @param event the raw string of the rmas event
    '''
    
    logging.info('handling event: %s' % event)