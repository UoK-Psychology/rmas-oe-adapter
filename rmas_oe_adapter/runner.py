import os
import logging

def run():
    '''
        This function starts the lifecycle consumer which will start
        listening for OpenEthics lifecycle events, and then it will start
        polling the RMAS ESB for RMAS events (polling is blocking so you must 
        start the liefecycle consumer first).
    '''
    #this has to come first before you import any other modules otherwsise the settings won't be intitialized
    os.environ.setdefault("RMAS_ADAPTER_SETTINGS", "rmas_oe_adapter.settings")
    
    logging.basicConfig(level=logging.INFO)
    
    from rmas_adapter.core.poller import start_polling
    from rmas_oe_adapter import lifecycle_consumer
    
    lifecycle_consumer.connect()#start listening for oe lifecycle events
    start_polling()#start polling for rmas events

if __name__ == '__main__':
    run()
    