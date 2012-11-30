import logging

from rmas_oe_adapter.api import create_application, get_user
from rmas_oe_adapter.mapping import persist_proposal_ethics_application_link,\
    get_ethics_user
from lxml import etree


def parse_proposal_payload(payload):
    '''
        Parses the cerif payload contatined within the proposal events.
        
        It will pull out the releavant details and return a dictionary:
        
        {'project_id':'',
        'project_title':'',
        'principle_investigator_id':'',
        'principle_investigator_principle_email':''}
        
    '''
    
    projid = payload.xpath('p:cfProj/p:cfProjId', 
                              namespaces={'p':'urn:xmlns:org:eurocris:cerif-1.4-0'}).pop().text
    projtitle = payload.xpath('p:cfProj/p:cfTitle',
                                  namespaces={'p':'urn:xmlns:org:eurocris:cerif-1.4-0'}).pop().text
    
    principle_investigator_person_id = payload.xpath("p:cfProj/p:cfProj_Pers[p:cfClassId='b0e11470-1cfd-11e1-8bc2-0800200c9a66']/p:cfPersId", 
                                                  namespaces={'p':'urn:xmlns:org:eurocris:cerif-1.4-0'}).pop().text
    
    
    
    proposal_details = {
                        'proposal_id':projid,
                        'project_title':projtitle,
                        'principle_investigator_id':principle_investigator_person_id,
                        }
    
    logging.info('Got details: %s' % proposal_details)
    
    return proposal_details

def handle_event(payload):
    logging.info('handling proposal created message!')
    #if so retrieve the key information from the cerif payload:
    
    proposal_details = parse_proposal_payload(payload)
    
    application_uri = create_application(title=proposal_details['project_title'],
                                                    principle_investigator_resource=get_user(get_ethics_user(proposal_details['principle_investigator_id'])) )
    if application_uri != None:
        persist_proposal_ethics_application_link(proposal_details['proposal_id'], application_uri)
    