import os
import logging

if __name__ == '__main__':

    #this has to come first before you import any other modules otherwsise the settings won't be intitialized
    os.environ.setdefault("RMAS_ADAPTER_SETTINGS", "settings")
    
    logging.basicConfig(level=logging.INFO)
    
    from rmas_adapter.core.poller import start_polling
    from rmas_oe_adapter import lifecycle_consumer
    
    lifecycle_consumer.connect()#start listening for oe lifecycle events
    start_polling()#start polling for rmas events