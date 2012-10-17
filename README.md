##rmas-oe-adapter##

This adapter will sit between the [RMAS communication bus] [esb], and the [OpenEthics] [oe] API.

It has one responsibility:

Poll the bus for proposal-created messages, and when one is received, create a new
OpenEthics application form using the OpenEthics API.

[esb]:https://github.com/UoK-Psychology/RMAS-ServiceBus
[oe]:https://github.com/UoK-Psychology/Openethics
