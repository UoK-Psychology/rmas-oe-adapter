'''
This module handles the parsing of RMAS messages. It knows how to parse the message/event type
and depending on the type of message, it knows how to parse its payload.

This is the most changeable module in the package as the specification for these messages has
yet to be defined.

@author: jasonmarshall
'''

from lxml import etree
import logging

def parse_event(event):
    '''
        Parses the event and returns a tuple, the first element being the
        event type, and the second element being the cerif payload of the message
    '''
    
    parser = etree.XMLParser(remove_comments=True)
    event_root = etree.fromstring(str(event), parser=parser)
    
    event_type = event_root.xpath('/rmas/message-type').pop().text
    payload = event_root.xpath('/rmas/p:CERIF', 
                               namespaces={'p':'urn:xmlns:org:eurocris:cerif-1.4-0'}).pop()
    
    return (event_type, payload)


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