'''
This module provides the functionality to mediate the interaction between the RMAS ESB and the 
OpenEthics API, it handles messages recieved by the ESB, and depending on the message type, 
interacts with the OpenEthics API appropriatley.

@author: jasonmarshall
'''
import logging
from rmas_oe_adapter.parser import parse_event, parse_proposal_payload
from rmas_oe_adapter.mapping import persist_proposal_ethics_application_link,\
    get_ethics_user
from rmas_oe_adapter.api import get_user, create_application


def handle_proposal_created(payload):
    '''
        This function handles the proposal created event. It will parse the payload
        to get the information that it needs to then create an OpenEthics application via the 
        OpenEthics API
    
    '''
    logging.info('handling proposal created message!')
    #if so retrieve the key information from the cerif payload:
    
    proposal_details = parse_proposal_payload(payload)
    
    application_uri = create_application(title=proposal_details['project_title'],
                                                    principle_investigator_resource=get_user(get_ethics_user(proposal_details['principle_investigator_id'])) )
    if application_uri != None:
        persist_proposal_ethics_application_link(proposal_details['proposal_id'], application_uri)
    
def handle_event(event):
    '''
    
        Handles the received RMAS event.
        
        Currently it only handles proposal-created events but in future this would fork out to different
        event based handler functions
        
        @param event the raw string of the rmas event
    '''
    logging.info('handling event: %s' % event)
    
    event_type, payload = parse_event(event)
    
    
    if event_type.lower() == 'proposal-created':
        handle_proposal_created(payload)
