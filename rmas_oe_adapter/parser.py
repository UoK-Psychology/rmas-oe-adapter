'''

'''

from lxml import etree
import logging
import os
from rmas_adapter.conf import settings


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
