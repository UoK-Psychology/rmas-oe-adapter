'''
This function wraps the functionality of the OpenEthics REST API, presenting a simplified
interface for accessing its resources.

This module relies on the 'Slumber' package as a REST client.

@author: jasonmarshall
'''


def create_ethics_application(title, pi):
    '''
        Uses the OpenEthics API to create a new ethics application form
        
        @return: the id of the new application, or None if there was a problem
    '''
    # get the openethics id from the principle nvestigator uuid
    
    #post a new ethics application to the OpenEthics API
    
    #return the new id (or None)
    return 1