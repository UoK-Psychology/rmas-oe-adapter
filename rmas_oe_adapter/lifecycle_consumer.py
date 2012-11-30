'''
This module consumes lifecycle events, sent from OpenEthics about its applications via an AMQP message
queue.

@author: jasonmarshall
'''
import os
import pika
import logging
from threading import Thread
import json
from rmas_oe_adapter.mapping import get_proposal_ethics_application_link
from rmas_adapter.core.rmas_bus import RMASBus
from rmas_oe_adapter import settings
from rmas_oe_adapter.api import build_application_uri


def create_ethics_approved_event(rmas_id, start='', end='', template=os.path.abspath(os.path.join(settings.TEMPLATE_DIR,'ethics_approved.xml'))):
    '''
        This will create the RMAS-CERIF event message to tell the bus that an ethics application has been
        approved.
    '''
    
    with open(template) as template_file:
        event_message=template_file.read() % {'rmas_id':rmas_id, 'start':start, 'end':end}
    
    
    return event_message
# Create a global channel variable to hold our channel object in
channel = None
connection = None

# Step #2
def on_connected(connection):
    """Called when we are fully connected to RabbitMQ"""
    # Open a channel
    connection.channel(on_channel_open)

# Step #3
def on_channel_open(new_channel):
    """Called when our channel has opened"""
    global channel
    channel = new_channel
    channel.queue_declare(queue=settings.AMQP_QUEUE_NAME, 
                          durable=True, 
                          exclusive=False, 
                          auto_delete=True, 
                          callback=on_queue_declared)

# Step #4
def on_queue_declared(frame):
    """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ
        We now need to make sure that there is an exchange registered, it is very likely that it will already
        be declared but just in case we will declare it anyway.
    """
    channel.exchange_declare(callback=on_exchange_declared, 
                             exchange=settings.AMQP_EXCHANGE_NAME, 
                             exchange_type=settings.AMQP_EXCHANGE_TYPE)

# Step #5  
def on_exchange_declared(*args):
    '''
        Now that we have a queue and an exchange declared we can bind the two together
    '''
    channel.queue_bind(on_queue_bind, queue=settings.AMQP_QUEUE_NAME, 
                       exchange=settings.AMQP_EXCHANGE_NAME, 
                       routing_key=settings.AMQP_QUEUE_ROUTING_KEY)

# Step #6
def on_queue_bind(*args):
    '''
        Called once we have found our queue to the exchange
    '''
    channel.basic_consume(handle_delivery, queue='adapter')

# Step #7
def handle_delivery(channel, method, header, body):
    """Called when we receive a message from RabbitMQ"""
    
    
    event = json.loads(body)
    
    if event['event_type'] == 'accepted':
        
        logging.info('Received an application approved event %s' % event['application'])
        application_uri = build_application_uri(event['application'])
        proposal_ethics_application_link = get_proposal_ethics_application_link(ethics_application_id=application_uri)
        
        if proposal_ethics_application_link:
            bus = RMASBus()
            logging.info('We have got an proposal link so will send a message to the rmas bus')
            bus.push_event(create_ethics_approved_event(proposal_ethics_application_link['proposal_id']))
        else: 
            logging.info('No link found for this application, will not tell RMAS')
            

def connect():
    # Step #1: Connect to RabbitMQ using the default parameters
    
    connection = pika.SelectConnection(settings.AMQP_CONNECTION_PARAMETERS, on_connected)
    

    # Loop so we can communicate with RabbitMQ
    Thread(target=connection.ioloop.start).start()

def disconnect():
    # Gracefully close the connection
    connection.close()
    # Loop until we're fully closed, will stop on its own
    connection.ioloop.start()