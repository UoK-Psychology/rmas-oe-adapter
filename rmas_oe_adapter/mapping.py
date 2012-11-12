'''
This module handlkes the mapping of RMAS entites to OpenEthics entities, and persists them
to a MongoDB database.

@author: jasonmarshall
'''

import logging
from pymongo import Connection
from pymongo.errors import PyMongoError

def persist_proposal_ethics_application_link(proposal_id, ethics_application_id):
    '''
        Persists a link between the proposal_id and the newly created ethics_application_id
        This will be useful if there are any updates.
        
        The persistance is carried out using a MongoDB database (oe_rmas_adapter), and the 
        'application_links' collection
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


def get_proposal_ethics_application_link(**kwargs):
    '''
        This function returns the proposal_ethics_application link, filtered by the kwargs.
        If no link is found this will return None.
        
        kwargs:
            ethics_application_id : search for the link by the ethics id
            proposal_id : search by the proposal id.
    '''
    
    try:
        connection = Connection()
        database = connection.oe_rmas_adapter
        link_collection = database.application_links
        
        link = link_collection.find_one(kwargs)
        connection.close()
        
        return link
        
    except PyMongoError as e:
        logging.error('An error occured trying to lookup the link: %s' % e)


def persist_rmas_user_ethics_user_link(rmas_user_id, ethics_user_id):
    '''
        This function persists the link between the unique identifier that is used to identify a user
        in RMAS, to the unique identifier that represents the same user in the OpenEthics system.
        
        The persistance is carried out using a MongoDB database (oe_rmas_adapter), and the 'people_links' 
        collection
    '''

def get_ethics_user(rmas_id):
    '''
        Gets the OpenEthics user id based on the rmas_id supplied. If there is no
        matching user then this function will return None.
        
        The persistance is carried out using a MongoDB database (oe_rmas_adapter), and the 'people_links' 
        collection
    '''    
    try:
        connection = Connection()
        database = connection.oe_rmas_adapter
        link_collection = database.people_links
        
        link = link_collection.find_one({'person_id':rmas_id})
        connection.close()
        
        if link:
            return link['ethics_user_id']
        
        
    except PyMongoError as e:
        logging.error('Error looking up the ethics id: %s' % e)
        
    return None #error or no user found
