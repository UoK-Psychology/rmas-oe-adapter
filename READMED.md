This adapter will sit between the RMAS communication bus[1], and the OpenEthics[2] API.

It has one responsibility:

Poll the bus for proposal-created messages, and when one is received, create a new
OpenEthics application form using the OpenEthics API.

[1]https://github.com/UoK-Psychology/RMAS-ServiceBus
[2]https://github.com/UoK-Psychology/Openethics
