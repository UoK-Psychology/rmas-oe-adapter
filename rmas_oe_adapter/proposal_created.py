import logging
from rmas_oe_adapter.parser import parse_proposal_payload
from rmas_oe_adapter.api import create_application, get_user
from rmas_oe_adapter.mapping import persist_proposal_ethics_application_link,\
    get_ethics_user


def handle_event(payload):
    logging.info('handling proposal created message!')
    #if so retrieve the key information from the cerif payload:
    
    proposal_details = parse_proposal_payload(payload)
    
    application_uri = create_application(title=proposal_details['project_title'],
                                                    principle_investigator_resource=get_user(get_ethics_user(proposal_details['principle_investigator_id'])) )
    if application_uri != None:
        persist_proposal_ethics_application_link(proposal_details['proposal_id'], application_uri)
    