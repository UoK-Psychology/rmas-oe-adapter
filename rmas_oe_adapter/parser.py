'''

'''

from lxml import etree
import logging
import os
from rmas_adapter.conf import settings





def create_ethics_approved_event(rmas_id, start='', end='', template=os.path.abspath(os.path.join(settings.TEMPLATE_DIR,'ethics_approved.xml'))):
    '''
        This will create the RMAS-CERIF event message to tell the bus that an ethics application has been
        approved.
    '''
    
    with open(template) as template_file:
        event_message=template_file.read() % {'rmas_id':rmas_id, 'start':start, 'end':end}
    
    
    return event_message
