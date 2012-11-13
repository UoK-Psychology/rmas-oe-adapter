'''
This module handles the parsing of RMAS messages. It knows how to parse the message/event type
and depending on the type of message, it knows how to parse its payload.

This is the most changeable module in the package as the specification for these messages has
yet to be defined.

@author: jasonmarshall
'''

from lxml import etree
import logging
import os
import settings

def _process_single_element_xpath(root, xpath_expression, namespaces={'p':'urn:xmlns:org:eurocris:cerif-1.4-0'}):
    '''
        This function should be used to process an xpath that you believe will only
        return one element (or you only want the first element of those returned)
    '''
    
    expression_result = root.xpath(xpath_expression, namespaces=namespaces)
    
    result = None
    if len(expression_result) > 0:
        result = expression_result.pop() 
    
    return result
    
def parse_event(event):
    '''
        Parses the event and returns a tuple, the first element being the
        event type, and the second element being the cerif payload of the message
    '''
    
    parser = etree.XMLParser(remove_comments=True)
    event_root = etree.fromstring(str(event), parser=parser)
    
    event_type = event_root.xpath('/rmas/message-type').pop().text
    payload = _process_single_element_xpath(event_root, '/rmas/message-type')
    
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



def create_ethics_approved_event(rmas_id, start='', end='', template=os.path.abspath(os.path.join(settings.TEMPLATE_DIR,'ethics_approved.xml'))):
    '''
        This will create the RMAS-CERIF event message to tell the bus that an ethics application has been
        approved.
    '''
    
    with open(template) as template_file:
        event_message=template_file.read() % {'rmas_id':rmas_id, 'start':start, 'end':end}
    
    
    return event_message
