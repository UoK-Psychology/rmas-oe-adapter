Install, Configure and Run
==========================

This document helps you install the software. There are a couple of ways to install it, but
if you dont have a lot of Python experience then you should use **pip** to install it:::

	pip install RMAS-OE-Adapter
	
This pre-supposes that you have pip installed if not then follow these 'instructions <http://www.pip-installer.org/en/latest/installing.html>`_

In order for the adapter to work there are two sub-systems that it relies on:

* AMQP Server : We have tested this using RabbitMQ, but in theory you could use any AMQP server (ymmv)
* RMAS Service bus : We are using our own RMAS Service bus - https://github.com/UoK-Psychology/RMAS-ServiceBus
* MongoDb server : This is used to persist links between users, and applications.

By using pip to install the software, it will install the pre-requisites and put a script
in you path that will allow you to run the adapter:::

	python rmas_oe_adapter_runner.py
	
This uses the default settings module, which assumes that the AMQP Server and the RMAS Service Bus
are running locally, and that you want to poll every 5 seconds.

If you want to use any other settings then you will need to download the package and install it
manually:

1. Downlad the package from PyPi using this link: http://pypi.python.org/packages/source/R/RMAS-OE-Adapter/RMAS-OE-Adapter-0.1.3.tar.gz
2. Extract the package from the downloaded tar ball (you'll need 7-zip if on windows)
3. You then need to install the pre-requisites, this can be done using pip by running:::
	
	pip install -r requirements.txt #(requirements.txt is in the root of the package so you will need to cd into that directory first)
	
4. Having done this, you can make the nescessary changes to the settings.py module (refer to the documentation for the settings module)
5. You can then run the adapter:::

	python runner.py
	

	

