'''
Created on Oct 18, 2012

@author: jasonmarshall
'''

import logging
from pymongo import Connection
from pymongo.errors import PyMongoError

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


def get_ethics_user(rmas_id):
    '''
        Gets the OpenEthics user id based on the rmas_id supplied. If there is no
        matching user then this function will return None.
    '''
