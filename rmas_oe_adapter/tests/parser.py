'''
Created on Nov 13, 2012

@author: jasonmarshall
'''
from unittest2.case import TestCase
from rmas_oe_adapter.parser import create_ethics_approved_event, parse_event,\
    parse_proposal_payload, _process_single_element_xpath
from lxml.etree import XMLSyntaxError, _Element, XML

class ProcessSingleElementXPathTests(TestCase):
    '''
        _process_single_element_xpath
    '''
    
    def setUp(self):
        self.test_element = XML('''
    <CERIF
        xmlns="urn:xmlns:org:eurocris:cerif-1.4-0" 
        xsi:schemaLocation="urn:xmlns:org:eurocris:cerif-1.4-0http://www.eurocris.org/Uploads/Web%20pages/CERIF-1.4/CERIF_1.4_0.xsd" 
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        release="1.4"
        date="2012-04-12"
        sourceDatabase="OpenEthics">
        <cfProj>
            <cfAcro>RMAS</cfAcro> <!-- Project acronym -->
        </cfProj>
    </CERIF>''')
    
    def test_xpath_returns_nothing(self):
        '''
            If the xpath yeilds nothing then the function should return None.
            By default the function should append the cerif namespace so you don't have to.
        '''
        
        self.assertIsNone(_process_single_element_xpath(self.test_element , 'p:cfProj/p:cfProjId'))
    
    def test_returns_element(self):
        '''
            If the xpath yeilds an element it should be returned.
        '''
        element = _process_single_element_xpath(self.test_element , 'p:cfProj/p:cfAcro')
        self.assertIsInstance(element, _Element)
        self.assertEqual(element.text, 'RMAS')
        
class ParseEventTests(TestCase):
    '''
        Tests relating to the parse_event function
    ''' 
    
    
    
    def test_invalid_event(self):
        '''
            If the event xml is invalid then an XMLSyntaxError will be raised.
        '''
        self.assertRaises(XMLSyntaxError, parse_event, 'not xml!!')
        
    def test_valid_event(self):
        '''
            If a valid event is passed in the this should returna tuple of 
            the event type, and the CERIF payload element
        '''
        
        event = '''<?xml version="1.0" encoding="UTF-8"?> 
<rmas>
    <message-type>ethics-approved</message-type><!-- RMAS message type -->
    <CERIF
        xmlns="urn:xmlns:org:eurocris:cerif-1.4-0" 
        xsi:schemaLocation="urn:xmlns:org:eurocris:cerif-1.4-0http://www.eurocris.org/Uploads/Web%20pages/CERIF-1.4/CERIF_1.4_0.xsd" 
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        release="1.4"
        date="2012-04-12"
        sourceDatabase="OpenEthics">
    </CERIF>
</rmas>'''
        event_information = parse_event(event)
        
        self.assertEqual(event_information[0], 'ethics-approved')
        self.assertIsInstance(event_information[1], _Element)
        self.assertEqual(event_information[1].tag, '{urn:xmlns:org:eurocris:cerif-1.4-0}CERIF', )
        
