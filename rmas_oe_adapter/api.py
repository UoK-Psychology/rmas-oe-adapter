'''
This function wraps the functionality of the OpenEthics REST API, presenting a simplified
interface for accessing its resources.

This module relies on the 'Requests' package as a REST client.

@author: jasonmarshall
'''
import requests
import json
import logging


def create_ethics_application(title, pi):
    '''
        Uses the OpenEthics API to create a new ethics application form
        @param the title of the new ethics applicaiton
        @pi a dictionary representing the principle investigator user
        @return: the id of the new application, or None if there was a problem
    '''
    # get the openethics id from the principle nvestigator uuid
    user_endpoint = 'http://127.0.0.1:8000/api/v1/user/'
    headers = {'content-type': 'application/json', 'Authorization':'ApiKey admin:1234567890'}
    
    user_request = requests.get(user_endpoint, params={'email':pi['email']}, headers=headers)
    
    json_response = user_request.json
    
    if json_response and len(json_response['objects']) == 1:
        
        #there should only be one resource returned:
        user = json_response['objects'][0]
        user_uri =  str(user['resource_uri'])
        logging.info('Found OpenEthics User: %s' % str(user_uri))
    else:
        logging.error('Could not get the user from the api call here is the response: %s' % json_response)    
    
    if user_uri != None:
        #post a new ethics application to the OpenEthics API
        application_endpoint = 'http://127.0.0.1:8000/api/v1/application/'
        data = json.dumps({'principle_investigator':user_uri, 'title':title})
        
        new_application_request = requests.post(application_endpoint, data=data, headers=headers)
        
        if new_application_request.status_code == 201:
            new_uri =new_application_request.headers['location']
            logging.info ("created new ethics application with the following uri: %s" %new_uri)
            return new_uri
        else:
            logging.error('Could not create a new ethics application, request status was %s' % new_application_request.status_code)
    
    return None

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    new_uri= create_ethics_application('test application', {'email':'me@home.com'})
    
    
    