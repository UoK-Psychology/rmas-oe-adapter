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
    
    #check to see if the event is a proposal created event
    
        #if so retrieve the key information from the cerif payload:
        
        #call the OpenEthics API with the information retrieved from the payload
        
        #persist a link between the proposal uuid and the application id returned by the api call