class ParseProposalPayloadTests(TestCase):
    
    def test_valid_payload(self):
        '''
            If a valid CERIF element is passed in which contains the data expected
            of a proposal created message then we should get back a dictionary that looks like:
            
            {
                'proposal_id':<projid>,
                'project_title':<projtitle>,
                'principle_investigator_id':<principle_investigator_person_id>,
            }
        '''
        
        element_string='''<CERIF
        xmlns="urn:xmlns:org:eurocris:cerif-1.4-0" 
        xsi:schemaLocation="urn:xmlns:org:eurocris:cerif-1.4-0http://www.eurocris.org/Uploads/Web%20pages/CERIF-1.4/CERIF_1.4_0.xsd" 
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        release="1.4"
        date="2012-04-12"
        sourceDatabase="pFact"> 
        <!-- Base project entity -->
        <cfProj>
            <cfProjId>my-project-id</cfProjId> <!-- RMAS identifier --> 
            <cfStartDate>2010-01-01</cfStartDate> <!-- Project start --> 
            <cfEndDate>2012-07-31</cfEndDate> <!-- Project end --> 
            <cfAcro>RMAS</cfAcro> <!-- Project acronym -->
            <cfTitle
                cfLangCode="EN"
                cfTrans="o">my-project</cfTitle> <!-- Link entity (denoting project co-ordinator) -->
            <cfProj_Pers><!-- Link entity (denoting project principal investigator -->
                <cfPersId>my-person-id</cfPersId>
                <cfClassId>b0e11470-1cfd-11e1-8bc2-0800200c9a66</cfClassId><!-- Formal euroCRIS UUID for 'Principal Investigator' --> 
                <cfClassSchemeId>94fefd50-1d00-11e1-8bc2-0800200c9a66</cfClassSchemeId> <!-- Formal euroCRIS UUID for 'CERIF1.3-Project-Person' --> 
                <cfStartDate>2010-01-01T00:00:00</cfStartDate> <!-- Project start --> 
                <cfEndDate>2012-07-31T00:00:00</cfEndDate> <!-- Project end -->
            </cfProj_Pers> 
        </cfProj>
    </CERIF>'''
        test_payload_element = XML(element_string)
        
        expected_output = {
                'proposal_id':'my-project-id',
                'project_title':'my-project',
                'principle_investigator_id':'my-person-id'
            }
        
        self.assertEqual(parse_proposal_payload(test_payload_element), expected_output)
        
        
    def test_invalid_data_in_payload(self):
        '''
            If an element is passed in that does not have the data structure as expected
            then a AttributeErro error should be raised
        '''
        
        invalid_cereif_element = XML('<CERIF></CERIF>')
        valid_cerif_element_missing_data=XML('''<CERIF
        xmlns="urn:xmlns:org:eurocris:cerif-1.4-0" 
        xsi:schemaLocation="urn:xmlns:org:eurocris:cerif-1.4-0http://www.eurocris.org/Uploads/Web%20pages/CERIF-1.4/CERIF_1.4_0.xsd" 
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        release="1.4"
        date="2012-04-12"
        sourceDatabase="pFact"> 
        <!-- Base project entity -->
        <cfProj>
            
            <cfStartDate>2010-01-01</cfStartDate> <!-- Project start --> 
            <cfEndDate>2012-07-31</cfEndDate> <!-- Project end --> 
            <cfAcro>RMAS</cfAcro> <!-- Project acronym -->
            <cfTitle
                cfLangCode="EN"
                cfTrans="o">my-project</cfTitle> <!-- Link entity (denoting project co-ordinator) -->
            <cfProj_Pers><!-- Link entity (denoting project principal investigator -->
                <cfPersId>my-person-id</cfPersId>
                <cfClassId>b0e11470-1cfd-11e1-8bc2-0800200c9a66</cfClassId><!-- Formal euroCRIS UUID for 'Principal Investigator' --> 
                <cfClassSchemeId>94fefd50-1d00-11e1-8bc2-0800200c9a66</cfClassSchemeId> <!-- Formal euroCRIS UUID for 'CERIF1.3-Project-Person' --> 
                <cfStartDate>2010-01-01T00:00:00</cfStartDate> <!-- Project start --> 
                <cfEndDate>2012-07-31T00:00:00</cfEndDate> <!-- Project end -->
            </cfProj_Pers> 
        </cfProj>
    </CERIF>''')#missing project id
        
        test_elements = [invalid_cereif_element,valid_cerif_element_missing_data]
        
        
        for tests in test_elements:
            self.assertRaises(AttributeError , parse_proposal_payload, tests)
        
        
class CreateEthicsApprovalEventTests(TestCase):
    
    '''
        Tests relating to the create_ethics_approved_event function.
    '''
    
    def test_valid_parameters_no_date_info(self):
        '''
            Assuming that we pass in valid parameters, and the settings are all setup properly
            then this function should return a string based on the ethics-approved template.
            if no date information is specified then startDate and endDate should remain blank
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
        
    def test_valid_parameters_with_date_info(self):
        '''
            If the start and end parameters are set then these should be present in the output from the template
            no date formatting is carried out it just substitutes the start and end as strings
        '''    
        
        event_message=create_ethics_approved_event('my-rmas-id', start='startDate', end='endDate')
        
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
                <cfStartDate>startDate</cfStartDate>
                <cfEndDate>endDate</cfEndDate>
            </cfProj_Class>
        </cfProj>
    </CERIF> 
</rmas>'''
        
        self.assertEqual(event_message, expected)
        
        
        