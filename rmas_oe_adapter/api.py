'''
This module wraps the functionality of the OpenEthics REST API, presenting a simplified
interface for accessing its resources.

This module relies on the 'Requests' package as a REST client.

@author: jasonmarshall
'''
import requests
import json
import logging
from rmas_adapter.conf import settings


headers = {'content-type': 'application/json', 'Authorization':settings.OE_API_AUTH_KEY}

def build_application_uri(application_id):
    '''
        Builds the uri for an application based on its uri.
    '''
    return settings.OE_API_APPLICATION_ENDPOINT + str(application_id) +'/'

def get_user(user_id):
    '''
    
        Gets the user resource from OpenEthics based on the users uri
        
        @param user_id: The OpenEthics id for the user
        @return: The user resource, or None if one cannot be found. Note if more than one
        user is found for a given filter then only the first one will be returned.
    '''
    user_id = int(user_id)#ids are always integers but we can't guarantee that the id will be received as an int so we should cast to be sure
    if user_id != None:
        logging.info('Getting user based on their open ethics id: %s' % user_id)
        user_request = requests.get(settings.OE_API_USER_ENDPOINT + str(user_id),  headers=headers)
        
        if user_request.status_code == 200:     
            #there should only be one resource returned:
            user = user_request.json
            logging.info('Found OpenEthics User: %s' % user)
            return user
        else:
            logging.error('Could not get the user from the api call returned a status of: %s' % user_request.status_code)    
    else:
        logging.error('User id was None when trying to get user resource, looks like this user does not exist in OpenEthics?')
        
    return None #Uh Oh! a problem must have occured!

def create_application(title, principle_investigator_resource):
    '''
        Creates a new ethics application
        
        @param title: The title of the new application
        @param principle_investigator_resource: the user resource which will be passed as the new applications
        principle investigator
        
        @return: the application resource uri, or None if there was a problem creating the application
    '''
    
    if principle_investigator_resource != None and 'resource_uri' in principle_investigator_resource:
        data = json.dumps({'principle_investigator':principle_investigator_resource['resource_uri'], 'title':title})
            
        new_application_request = requests.post(settings.OE_API_APPLICATION_ENDPOINT, data=data, headers=headers)
        
        if new_application_request.status_code == 201:
            new_uri =new_application_request.headers['location']
            logging.info ("created new ethics application with the following uri: %s" %new_uri)
            return new_uri
        else:
            logging.error('Could not create a new ethics application, request status was %s' % new_application_request.status_code)
    else:
        logging.error('principle investigator was None or poorly formed when trying to create a new application')
    return None #Uh Oh! a problem must have occured!
    
if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    user = get_user(1)
    
    
    
    