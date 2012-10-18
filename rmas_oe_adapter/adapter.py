'''
Created on Oct 17, 2012

@author: jasonmarshall
'''
import logging
from lxml import etree

def handle_event(event):
    '''
        @param event the raw string of the rmas event
    '''
    logging.info('handling event: %s' % event)
    
    parser = etree.XMLParser(remove_comments=True)
    event_root = etree.fromstring(str(event), parser=parser)
    
    #check to see if the event is a proposal created event
    event_type = event_root.xpath('/rmas/message-type').pop().text
    
    if event_type.lower() == 'proposal-created':
        logging.info('Got proposal created message!')
        #if so retrieve the key information from the cerif payload:
        projid = event_root.xpath('/rmas/p:CERIF/p:cfProj/p:cfProjId/.', 
                                  namespaces={'p':'urn:xmlns:org:eurocris:cerif-1.4-0'}).pop().text
        projtitle = event_root.xpath('/rmas/p:CERIF/p:cfProj/p:cfTitle/.',
                                      namespaces={'p':'urn:xmlns:org:eurocris:cerif-1.4-0'}).pop().text
        
        principle_investigator_person_id = event_root.xpath("/rmas/p:CERIF/p:cfProj/p:cfProj_Pers[p:cfClassId='b0e11470-1cfd-11e1-8bc2-0800200c9a66']/p:cfPersId", 
                                                      namespaces={'p':'urn:xmlns:org:eurocris:cerif-1.4-0'}).pop().text
        
        principle_investigator_person_node = event_root.xpath("/rmas/p:CERIF/p:cfPers[p:cfPersId='%s']" % principle_investigator_person_id, 
                                                              namespaces={'p':'urn:xmlns:org:eurocris:cerif-1.4-0'}).pop()
        
        pi_first_name = principle_investigator_person_node.xpath('./p:cfPersName/p:cfFirstNames',
                                      namespaces={'p':'urn:xmlns:org:eurocris:cerif-1.4-0'}).pop().text
                                      
        pi_family_name = principle_investigator_person_node.xpath('./p:cfPersName/p:cfFamilyNames',
                                      namespaces={'p':'urn:xmlns:org:eurocris:cerif-1.4-0'}).pop().text
        logging.info('''Got details: 
        projectId=%s
        projectTitle=%s
        principleInvestigator=%s %s
        '''% (projid,projtitle,pi_first_name, pi_family_name))
        #call the OpenEthics API with the information retrieved from the payload
        
        #persist a link between the proposal uuid and the application id returned by the api call