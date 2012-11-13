'''
This module consumes lifecycle events, sent from OpenEthics about its applications via an AMQP message
queue.

@author: jasonmarshall
'''

import pika
import logging
from threading import Thread
import json
from rmas_oe_adapter.mapping import get_proposal_ethics_application_link
from rmas_oe_adapter.rmas_bus import push_event
from rmas_oe_adapter.parser import create_ethics_approved_event

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
    channel.queue_declare(queue="adapter", durable=True, exclusive=False, auto_delete=True, callback=on_queue_declared)

# Step #4
def on_queue_declared(frame):
    """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ
        We now need to make sure that there is an exchange registered, it is very likely that it will already
        be declared but just in case we will declare it anyway.
    """
    channel.exchange_declare(callback=on_exchange_declared, exchange='openethics_events', exchange_type='fanout')

# Step #5  
def on_exchange_declared(*args):
    '''
        Now that we have a queue and an exchange declared we can bind the two together
    '''
    channel.queue_bind(on_queue_bind, queue='adapter', exchange='openethics_events', routing_key='')

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
        
        logging.info('Received an application approved event')
        proposal_ethics_application_link = get_proposal_ethics_application_link(ethics_application_id=event['application'])
        
        if proposal_ethics_application_link:
            logging.info('We have got an proposal link so will send a message to the rmas bus')
            push_event(create_ethics_approved_event(proposal_ethics_application_link))
        else: 
            logging.info('No link found for this application, will not tell RMAS')
            

def connect():
    # Step #1: Connect to RabbitMQ using the default parameters
    parameters = pika.ConnectionParameters()
    connection = pika.SelectConnection(parameters, on_connected)
    

    # Loop so we can communicate with RabbitMQ
    Thread(target=connection.ioloop.start).start()

def disconnect():
    # Gracefully close the connection
    connection.close()
    # Loop until we're fully closed, will stop on its own
    connection.ioloop.start()