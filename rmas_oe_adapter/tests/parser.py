'''
Created on Nov 13, 2012

@author: jasonmarshall
'''
from unittest2.case import TestCase
from rmas_oe_adapter.parser import create_ethics_approved_event


class CreateEthicsApprovalEventTests(TestCase):
    
    '''
        Tests relating to the create_ethics_approved_event function.
    '''
    
    def test_valid_parameters(self):
        '''
            Assuming that we pass in valid parameters, and the settings are all setup properly
            then this function should return a string based on the ethics-approved template
        '''
        
        event_message=create_ethics_approved_event('my-rmas-id')
        
        expected='''<?xml version="1.0" encoding="UTF-8"?> 
<rmas>
    <message-type>ethics-approved</message-type><!-- RMAS message type -->
    <CERIF
        xmlns="urn:xmlns:org:eurocris:cerif-1.4-0" 
        xsi:schemaLocation="urn:xmlns:org:eurocris:cerif-1.4-0http://www.eurocris.org/Uploads/Web%20pages/CERIF-1.4/CERIF_1.4_0.xsd" 
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        release="1.4"
        date="2012-04-12"
        sourceDatabase="OpenEthics">
        
        <cfProj>
            <cfProjId>my-rmas-id</cfProjId> <!-- RMAS identifier --> 
            <cfProj_Class>
                <cfClassId>11111-11111-11111-11111</cfClassId><!-- this is the uuid for the status "Ethics Approved" -->
                <cfClassSchemeId>759af93a-34ae-11e1-b86c-0800200c9a66</cfClassSchemeId><!--this is the uuid for the CERIF scheme "Activity Statuses"-->
                <cfStartDate></cfStartDate>
                <cfEndDate></cfEndDate>
            </cfProj_Class>
        </cfProj>
    </CERIF> 
</rmas>'''
        
        self.assertEqual(event_message, expected)
        
        
        
        
        
        