'''
Created on Oct 17, 2012

@author: jasonmarshall
'''
import logging
from lxml import etree
from pymongo import Connection
from pymongo.errors import PyMongoError

def parse_event(event):
    '''
        Parses the event and returns either None, if the event was not a proposal created event
        or a dictionary containing the key information from the event:
        {'project_id':'',
        'project_title':'',
        'principle_investigator_id':'',
        'principle_investigator_name':(firstnames, surname)}
    '''
    
    parser = etree.XMLParser(remove_comments=True)
    event_root = etree.fromstring(str(event), parser=parser)
    
    
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
        principleInvestigator=%s %s''' % (projid,projtitle,pi_first_name, pi_family_name))
        
        return {'project_id':projid,
        'project_title':projtitle,
        'principle_investigator_id':principle_investigator_person_id,
        'principle_investigator_name':(pi_first_name, pi_family_name)}
    
    return None #wasn't a proposal created event!

def create_ethics_application(title, pi):
    '''
        Uses the OpenEthics API to create a new ethics application form
        
        @return: the id of the new application, or None if there was a problem
    '''
    
    return 1

def persist_proposal_ethics_application_link(proposal_id, ethics_application_id):
    '''
        Persists a link between the proposal_id and the newly created ethics_application_id
        This will be useful if there are any updates.
    '''
    try:
        connection = Connection()
        database = connection.oe_rmas_adapter
        link_collection = database.application_links
        link = {'proposal_id':proposal_id, 'ethics_application_id':ethics_application_id}
        link_collection.insert(link)
        
        connection.close()
        logging.info('peristed link %s' % link)
        
    except PyMongoError as e:
        logging.error('An error occured trying to persist the proposal-ethics-application link: %s' % e)

def handle_event(event):
    '''
    
        Handles the the received RMAs event.
        
        in the best case scenario: A proposal-created message is received, it is then parsed and used
        to create a new ethics application using the OpenEthics API. They newly created ethics application
        id is then persisted with the proposal id to provide a link between the two entities.
        
        @param event the raw string of the rmas event
    '''
    logging.info('handling event: %s' % event)
    
    
    event_info = parse_event(event)
    
    if event_info:
        application_id = create_ethics_application(event_info['project_title'], event_info['principle_investigator_name'])
        if application_id:
            persist_proposal_ethics_application_link(event_info['project_id'], application_id)
            
        
        
        
        