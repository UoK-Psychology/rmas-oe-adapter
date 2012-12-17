How we sync RMAS and OpenEthics Users
=======================================
We have written a blog post to give some context around this which you can read at this url http://blogs.kent.ac.uk/rmas-ee/2012/12/11/lessons-learned-synchronizing-users/.

Essentially we are using a `MongoDb <http://www.mongodb.org>`_ datastore to store links between RMAS User IDs and OpenEthics IDs.
Thisese links need to be created manually at present. If a link doesn't exist, then this won't cause the 
software to crash, instead it will be logged that the adapter couldn't find a link.

To establish a link you can use the `mongo shell <http://www.mongodb.org/display/DOCS/mongo+-+The+Interactive+Shell>`_ ::

	> use oe_rmas_adapter
	> db.people_links.save({"person_id":11111111111, "ethics_user_id":1234})


