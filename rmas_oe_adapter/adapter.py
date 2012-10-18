'''
Created on Oct 17, 2012

@author: jasonmarshall
'''
import logging
from rmas_oe_adapter.parser import parse_event, parse_proposal_payload
from rmas_oe_adapter.mapping import get_ethics_user, persist_proposal_ethics_application_link
from rmas_oe_adapter.api import create_ethics_application

def handle_proposal_created(payload):
    logging.info('handling proposal created message!')
    #if so retrieve the key information from the cerif payload:
    
    proposal_details = parse_proposal_payload(payload)
    
    ethics_user = get_ethics_user(proposal_details['principle_investigator_id'])
    
    if ethics_user:
        application_id = create_ethics_application(proposal_details['project_title'], ethics_user)
        persist_proposal_ethics_application_link(proposal_details['proposal_id'], application_id)
    
def handle_event(event):
    '''
    
        Handles the the received RMAs event.
        
        Currently it only handles proposal-created events.
        
        @param event the raw string of the rmas event
    '''
    logging.info('handling event: %s' % event)
    
    event_type, payload = parse_event(event)
    
    
    if event_type.lower() == 'proposal-created':
        handle_proposal_created(payload)
        