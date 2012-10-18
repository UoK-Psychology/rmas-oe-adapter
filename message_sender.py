'''
Utility module that can be used to send the test proposal created message to the esb

@author: jasonmarshall
'''
from suds.client import Client
import logging

if __name__=='__main__':
    
    with open('test_message.xml', 'r') as message:
        
        
        logging.basicConfig(level=logging.INFO)
        
        test_event = message.read()
        client = Client('http://localhost:7789/?wsdl', cache=None)
        success = client.service.pushEvent(test_event)
        
        if success:
            logging.info('Message pushed succesfully')
        else:
            logging.error('Message push FAILED!')
