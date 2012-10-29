'''
This module wraps the functionality of the OpenEthics REST API, presenting a simplified
interface for accessing its resources.

This module relies on the 'Requests' package as a REST client.

@author: jasonmarshall
'''
import requests
import json
import logging


user_endpoint = 'http://127.0.0.1:8000/api/v1/user/'
headers = {'content-type': 'application/json', 'Authorization':'ApiKey admin:1234567890'}
application_endpoint = 'http://127.0.0.1:8000/api/v1/application/'

def create_ethics_application(title , **kwargs):
    '''
        Uses the OpenEthics API to create a new ethics application form
        @param the title of the new ethics applicaiton
        
        kwargs: One of these must be populated, if both are present then the email will be used.
        email - the email used to udentify the principle investigator
        uuid - the RMAS uuid used to identify the princip;e investigator (NOT YET IMPLEMENTED)
        
        @return: the id of the new application, or None if there was a problem
    '''
    #we need to ge the OpenEthics User Resource for the principle investigator:
    user_resource = get_user(**kwargs)
    
    if user_resource != None:
        
        #with a user resource we can now create the new application
        application_resource = create_application(title, user_resource)
        
        if application_resource != None:
            #we need to return the application_resource uri
            return application_resource
        else:
            logging.error('Unable to create a new application')
    else:
        logging.error('Could not find the user resource, unable to create a new application')
    
    return None #Uh Oh! a problem must have occured!

def get_user(**kwargs):
    '''
    
        Gets the user resource from OpenEthics, the method of finding the user depends on the 
        kwargs:
        
        kwargs:
        
        email - the email that will be used to identify the user in openEthics
        uuid - the uuid that will be used to identify the user in openethics (NOT YET IMPLEMENTED)
        
        @return: The user resource, or None if one cannot be found. Note if more than one
        user is found for a given filter then only the first one will be returned.
    '''
    
    json_response = None
    
    if 'email' in kwargs:
        logging.info('Getting user based on their email: %s' % kwargs['email'])
        user_request = requests.get(user_endpoint, params={'email':kwargs['email']}, headers=headers)
        json_response = user_request.json
    
        if json_response and len(json_response['objects']) == 1:
            
            #there should only be one resource returned:
            user = json_response['objects'][0]
            logging.info('Found OpenEthics User: %s' % user)
            return user
        else:
            logging.error('Could not get the user from the api call here is the response: %s' % json_response)    
    
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
            
        new_application_request = requests.post(application_endpoint, data=data, headers=headers)
        
        if new_application_request.status_code == 201:
            new_uri =new_application_request.headers['location']
            logging.info ("created new ethics application with the following uri: %s" %new_uri)
            return new_uri
        else:
            logging.error('Could not create a new ethics application, request status was %s' % new_application_request.status_code)
    
    return None #Uh Oh! a problem must have occured!
    
if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    new_uri= create_ethics_application('test rmas-oe-adapter application', email='me@home.com')
    
    
    
    
    