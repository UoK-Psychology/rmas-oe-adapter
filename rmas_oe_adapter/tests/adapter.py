'''
Created on Nov 13, 2012

@author: jasonmarshall
'''
from unittest2.case import TestCase

class HandleEventTests(TestCase):
    
    def test_valid_proposal_created_event(self):
        '''
            If a valid proposal created event is passed in then this function should
            call the handle_proposal_created_function, passing in the cerif payload
        '''
        self.assertTrue(False)
    
    def test_valid_other_element(self):
        '''
            If a valid event is passed in, but it is not a proposal-created event 
            then this function should not call handle_proposal_created
        '''
        self.assertTrue(False)
        
    def test_invalid_element(self):
        '''
            If an invalid event is passed in then this function should log an error but
            take no further action
        '''
        self.assertTrue(False)
        
class HandleProposalCreatedTests(TestCase):
    
    def test_valid_payload(self):
        '''
            If a valid payload is passed in then this function should firstly parse the payload using
            parse_proposal_payload, it should then call the create_application function to create an 
            OE application (passing in the relevant information from the payload), and then with the returned
            OE application id, it should persist a link between the proposal and the oe application
        '''
        self.assertTrue(False)
    
    def test_invalid_payload(self):
        '''
            If the payload is invalid then the function should log an error and take no further action.
        '''
        self.assertTrue(False)