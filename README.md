##rmas-oe-adapter##

This adapter will sit between the [RMAS communication bus] [esb], and the [OpenEthics] [oe] API.

It has one responsibility:

Poll the bus for proposal-created messages, and when one is received, create a new
OpenEthics application form using the OpenEthics API.

[esb]:https://github.com/UoK-Psychology/RMAS-ServiceBus
[oe]:https://github.com/UoK-Psychology/Openethics


This is the example message ([from the RMAS supplier documentation](http://blogs.kent.ac.uk/rmas-ee/files/2012/10/RMAS-Supplier-Documentation.pdf)) that we are targetting:

```xml
<?xml version="1.0" encoding="UTF-8"?> 
<rmas>
	<message-type>Proposal-created</message-type><!-- RMAS message type -->
	<!-- CERIF payload -->
	<CERIF
		xmlns="urn:xmlns:org:eurocris:cerif-1.4-0" 
		xsi:schemaLocation="urn:xmlns:org:eurocris:cerif-1.4-0http://www.eurocris.org/Uploads/Web%20pages/CERIF-1.4/CERIF_1.4_0.xsd" 
		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
		release="1.4"
		date="2012-04-12"
		sourceDatabase="pFact"> 
		<!-- Base project entity -->
		<cfProj>
			<cfProjId>urn:rmas:0078:pfact:2.02:UUID</cfProjId> <!-- RMAS identifier --> 
			<cfStartDate>2010-01-01</cfStartDate> <!-- Project start --> 
			<cfEndDate>2012-07-31</cfEndDate> <!-- Project end --> 
			<cfAcro>RMAS</cfAcro> <!-- Project acronym -->
			<cfTitle
				cfLangCode="EN"
				cfTrans="o">Research Management and Administration System</cfTitle> <!-- Link entity (denoting project co-ordinator) -->
			<cfProj_OrgUnit>
				<cfOrgUnitId>orgunit-exeter-internal-id</cfOrgUnitId>
				<cfClassId>c31d3380-1cfd-11e1-8bc2-0800200c9a66</cfClassId><!-- Formal euroCRIS UUID for 'Coordinator' --> 
				<cfClassSchemeId>6b2b7d25-3491-11e1-b86c-0800200c9a66</cfClassSchemeId><!-- Formal euroCRIS UUID for 'CERIF1.3-Project-Organisation' -->
			  	<cfStartDate>2010-01-01T00:00:00</cfStartDate> <!-- Project start --> 
			  	<cfEndDate>2012-07-31T00:00:00</cfEndDate> <!-- Project end -->
			</cfProj_OrgUnit>
		
			<cfProj_Pers><!-- Link entity (denoting project principal investigator -->
				<cfPersId>pers-simon-foster-internal-id</cfPersId>
				<cfClassId>b0e11470-1cfd-11e1-8bc2-0800200c9a66</cfClassId><!-- Formal euroCRIS UUID for 'Principal Investigator' --> 
				<cfClassSchemeId>94fefd50-1d00-11e1-8bc2-0800200c9a66</cfClassSchemeId> <!-- Formal euroCRIS UUID for 'CERIF1.3-Project-Person' --> 
				<cfStartDate>2010-01-01T00:00:00</cfStartDate> <!-- Project start --> 
				<cfEndDate>2012-07-31T00:00:00</cfEndDate> <!-- Project end -->
			</cfProj_Pers> 
		</cfProj>
	
		<cfOrgUnit><!-- Referenced organisation entity -->
			<cfOrgUnitId>orgunit-exeter-internal-id</cfOrgUnitId>
			<cfName cfLangCode="en_GB" cfTrans="o">University of Exeter</cfName>
		</cfOrgUnit>
	
		<cfPers> <!-- Referenced person entity -->
			<cfPersId>pers-simon-foster-internal-id</cfPersId> 
			<cfGender>m</cfGender>
			<cfPersName>
				<cfFamilyNames>Foster</cfFamilyNames>
				<cfFirstNames>Simon</cfFirstNames> 
			</cfPersName>
		</cfPers>
	</CERIF>
</rmas>
```

You can push this message to the ESB using the utility module: message_sender.py, but make sure that the ESB is running on localhost at port 7789 first:

```python message_sender.py```
